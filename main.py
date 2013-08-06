# from mininet.cli import CLI
# from mininet.log import setLogLevel, info, error
# from mininet.net import Mininet
# from mininet.node import RemoteController, OVSKernelSwitch
# from mininet.topolib import TreeTopo
# from mininet.topo import Topo
# from mininet.util import quietRun, irange
# from mininet.link import Intf

import logging
def delete_logs():
    if os.path.isfile(LOG_FILEPATH):
        os.remove(LOG_FILEPATH)
    if os.path.isfile(ROOT_LOG_FILEPATH):
        os.remove(ROOT_LOG_FILEPATH)
    if os.path.isfile(MALWARE_LOG_PATH):
        os.remove(MALWARE_LOG_PATH)

logger_MininetCE   = logging.getLogger("MininetCE")
logger_MalwareProp = logging.getLogger("MalwareProp")

def config_logger():
    '''Create loggers. Setting up the format of log files.
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename= ROOT_LOG_FILEPATH,
                        filemode='w')
    logger_MininetCE.addHandler(logging.FileHandler(LOG_FILEPATH))
    logger_MalwareProp.addHandler(logging.FileHandler(MALWARE_LOG_PATH))


from paramiko import *
from time import sleep
from random import randint
import os
import cmd
import sys
import threading
from SocketServer import ThreadingUDPServer, DatagramRequestHandler
import networkx as nx


# SOME IMPORTANT CONSTANTS =)
MININETCE_HOME_FOLDER = '/Users/vitalyantonenko/PycharmProjects/MininetClusterManagerRC'

LOG_FILEPATH      = MININETCE_HOME_FOLDER + '/logs/MininetCluster.log'
ROOT_LOG_FILEPATH = MININETCE_HOME_FOLDER + '/logs/MininetCluster_root.log'
MALWARE_LOG_PATH  = MININETCE_HOME_FOLDER + '/logs/MalwarePropagation.log'
SRC_SCRIPT_FOLDER = MININETCE_HOME_FOLDER + '/scripts/'
DST_SCRIPT_FOLDER = '/home/clusternode/MininetScripts/'
NODELIST_FILEPATH = MININETCE_HOME_FOLDER + '/config/nodelist.txt'

MALWARE_CENTER_IP   = "10.211.55.2"
MALWARE_CENTER_PORT = 56565

CLUSTER_NODE_MACHINE_NAME = 'clusternode-Parallels-Virtual-Platform'

MALWARE_PROP_DELAY             = 0
MALWARE_INIT_INF_PROB          = 5
MININET_SEGMENT_CREATION_DELAY = 0


# MININETCE SIMULATION MODES CONSTANTS
MALWARE_PROPAGATION_MODE = False
CLI_MODE                 = True

MALWARE_PROP_STEP_NUMBER = 101

HOST_NUMBER  = 250 # number of hosts in one cluster node
HOST_NETMASK = 16 # mask of host intf on mininet cluster node

malware_node_list = []
malware_list_semaphore = threading.BoundedSemaphore(value=1)


from KThread import KThread
import mininet_script_generator
import mininet_script_operator
from cluster_cmd_manager import *
from cluster_ssh_manager import *
from cluster_mininet_cmd_manager import *
from cluster_support import *
from host_configurator import *
from CLI_Director import CLI_director
from Malware_Node import Malware_Node


node_map         = {} # maps node IP to node username
node_intf_map    = {} # maps node IP to node outbound interface
node_IP_gr_map   = {}
host_map         = {} # maps host IP to host name
host_to_node_map = {} # maps host IP to node IP
ssh_map          = {} # maps node IP to ssh session object
ssh_chan_map     = {}
ssh_sessions_map = {}
ssh_stdin_map    = {} # maps node IP to ssh stdin flow
ssh_stdout_map   = {} # maps node IP to ssh stdout flow
ssh_stderr_map   = {} # maps node IP to ssh stderr flow




def read_nodelist_from_file(nodelist_filepath):
    '''Read list of cluster nodes from file.

    Args:
        nodelist_file: Name of file with list of cluster nodes.
    '''
    # open nodelist file
    logger_MininetCE.info('Reading nodelist from file')
    nodelist_file = open(nodelist_filepath, 'r')
    file_lines = nodelist_file.readlines()
    for file_line in file_lines:
        splitted_line = file_line.split(' ')
        node_map[splitted_line[0]]      = splitted_line[1]
        node_intf_map[splitted_line[0]] = splitted_line[2][:-1]
    logger_MininetCE.info('DONE!')



class Malware_request_handler(DatagramRequestHandler):
    '''Class for handling request from host process about there infectioning.
    '''
    def handle(self):
        malware_list_semaphore.acquire()
        new_infected_ip = self.rfile.read()
        print("MALWARE:" + node_IP + ": " + "New worm instance " + str(new_infected_ip))
        logger_MininetCE.info("MALWARE:" + node_IP + ": " + "New worm instance " + str(new_infected_ip))
        new_infected_node = self.is_mal_node_in_network(new_infected_ip)
        if new_infected_node is not None:
            if new_infected_node.is_vulnerable():
                new_infected_node.set_infected(True)
        malware_list_semaphore.release()

    def is_mal_node_in_network(self,IP):
        for mal_node in malware_node_list:
            if mal_node.get_host_IP() == IP:
                return mal_node
        return None


class Malware_propagation_director:
    def __init__(self):
        self.server_thread = KThread(target=self.start_malware_center, args=(MALWARE_CENTER_IP, MALWARE_CENTER_PORT))
        self.server_thread.start()
        self.try_count = 0
        self.success_count = 0
        self.count = 0
        self.critical = threading.BoundedSemaphore(value=1)
        self.current_population = 0

        self.sniffer_node_map = {}
        self.generator_node_map = {}

        self.available_map = {}
        self.ping_map = {}

    def set_init_population(self, init_population):
        self.current_population = init_population

    def inc_try_count(self):
        self.critical.acquire()
        self.try_count += 1
        self.critical.release()

    def inc_success_count(self):
        self.critical.acquire()
        self.success_count += 1
        self.critical.release()

    def inc_count(self):
        self.critical.acquire()
        self.count += 1
        self.critical.release()

    def dec_count(self):
        self.critical.acquire()
        self.count -= 1
        self.critical.release()

    def start_malware_center(self, ip="1.2.3.254", port=56565):
        server = ThreadingUDPServer((ip, port), Malware_request_handler)
        server.allow_reuse_address = True
        print("server started")
        server.serve_forever()
        return server

    def stop_malware_center(self):
        print("server stoped")
        self.server_thread.kill()

    def add_malware_node(self, host_IP, cluster_IP, vulnerable, infected ):
        malware_node = Malware_Node( host_IP, cluster_IP, vulnerable, infected )
        malware_node_list.append( malware_node )

    def is_mal_node_in_network(self,IP):
        for mal_node in malware_node_list:
            if mal_node.get_host_IP() == IP:
                return mal_node
        return None

    # def operate_with_mal_node(self, mal_node):
    #     if mal_node.is_infected():
    #
    #         victim_ip = get_random_test_IP()
    #         cmd = host_map[mal_node.get_host_IP()] + ' ping ' + victim_ip + " -c 2"
    #         available = send_mininet_ping_to_cluster_node(mal_node.get_cluster_IP(), cmd, ssh_chan_map)
    #
    #         victim_node = self.is_mal_node_in_network(victim_ip)
    #
    #         if (victim_node is not None) and available:
    #             if victim_node.is_vulnerable():
    #                 intf_name = host_map[victim_ip] + "-eth0"
    #                 cmd = host_map[victim_ip] + ' python ' + DST_SCRIPT_FOLDER + 'port_sniffer.py ' + victim_ip + \
    #                       "pin " + intf_name
    #                 send_mininet_cmd_to_cluster_node(victim_node.get_cluster_IP(), cmd)
    #                 self.inc_success_count()
    #             intf_name = host_map[mal_node.get_host_IP()] + "-eth0"
    #             cmd = host_map[mal_node.get_host_IP()] + ' python ' + DST_SCRIPT_FOLDER + 'scapy_packet_gen.py ' \
    #                   + victim_ip + " " + intf_name
    #             send_mininet_cmd_to_cluster_node(mal_node.get_cluster_IP(), cmd)
    #         self.inc_try_count()

    def setup_sniffer(self, sniffer_list):
        for sniffer in sniffer_list:
            victim_node = sniffer[0]
            victim_ip   = sniffer[1]
            intf_name = host_map[victim_ip] + "-eth0"
            cmd = host_map[victim_ip] + ' python ' + DST_SCRIPT_FOLDER + 'port_sniffer.py ' + victim_ip + \
                  " " + intf_name
            send_mininet_cmd_to_cluster_node(victim_node.get_cluster_IP(), cmd, ssh_chan_map)

    def setup_generator(self, generator_list):
        for generator in generator_list:
            mal_node  = generator[0]
            victim_ip = generator[1]
            intf_name = host_map[mal_node.get_host_IP()] + "-eth0"
            cmd = host_map[mal_node.get_host_IP()] + ' python ' + DST_SCRIPT_FOLDER + 'scapy_packet_gen.py ' \
                  + victim_ip + " " + intf_name
            send_mininet_cmd_to_cluster_node(mal_node.get_cluster_IP(), cmd, ssh_chan_map)

    def search_victim(self, mal_node):
        if mal_node.is_infected():
            victim_ip = get_random_test_IP()
            if mal_node.get_cluster_IP() not in self.ping_map.keys():
                self.ping_map[mal_node.get_cluster_IP()] = [(mal_node.get_host_IP(), victim_ip)]
            else:
                self.ping_map[mal_node.get_cluster_IP()].append((mal_node.get_host_IP(), victim_ip))

    def make_ping(self, ping_list, node_IP):
        for ping in ping_list:
            src_ip = ping[0]
            dst_ip = ping[1]
            cmd = host_map[src_ip] + ' ping ' + dst_ip + " -c 2"
            available = send_mininet_ping_to_cluster_node(node_IP, cmd, ssh_chan_map)
            self.available_map[(src_ip, dst_ip)] = available
            self.inc_try_count()

    def operate_with_mal_node(self):
        for pair_host, available in self.available_map.items():
            if available:
                mal_ip = pair_host[0]
                victim_ip = pair_host[1]
                mal_node = self.is_mal_node_in_network(mal_ip)
                victim_node = self.is_mal_node_in_network(victim_ip)
                if (victim_node is not None) and (mal_node is not None):
                    if victim_node.is_vulnerable():
                        if victim_node.get_cluster_IP() not in self.sniffer_node_map.keys():
                            self.sniffer_node_map[victim_node.get_cluster_IP()] = [(victim_node, victim_ip)]
                        else:
                            self.sniffer_node_map[victim_node.get_cluster_IP()].append((victim_node, victim_ip))
                        self.inc_success_count()
                    if mal_node.get_cluster_IP() not in self.generator_node_map.keys():
                        self.generator_node_map[mal_node.get_cluster_IP()] = [(mal_node, victim_ip)]
                    else:
                        self.generator_node_map[mal_node.get_cluster_IP()].append((mal_node, victim_ip))

    def propagation_step_threaded(self):
        self.success_count = 0
        self.try_count = 0
        self.sniffer_node_map   = {}
        self.generator_node_map = {}

        self.ping_map = {}
        for mal_node in malware_node_list:
            self.search_victim(mal_node)

        self.available_map = {}
        ping_threads = []
        for node_ip in self.ping_map.keys():
            thread = KThread(target=self.make_ping, args=(self.ping_map[node_ip], node_ip))
            ping_threads.append(thread)
        for thread in ping_threads:
            thread.start()
        for thread in ping_threads:
            thread.join()

        self.operate_with_mal_node()
        self.current_population += self.success_count
        logger_MalwareProp.info(str(self.try_count) + "\t\t\t" + str(self.success_count) +
                                "\t\t\t" + str(self.current_population) + '\t\t\t' + str(len(malware_node_list)))

        sniffer_threads = []
        for node_ip in self.sniffer_node_map.keys():
            thread = KThread(target=self.setup_sniffer, args=(self.sniffer_node_map[node_ip],))
            sniffer_threads.append(thread)
        for thread in sniffer_threads:
            thread.start()
        for thread in sniffer_threads:
            thread.join()

        generator_threads = []
        for node_ip in self.generator_node_map.keys():
            thread = KThread(target=self.setup_generator, args=(self.generator_node_map[node_ip],))
            generator_threads.append(thread)
        for thread in generator_threads:
            thread.start()
        for thread in generator_threads:
            thread.join()

        sleep(MALWARE_PROP_DELAY)

    # def propagation_step(self):
    #     self.success_count = 0
    #     self.try_count = 0
    #     for mal_node in malware_node_list:
    #         self.operate_with_mal_node(mal_node)
    #     logger_MalwareProp.info(str(self.success_count) + "\t\t\t" + str(self.try_count) +
    #                           '\t\t\t' + str(len(malware_node_list)))
    #     sleep(MALWARE_PROP_DELAY)

    def propagation_loop(self, step_number):
        for i in xrange(step_number):
            print("STEP: " + str(i))
            self.propagation_step_threaded()

    def get_infected_nodes_number(self):
        count = 0
        for mal_node in malware_node_list:
            if mal_node.is_infected():
                count += 1
        return count

    def show_node_list(self):
        for mal_node in malware_node_list:
            mal_node.show()
        print("infected nodes number = " + str(self.get_infected_nodes_number()))


# def host_process_configurator_nodegroup(node_IP, node_group, first_host_ip, CIDR_mask, leaves):
#     # curr_host = first_host
#     curr_host_ip = first_host_ip
#     for node in node_group:
#         if node in leaves:
#             # reset config on host interface
#             curr_host = 'h' + str(node)
#             cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 0'
#             send_mininet_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map)
#             # config new IP address on host interface
#             cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 ' + curr_host_ip + '/' + CIDR_mask
#             send_mininet_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map)
#             host_to_node_map[curr_host_ip] = node_IP
#             host_map[curr_host_ip] = curr_host
#             if MALWARE_PROPAGATION_MODE:
#                 malware_list_semaphore.acquire()
#                 malware_director.add_malware_node(curr_host_ip, node_IP, True, randomize_infected(MALWARE_INIT_INF_PROB))
#                 malware_list_semaphore.release()
#             # prepare for next host
#             curr_host_ip = get_next_IP(curr_host_ip)


def malware_propagation_mode():
    # prepare malware director
    malware_director = Malware_propagation_director()

    init_population_number = malware_director.get_infected_nodes_number()
    logger_MalwareProp.info("Try\t\t\tSuccess\t\t\tCurrent\t\t\tTotal")
    logger_MalwareProp.info("0\t\t\t" + "0\t\t\t" + str(init_population_number) +
                            '\t\t\t' + str(len(malware_node_list)))
    malware_director.set_init_population(init_population_number)
    malware_director.propagation_loop(MALWARE_PROP_STEP_NUMBER)
    malware_director.show_node_list()
    print("initial population number = " + str(init_population_number))
    print("total population number = " + str(HOST_NUMBER * len(node_map.items())))

    malware_director.stop_malware_center()

def cli_mode():
    cli_director = CLI_director(host_map, host_to_node_map, ssh_chan_map)
    cli_director.cmdloop()

if __name__ == '__main__':
    util.log_to_file('paramiko.log')

    # config logger
    delete_logs() # for testing period ONLY
    config_logger()
    print('Configuring loggers - DONE!')

    # take nodelist from file
    read_nodelist_from_file(NODELIST_FILEPATH)
    print('Taking nodelist from config file - DONE!')

    # open ssh sessions to nodes
    ssh_map, ssh_chan_map = open_ssh_to_nodes(node_map)
    print('Opening SSH connections to all nodes in Cluster - DONE!')

    # prepare scripts to nodes
    G = nx.Graph()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        G = mininet_script_operator.standard_mininet_script_parser(sys.argv[1], G)
    else:
        G = mininet_script_operator.standard_mininet_script_parser('test_script', G)
    print('Parsing network graph - DONE!')

    leaves = mininet_script_operator.define_leaves_in_graph(G)
    node_groups, edge_groups = mininet_script_operator.split_graph_on_parts(G, len(node_map))
    for gr_number in node_groups.keys():
        node_IP_gr_map[node_map.keys()[gr_number]] = gr_number
    print('Splitting network graph for nodes - DONE!')

    mininet_script_generator.generate_mininet_turn_on_script_auto(node_intf_map, node_groups,
                                                                      edge_groups, leaves, node_map)
    print('Generating start up scripts for nodes Mininet - DONE!')

    # for node_IP in node_map.keys():
    #    mininet_script_generator.generate_mininet_turn_on_script(node_IP, node_intf_map[node_IP], HOST_NUMBER)
    #    logger_MininetCE.info('generating turn on script for ' + str(node_IP))

    # send scripts to nodes
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=send_support_scripts_to_cluster_node, args=(node_IP, node_map))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending scripts to nodes - DONE!')

    # STAGE 1. Execute start-up scripts on nodes
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=exec_start_up_script, args=(node_IP,node_intf_map, ssh_chan_map))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Executing start up scripts on nodes - DONE!')

    first_IP = '1.2.3.1'
    next_IP_pool = first_IP
    threads = []
    for node_IP in node_map.keys():
        # Configure IP address on nodes (cos by default there is 10.0.0.0/24 subnet). For correct config-function
        # execution we need to set the number of hosts proccesses on one cluster node.
        host_num = len(node_groups[node_IP_gr_map[node_IP]])
        for node in node_groups[node_IP_gr_map[node_IP]]:
            if node not in leaves:
                host_num -= 1

        thread = KThread(target=host_process_configurator_nodegroup, args=(node_IP, node_groups[node_IP_gr_map[node_IP]], next_IP_pool,
                                                                 str(HOST_NETMASK), leaves, host_to_node_map, host_map, ssh_chan_map))
        threads.append(thread)
        next_IP_pool = get_next_IP_pool(next_IP_pool, host_num)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Configuring host-proccesses eth interfaces - DONE!')

    # STAGE 2. Execute test scenario.
    # for i,node_IP  in enumerate(node_map.keys()):
    #     if node_IP == '10.30.40.62':
    #         send_mininet_cmd_to_cluster_node( node_IP, 'h1 ping 1.2.3.117 -c 2' )
    #         sleep(2)
    #     elif node_IP == '10.30.40.65':
    #         send_mininet_cmd_to_cluster_node( node_IP, 'h1 ping 1.2.3.2 -c 2' )
    #         sleep(2)

    # STAGE 2.5. Simulation
    if MALWARE_PROPAGATION_MODE:
        malware_propagation_mode()
    elif CLI_MODE:
        cli_mode()
        print('Turning OFF CLI interface - DONE!')


    # STAGE 3. Shutdown all cluster nodes.
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=send_mininet_cmd_to_cluster_node, args=(node_IP, 'exit', ssh_chan_map))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending exit to Mininet on nodes - DONE!')


    # close ssh sessions to nodes
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=send_cmd_to_cluster_node, args=(node_IP, 'exit', ssh_chan_map))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending exit to cluster nodes - DONE!')

    close_ssh_to_nodes(ssh_map)
    print('Sending CLOSE to all ssh connections - DONE!')


    print('FINISH')
