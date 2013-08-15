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
import os
import sys
import networkx as nx
from multiprocessing import Process

from config.config_constants import STRING_ALIGNMENT, DRAWING_FLAG
from config.config_constants import LOG_FILEPATH, ROOT_LOG_FILEPATH, MALWARE_LOG_PATH, NODELIST_FILEPATH
from config.config_constants import MALWARE_PROPAGATION_MODE, CLI_MODE
from config.config_constants import HOST_NETMASK
from config.config_constants import RANDOM_GRAPH_FLAG

import mininet_script_generator
import mininet_script_operator
from cluster_cmd_manager import *
from cluster_ssh_manager import *
from cluster_mininet_cmd_manager import *
from cluster_support import *
from host_configurator import *
from cluster_manager_modes import *

node_map         = {} # maps node IP to node username
node_intf_map    = {} # maps node IP to node outbound interface
node_IP_gr_map   = {} # maps node IP to node group
host_map         = {} # maps host IP to host name
host_IP_map      = {} # maps host name to host IP
host_to_node_map = {} # maps host IP to node IP
ssh_map          = {} # maps node IP to ssh session object
ssh_chan_map     = {} # maps node IP to ssh chan objects
node_IP_pool_map = {} # maps node IP to host IP pool

if __name__ == '__main__':
    util.log_to_file('paramiko.log')
    malware_node_list = {}

    # config logger
    print('Configuring loggers'.ljust(STRING_ALIGNMENT, ' ')),
    delete_logs() # for testing period ONLY
    config_logger()
    print('DONE!')

    # take nodelist from file
    print('Taking nodelist from config file'.ljust(STRING_ALIGNMENT, ' ')),
    node_map, node_intf_map = read_nodelist_from_file(NODELIST_FILEPATH)
    print('DONE!')

    # prepare scripts to nodes
    if RANDOM_GRAPH_FLAG:
        print('Generating random network graph'.ljust(STRING_ALIGNMENT, ' ')),
        G = nx.random_lobster(6, 1.0, 0.33)
        print('DONE!')
    else:
        print('Parsing network graph'.ljust(STRING_ALIGNMENT, ' ')),
        G = nx.Graph()
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            G = mininet_script_operator.standard_mininet_script_parser(sys.argv[1], G)
        else:
            G = mininet_script_operator.standard_mininet_script_parser('test_script', G)
        print('DONE!')
    node_map, node_intf_map = mininet_script_operator.nodes_number_optimization(G, node_map, node_intf_map)


    # open ssh sessions to nodes
    print('Opening SSH connections to all nodes in Cluster'.ljust(STRING_ALIGNMENT, ' ')),
    ssh_map, ssh_chan_map = open_ssh_to_nodes(node_map)
    print('DONE!')




    print('Splitting network graph for nodes'.ljust(STRING_ALIGNMENT, ' ')),
    leaves = mininet_script_operator.define_leaves_in_graph(G)
    node_groups, edge_groups, node_ext_intf_group = mininet_script_operator.split_graph_on_parts(G, len(node_map))
    for gr_number in node_groups.keys():
        node_IP_gr_map[node_map.keys()[gr_number]] = gr_number
    print('DONE!')

    if DRAWING_FLAG:
        print('Drawing graph'.ljust(STRING_ALIGNMENT, ' ')),
        p = Process(target=mininet_script_operator.draw_graph, args=tuple([G, node_groups, edge_groups, leaves, node_map]),)
        p.daemon = True
        p.start()
        print('DONE!')

    print('Generating start up scripts for nodes Mininet'.ljust(STRING_ALIGNMENT, ' ')),
    mininet_script_generator.generate_mininet_turn_on_script_auto(node_intf_map, node_groups,
                                                                      edge_groups, node_ext_intf_group, leaves, node_map)
    print('DONE!')

    # sys.stdin.read(1)
    # exit(-1)

    # send scripts to nodes
    print('Sending scripts to nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_support_scripts_to_cluster_node, [node_map,], node_map)
    print('DONE!')

    # STAGE 1. Execute start-up scripts on nodes
    print('Executing start up scripts on nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(exec_start_up_script, [node_intf_map, ssh_chan_map], node_map)
    print('DONE!')

    print('Configuring host-processes eth interfaces'.ljust(STRING_ALIGNMENT, ' ')),
    node_IP_pool_map = define_node_ip_pool(node_groups, node_IP_gr_map, leaves, node_map)

    make_threaded(host_process_configurator_nodegroup,
                        [node_groups, node_IP_gr_map, node_IP_pool_map, str(HOST_NETMASK),
                            leaves, host_to_node_map, host_map, host_IP_map, ssh_chan_map],
                        node_map)
    print('DONE!')

    # STAGE 2. Execute test scenario.

    # STAGE 2.5. Simulation
    if MALWARE_PROPAGATION_MODE:
        malware_propagation_mode(malware_node_list)
    elif CLI_MODE:
        cli_mode(host_map, host_to_node_map, host_IP_map, ssh_chan_map)
        print('Turn OFF CLI interface'.ljust(STRING_ALIGNMENT, ' ')),
        print('DONE!')

    # STAGE 3. Shutdown all cluster nodes.
    print('Sending exit to Mininet on nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_mininet_cmd_to_cluster_node, ['exit', ssh_chan_map], node_map)
    print('DONE!')

    # close ssh sessions to nodes
    print('Sending exit to cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_cmd_to_cluster_node, ['exit', ssh_chan_map], node_map)
    print('DONE!')

    print('Sending CLOSE to all ssh connections'.ljust(STRING_ALIGNMENT, ' ')),
    close_ssh_to_nodes(ssh_map)
    print('DONE!')

    print('FINISH')
