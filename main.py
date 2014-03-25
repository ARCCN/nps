from paramiko import *
import os, sys, time, json

from config.config_constants import STRING_ALIGNMENT, DRAWING_FLAG
from config.config_constants import NODELIST_FILEPATH
from config.config_constants import CLI_MODE
from config.config_constants import HOST_NETMASK

from src.mininettools import mininet_script_generator, mininet_script_operator

from src.clustertools.cluster_cmd_manager         import *
from src.clustertools.cluster_ssh_manager         import *
from src.clustertools.cluster_mininet_cmd_manager import *
from src.clustertools.cluster_support             import *
from src.mininettools.host_configurator           import *
from src.clustertools.cluster_manager_modes       import *
from GUIApp                                       import *


nodes = {} # IP -> username, machine_name, out_intf, ssh, ssh_chan, IP_pool, controller
hosts = {} # IP -> name, nodeIP
groups = {} # ID -> vertexes, edges, IP

cluster_info = {}

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    begin_config_timestamp = time.time()
    util.log_to_file('paramiko.log')
    malware_node_list = {}
    pos = None

    # take nodelist from file
    print('Taking nodelist from config file'.ljust(STRING_ALIGNMENT, ' ')),
    nodes = read_nodelist_from_file(NODELIST_FILEPATH)
    print('DONE!')

    print('Preparing graph'.ljust(STRING_ALIGNMENT, ' ')),
    if os.path.isfile(str(sys.argv[1])):
        graph_file = open(str(sys.argv[1]), 'r')
        graph_data = json.loads(graph_file.read())
    else:
        graph_file = open('graph.txt', 'w')
        graph_file.write(str(sys.argv[1]))
        graph_file.close()
        graph_data = json.loads(str(sys.argv[1]))
    print('DONE!')

    G, pos, node_services = get_networkX_graph(graph_data)
    ## this function will not use cluster nodes if there is less then 2 graph vertexes to cluster node
    nodes = mininet_script_operator.nodes_number_optimization(G, nodes)

    print('Splitting network graph for nodes'.ljust(STRING_ALIGNMENT, ' ')),
    leaves = mininet_script_operator.define_leaves_in_graph(G)
    groups = mininet_script_operator.split_graph_on_parts(G, len(nodes))
    if len(groups) == 1:
        groups = {0: groups[1]}
    print('DONE!')

    if DRAWING_FLAG:
        print('Drawing graph'.ljust(STRING_ALIGNMENT, ' ')),
        draw_graph(G, groups, leaves, nodes, pos)
        print('DONE!')

    print('Generating start up scripts for nodes Mininet'.ljust(STRING_ALIGNMENT, ' ')),
    # USE WITH NSP with net apps with custom host IP
    hosts = mininet_script_generator.generate_mn_ns_script_with_custom_host_ip_auto(nodes, groups,
                                                                                    leaves, node_services)
    print('DONE!')

    # open ssh sessions to nodes
    print('Opening SSH connections to all nodes in Cluster'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(open_ssh_to_node, [], nodes)
    print('DONE!')


    # send scripts to nodes
    print('Sending scripts to nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_support_scripts_to_cluster_node, [], nodes)
    print('DONE!')

    if MALWARE_MODE_ON:
        print('Turn ON file monitor scripts on nodes'.ljust(STRING_ALIGNMENT, ' ')),
        # Turn ON infected hosts file monitor scripts on cluster nodes
        file_monitor_cmd = 'python ' + DST_SCRIPT_FOLDER + 'file_monitor.py ' + \
                           MALWARE_CENTER_IP + ' ' + str(MALWARE_CENTER_PORT) + ' ' + \
                           DST_SCRIPT_FOLDER + INFECTED_HOSTS_FILENAME + ' &'
        #print file_monitor_cmd
        make_threaded(send_cmd_to_cluster_node, [file_monitor_cmd, ], nodes)
        print('DONE!')

    # Execute start-up scripts on nodes
    print('Executing start up scripts on nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(exec_start_up_script, [], nodes)
    print('DONE!')


    print('Configuring host-processes eth interfaces'.ljust(STRING_ALIGNMENT, ' ')),
    #node_IP_pool_map, node_IP_gr_map = define_node_ip_pool(node_groups, leaves, node_map)
    make_threaded(host_process_configurator_nodegroup, [groups, str(HOST_NETMASK), leaves, hosts], nodes)
    print('DONE!')

    end_config_timestamp = time.time()
    print('Setting up cluster for ' + str(end_config_timestamp-begin_config_timestamp) + ' sec.')

    # Simulation
    if CLI_MODE:
        cluster_info['switch_number'] = len(set(G.nodes()).difference(set(leaves)))
        node_info = {}
        for id, group in groups.items():
            if id != 'no_group':
                h_num = len(set(group['vertexes']).intersection(leaves))
                sw_num = len(group['vertexes']) - h_num
                node_info[id] = (h_num, sw_num)
        cluster_info['node_info'] = node_info
        cli_mode(hosts, nodes, cluster_info)
        print('Turn OFF CLI interface'.ljust(STRING_ALIGNMENT, ' ')),
        print('DONE!')

    # Shutdown all cluster nodes.
    print('Sending exit to Mininet on nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_mininet_cmd_to_cluster_node, ['exit',], nodes)
    print('DONE!')

    # Deleting ovs bridges from nodes
    print('Deleting ovs bridges from cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_cmd_to_cluster_node, ['ovs-vsctl list-br | xargs -L1 ovs-vsctl del-br',], nodes)
    print('DONE!')

    # close ssh sessions to nodes
    print('Sending exit to cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
    make_threaded(send_cmd_to_cluster_node, ['exit',], nodes)
    print('DONE!')

    print('Sending CLOSE to all ssh connections'.ljust(STRING_ALIGNMENT, ' ')),
    close_ssh_to_nodes(nodes)
    print('DONE!')

    print('FINISH')
