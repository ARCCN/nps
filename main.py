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
import os
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



from KThread import KThread
import mininet_script_generator
import mininet_script_operator
from cluster_cmd_manager import *
from cluster_ssh_manager import *
from cluster_mininet_cmd_manager import *
from cluster_support import *
from host_configurator import *
from CLI_Director import CLI_director
from Malware_Propagation_Director import Malware_propagation_director

node_map         = {} # maps node IP to node username
node_intf_map    = {} # maps node IP to node outbound interface
node_IP_gr_map   = {}
host_map         = {} # maps host IP to host name
host_to_node_map = {} # maps host IP to node IP
ssh_map          = {} # maps node IP to ssh session object
ssh_chan_map     = {}
# ssh_sessions_map = {}
# ssh_stdin_map    = {} # maps node IP to ssh stdin flow
# ssh_stdout_map   = {} # maps node IP to ssh stdout flow
# ssh_stderr_map   = {} # maps node IP to ssh stderr flow


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
    node_map, node_intf_map = read_nodelist_from_file(NODELIST_FILEPATH)
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
