from paramiko import *

# from mininet.cli import CLI
# from mininet.log import setLogLevel, info, error
# from mininet.net import Mininet
# from mininet.node import RemoteController, OVSKernelSwitch
# from mininet.topolib import TreeTopo
# from mininet.topo import Topo
# from mininet.util import quietRun, irange
# from mininet.link import Intf


from KThread import KThread
from time import sleep
from random import randint
import os
import cmd
import logging
import sys
import mininet_script_generator
import mininet_script_operator
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

HOST_NUMBER  = 250 # number of hosts in one cluster node
HOST_NETMASK = 16 # mask of host intf on mininet cluster node

MALWARE_PROP_STEP_NUMBER = 101

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


def send_script_to_cluster_node(node_IP, script_filename):
    '''Send file with python script to cluster node.

    Args:
        node_IP: IP address of cluster node.
        script_filename: Name of script file. File on Cluster Manager machine and on cluster node
                         node machine will have the same name.
    '''
    # find SSH key
    # privatekeyfile = os.path.expanduser( '~/.ssh/id_rsa')
    # key = RSAKey.from_private_key_file( privatekeyfile)

    # open SFTP session to node
    transport = Transport((node_IP, 22))
    transport.connect(username=node_map[node_IP], password=node_map[node_IP])
    sftp = SFTPClient.from_transport(transport)
    logger_MininetCE.info('opening SFTP session to ' + str(node_IP))

    # config script file paths
    src_script_filepath = SRC_SCRIPT_FOLDER + script_filename
    dst_script_filepath = DST_SCRIPT_FOLDER + script_filename

    # send script via SFTP
    sftp.put(src_script_filepath, dst_script_filepath)

    # close SFTP session to node
    sftp.close()
    transport.close()
    logger_MininetCE.info('close SFTP session to ' + str(node_IP))


def send_support_scripts_to_cluster_node(node_IP):
    '''Send helpful scripts to cluster nodes.

    This scripts used in malware propagation experiment ONLY!

    Args:
        node_IP: IP address of cluster node.
    '''
    script_name = 'turn_on_script_for_' + str(node_IP) + '.py'
    send_turn_on_script_to_cluster_node(node_IP, script_name)
    send_script_to_cluster_node(node_IP, 'scapy_packet_gen.py')
    send_script_to_cluster_node(node_IP, 'port_sniffer.py')


def send_turn_on_script_to_cluster_node(node_IP, script_filename):
    '''Send start up script to cluster node.

    This script generated for each cluster node specially. The generation algorithm depends on mapping
    of simulated topology on cluster topology.

    Args:
        node_IP: IP address of cluster node.
        script_filename: Name of script file. File on Cluster Manager machine and on cluster node
                         node machine will have the same name.
    '''
    # find SSH key
    # privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
    # key = RSAKey.from_private_key_file(privatekeyfile)

    # open SFTP session to node
    transport = Transport((node_IP, 22))
    transport.connect(username=node_map[node_IP], password=node_map[node_IP])
    sftp = SFTPClient.from_transport(transport)
    logger_MininetCE.info('opening SFTP session to ' + str(node_IP))

    # config script file paths
    src_sricpt_filepath = SRC_SCRIPT_FOLDER + 'nodes/' + script_filename
    dst_script_filepath = DST_SCRIPT_FOLDER + script_filename

    # send script via SFTP
    sftp.put(src_sricpt_filepath, dst_script_filepath)

    # close SFTP session to node
    sftp.close()
    transport.close()
    logger_MininetCE.info('close SFTP session to ' + str(node_IP))

def open_ssh_to_nodes():
    '''Open SSH sessions to each node in cluster.
    '''
    for node_IP in node_map.keys():
        ssh_map[node_IP] = SSHClient()
        ssh_map[node_IP].set_missing_host_key_policy(AutoAddPolicy())
        ssh_map[node_IP].connect(hostname=node_IP, username=node_map[node_IP], password=node_map[node_IP])
        ssh_chan_map[node_IP] = ssh_map[node_IP].invoke_shell()
        logger_MininetCE.info('opening SSH session to ' + str(node_IP))


def close_ssh_to_nodes():
    '''Close SSH sessions to each node in cluster.
    '''
    for node_IP, ssh_session in ssh_map.items():
        ssh_session.close()
        # print('close SSH session to ' + str(node_IP))
        logger_MininetCE.info('close SSH session to ' + str(node_IP))


def send_cmd_to_cluster_node(node_IP, cmd):
    '''Send console command to cluster node.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.
    '''
    cmd += '\n'
    ssh_chan_map[node_IP].send(cmd)
    if cmd != 'exit\n':
        buff = ''
        endswith_str = 'root@' + CLUSTER_NODE_MACHINE_NAME + ':~# '
        while not buff.endswith(endswith_str): # Need to change name, or use the variable.
            buff += ssh_chan_map[node_IP].recv(9999)
        print('SUCCESS:' + node_IP + ': ' + cmd)
        logger_MininetCE.info('SUCCESS:' + node_IP + ': ' + cmd)


def exec_start_up_script(node_IP):
    '''Send the console command to cluster Node to execute the start up script.

    Args:
        node_IP: IP address of cluster node.
    '''
    # Flush options on eth1 interface on nodes in cluster. This interface will be use for inter
    # Mininet instances communications
    reset_intf_cmd = 'ifconfig ' + node_intf_map[node_IP] + ' 0'
    send_cmd_to_cluster_node(node_IP, reset_intf_cmd)

    split_IP = node_IP.split('.')
    reset_vs_cmd = 'ovs-vsctl del-br s' + split_IP[3]
    send_cmd_to_cluster_node(node_IP, reset_vs_cmd)

    # Turn On Mininet instance on nodes in cluster
    send_mn_turn_on_cmd_to_cluster_node(node_IP)


def send_mn_turn_on_cmd_to_cluster_node(node_IP):
    '''Send the console command to cluster node to start up the Mininet.

    Args:
        node_IP: IP address of cluster node.
    '''
    turn_on_mininet_script_name = 'turn_on_script_for_' + str(node_IP) + '.py'
    cmd = 'python ' + DST_SCRIPT_FOLDER + turn_on_mininet_script_name
    cmd += '\n'
    ssh_chan_map[node_IP].send(cmd)
    buff = ""
    while not buff.endswith('mininet> '):
        buff += ssh_chan_map[node_IP].recv(9999)
    print("SUCCESS:" + node_IP + ": Mininet turning ON")
    logger_MininetCE.info("SUCCESS:" + node_IP + ": Mininet turning ON")


def send_mininet_cmd_to_cluster_node(node_IP, cmd):
    '''Send Mininet console command to cluster node.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.
    '''

    cmd += '\n'
    ssh_chan_map[node_IP].send(cmd)
    buff = ""
    if cmd != 'exit\n':
        while not buff.endswith('mininet> '):
            buff += ssh_chan_map[node_IP].recv(9999)
        print("SUCCESS:" + node_IP + ": " + cmd)
        logger_MininetCE.info("SUCCESS:" + node_IP + ": " + cmd)


def send_mininet_ping_to_cluster_node(node_IP, cmd):
    '''Send Mininet console command PING to cluster node and check the result of its execution.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.

    Returns:
        True: If the ping reached the destination point successfully.
        False: If the ping failed to reach the destination point.
    '''
    cmd += '\n'
    ssh_chan_map[node_IP].send(cmd)
    buff = ''
    while not buff.endswith('mininet> '):
        if ssh_chan_map[node_IP].recv_ready():
            buff += ssh_chan_map[node_IP].recv(9999)
    buff_lines = buff.splitlines()
    for line in buff_lines[:-1]:
        print(line)
        # if 'Destination Host Unreachable' in buff:
        #     print('FAIL:' + node_IP + ': ' + cmd)
        #     logger_MininetCE.info('FAIL:' + node_IP + ': ' + cmd)
        #     return False
        # elif 'bytes from' in buff and 'icmp_req=' in buff and 'ttl=' in buff and 'time=' in buff:
        #     print('SUCCESS:' + node_IP + ': ' + cmd)
        #     logger_MininetCE.info('SUCCESS:' + node_IP + ': ' + cmd)
        #     return True
        # # else:
        # #     print('FAIL:' + node_IP + ': ' + cmd)
        # #     logger_MininetCE.info('FAIL:' + node_IP + ': ' + cmd)
        # #     return False


def get_next_IP(IP):
    '''Generate next IP address. The next IP address is the incrementation (+1) of current IP address.

    Args:
        IP: The current IP address.

    Returns:
        The next incremented IP address. The input and output IP addresses are strings.

    '''
    octets = IP.split('.')
    if int(octets[3]) + 1 >= 255:
        next_IP = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + 1) + '.' + '1'
    else:
        next_IP = octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + str(int(octets[3]) + 1)
    return next_IP


def get_next_IP_pool(IP, hosts_number):
    '''Generate the first IP address on next IP address pool. Depends on IP address pool size.

    Args:
        IP: The first address of current pool.
        hosts_number: The size of current pool.

    Returns:
        The first IP address of the next pool. The input and output IP addresses are strings.
    '''
    octets = IP.split('.')
    if int(octets[3]) + hosts_number >= 255:
        new_oct = divmod(int(octets[3]) + hosts_number, 255)
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + int(new_oct[0])) \
                       + '.' + str(int(new_oct[1]) + int(new_oct[0]))
    else:
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2])) \
                       + '.' + str(int(octets[3]) + hosts_number)
    return next_IP_pool


def get_next_host_name(host):
    '''Generate the next host name in Mininet network. he next host name is the incremention (+1)
        of current host name.

    Args:
        host: The current host name.

    Returns:
        The next host incremented name.
    '''
    next_nost = 'h' + str(int(host[1:]) + 1)
    return next_nost


def get_random_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    '''
    IP = str(randint(1,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255))
    return IP


def get_random_test_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    In this test function is a smaller pool of possible IP addresses. Used for experiments with malware
    propagation.
    '''
    IP = str(randint(1,1)) + '.' + str(randint(1,2)) + '.' + str(randint(1,254)) + '.' + str(randint(1,254))
    return IP


def randomize_infected(prob):
    '''Make decision of host infection, depends on infection probability.

    Args:
        prob: Host infection probability.

    Returns:
        True: If the host is infected.
        False: If the host is NOT infected.
    '''
    r = randint(1,100)
    if r <= prob:
        return True
    else:
        return False

class CLI_director(cmd.Cmd):

    def __init__(self, host_map, host_to_node_map):
        cmd.Cmd.__init__(self)
        self.prompt = "+> "
        self.intro  = "Welcome to Mininet CE console!"  ## defaults to None

        self.host_map = host_map
        self.host_to_node_map = host_to_node_map

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    def do_ping(self,args):
        args = args.split()
        if len(args) != 2:
            print('*** invalid number of arguments')
            return
        src_ip = args[0]
        dst_ip = args[1]

        cmd = self.host_map[src_ip] + ' ping -c 4 ' + dst_ip
        send_mininet_ping_to_cluster_node(self.host_to_node_map[src_ip], cmd)


    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

class Malware_Node:
    '''Class of Malware node.

    Object of this class created when new host is appeared. This is sort of mapping - list of hosts in
    simulated topology in infection topology.
    '''
    def __init__( self, host_IP, cluster_IP, vulnerable, infected ):
        '''Inits the the host node in infection topology.

        Args:
            host_IP: IP address of host.
            cluster_IP: IP address of cluster node, where the host process is located.
            vulnerable: Vulnerability indicator for host. If true this host could be infected,
                        false - could NOT.
        '''
        self.host_IP = host_IP
        self.cluster_IP = cluster_IP
        self.vulnerable = vulnerable
        self.infected = infected

    def is_infected(self):
        '''Check the infection of current host.

        Returns:
            The value of infected variable.
        '''
        return self.infected

    def is_vulnerable(self):
        '''Check the vulnerability of current host.

        Returns:
            The value of vulnerable variable.
        '''
        return self.vulnerable

    def set_infected(self, inf):
        '''Setup value of infected variable of current host.

        Args:
            inf: The new value of infected variable.
        '''
        self.infected = inf

    def get_cluster_IP(self):
        '''Found out the IP address of cluster node, where the current host process is located.

        Returns:
            The IP address of cluster node.
        '''
        return self.cluster_IP

    def get_host_IP(self):
        '''Found out the IP address of host process.

        Returns:
            The IP address of host process.
        '''
        return self.host_IP

    def show(self):
        '''Show brief info about current host.
        '''
        print("host_IP    = " + str(self.host_IP))
        print("cluster_IP = " + str(self.cluster_IP))
        print("vulnerable = " + str(self.vulnerable))
        print("infected   = " + str(self.infected))
        print('\n')


malware_node_list = []
malware_list_semaphore = threading.BoundedSemaphore(value=1)
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
    #         available = send_mininet_ping_to_cluster_node(mal_node.get_cluster_IP(), cmd)
    #
    #         victim_node = self.is_mal_node_in_network(victim_ip)
    #
    #         if (victim_node is not None) and available:
    #             if victim_node.is_vulnerable():
    #                 intf_name = host_map[victim_ip] + "-eth0"
    #                 cmd = host_map[victim_ip] + ' python ' + DST_SCRIPT_FOLDER + 'port_sniffer.py ' + victim_ip + \
    #                       " " + intf_name
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
            send_mininet_cmd_to_cluster_node(victim_node.get_cluster_IP(), cmd)

    def setup_generator(self, generator_list):
        for generator in generator_list:
            mal_node  = generator[0]
            victim_ip = generator[1]
            intf_name = host_map[mal_node.get_host_IP()] + "-eth0"
            cmd = host_map[mal_node.get_host_IP()] + ' python ' + DST_SCRIPT_FOLDER + 'scapy_packet_gen.py ' \
                  + victim_ip + " " + intf_name
            send_mininet_cmd_to_cluster_node(mal_node.get_cluster_IP(), cmd)

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
            available = send_mininet_ping_to_cluster_node(node_IP, cmd)
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


def host_process_configurator(node_IP, first_host, first_host_ip, CIDR_mask, hosts_number):
    curr_host = first_host
    curr_host_ip = first_host_ip
    for i in xrange(hosts_number):
        # reset config on host interface
        cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 0'
        send_mininet_cmd_to_cluster_node(node_IP, cmd)
        # config new IP address on host interface
        cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 ' + curr_host_ip + '/' + CIDR_mask
        send_mininet_cmd_to_cluster_node(node_IP, cmd)
        host_to_node_map[curr_host_ip] = node_IP
        host_map[curr_host_ip] = curr_host
        if MALWARE_PROPAGATION_MODE:
            malware_list_semaphore.acquire()
            malware_director.add_malware_node(curr_host_ip, node_IP, True, randomize_infected(MALWARE_INIT_INF_PROB))
            malware_list_semaphore.release()
        # prepare for next host
        curr_host    = get_next_host_name(curr_host)
        curr_host_ip = get_next_IP(curr_host_ip)


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
    cli_director = CLI_director(host_map,host_to_node_map)
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
    open_ssh_to_nodes()
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
        thread = KThread(target=send_support_scripts_to_cluster_node, args=(node_IP,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending scripts to nodes - DONE!')

    # STAGE 1. Execute start-up scripts on nodes
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=exec_start_up_script, args=(node_IP,))
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

        thread = KThread(target=host_process_configurator, args=(node_IP, 'h1', next_IP_pool,
                                                                 str(HOST_NETMASK), host_num))
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
        thread = KThread(target=send_mininet_cmd_to_cluster_node, args=(node_IP, 'exit'))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending exit to Mininet on nodes - DONE!')


    # close ssh sessions to nodes
    threads = []
    for node_IP in node_map.keys():
        thread = KThread(target=send_cmd_to_cluster_node, args=(node_IP, 'exit'))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Sending exit to cluster nodes - DONE!')

    close_ssh_to_nodes()
    print('Sending CLOSE to all ssh connections - DONE!')



    print('FINISH')
