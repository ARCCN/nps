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


#nodes = {} # IP -> username, machine_name, out_intf, ssh, ssh_chan, IP_pool, controller
#hosts = {} # IP -> name, nodeIP
#groups = {} # ID -> vertexes, edges, IP

#cluster_info = {}

class NPS:
    def __init__(self, file_name="graph.txt"):
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
        self.begin_config_timestamp = time.time()
        util.log_to_file('paramiko.log')
        self.pos = None

        self.nodes = {} # IP -> username, machine_name, out_intf, ssh, ssh_chan, IP_pool, controller
        self.hosts = {} # IP -> name, nodeIP
        self.groups = {} # ID -> vertexes, edges, IP
        self.cluster_info = {}

        self.input_file_name = file_name

    def get_groups(self):
        return self.groups

    def clean(self):
        # take nodelist from file
        print('Taking nodelist from config file'.ljust(STRING_ALIGNMENT, ' ')),
        self.nodes = read_nodelist_from_file(NODELIST_FILEPATH)
        print('DONE!')
        # open ssh sessions to nodes
        print('Opening SSH to all nodes in Cluster'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(open_ssh_to_node, [], self.nodes)
        print('DONE!')
        # Deleting ovs bridges from nodes
        print('Deleting ovs bridges from cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_cmd_to_cluster_node, ['ovs-vsctl list-br | xargs -L1 ovs-vsctl del-br',], self.nodes)
        print('DONE!')
        # close ssh sessions to nodes
        print('Sending exit to cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_cmd_to_cluster_node, ['exit',], self.nodes)
        print('DONE!')
        print('Sending CLOSE to all ssh connections'.ljust(STRING_ALIGNMENT, ' ')),
        close_ssh_to_nodes(self.nodes)
        print('DONE!')
        print('FINISH')
        exit(0)

    def start(self):
        # take nodelist from file
        print('Taking nodelist from config file'.ljust(STRING_ALIGNMENT, ' ')),
        self.nodes = read_nodelist_from_file(NODELIST_FILEPATH)
        print('DONE!')

        print('Preparing graph'.ljust(STRING_ALIGNMENT, ' ')),
        if os.path.isfile(self.input_file_name):
            graph_file = open(self.input_file_name, 'r')
            graph_data = json.loads(graph_file.read())
        else:
            graph_file = open('graph.txt', 'w')
            graph_file.write(self.input_file_name)
            graph_file.close()
            graph_data = json.loads(self.input_file_name)
        print('DONE!')

        #G, pos, node_services = get_networkX_graph(graph_data)
        G, node_services = get_networkX_graph_without_pos(graph_data)
        ## this function will not use cluster nodes if there is less then 2 graph vertexes to cluster node
        #nodes = mininet_script_operator.nodes_number_optimization(G, nodes)

        print('Splitting network graph for nodes'.ljust(STRING_ALIGNMENT, ' ')),
        leaves = mininet_script_operator.define_leaves_in_graph(G)
        self.groups, self.nodes = mininet_script_operator.split_graph_on_parts(G, self.nodes)
        #print ('#$#' + str(self.groups))

        groups_file = open('tmp/groups.txt', 'w')
        groups_file.write(str(json.dumps(self.groups)))
        groups_file.close()

        #if len(groups) == 1:
        #    groups = {0: groups[1]}
        print('DONE!')

        if DRAWING_FLAG:
            print('Drawing graph'.ljust(STRING_ALIGNMENT, ' ')),
            draw_graph(G, self.groups, leaves, self.nodes, self.pos)
            print('DONE!')

        print('Generating start up scripts for nodes Mininet'.ljust(STRING_ALIGNMENT, ' ')),
        # USE WITH NSP with net apps with custom host IP
        self.hosts = mininet_script_generator.generate_mn_ns_script_with_custom_host_ip_auto(self.nodes, self.groups,
                                                                                        leaves, node_services)
        print('DONE!')

        # open ssh sessions to nodes
        print('Opening SSH connections to all nodes in Cluster'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(open_ssh_to_node, [], self.nodes)
        print('DONE!')


        # send scripts to nodes
        print('Sending scripts to nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_support_scripts_to_cluster_node, [], self.nodes)
        print('DONE!')

        if MALWARE_MODE_ON:
            print('Turn ON file monitor scripts on nodes'.ljust(STRING_ALIGNMENT, ' ')),
            # Turn ON infected hosts file monitor scripts on cluster nodes
            file_monitor_cmd = 'python ' + DST_SCRIPT_FOLDER + 'file_monitor.py ' + \
                               MALWARE_CENTER_IP + ' ' + str(MALWARE_CENTER_PORT) + ' ' + \
                               DST_SCRIPT_FOLDER + INFECTED_HOSTS_FILENAME + ' &'
            make_threaded(send_cmd_to_cluster_node, [file_monitor_cmd, ], self.nodes)
            print('DONE!')

        # Execute start-up scripts on nodes
        print('Executing start up scripts on nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(exec_start_up_script, [], self.nodes)
        print('DONE!')


        print('Configuring host-processes eth interfaces'.ljust(STRING_ALIGNMENT, ' ')),
        #node_IP_pool_map, node_IP_gr_map = define_node_ip_pool(node_groups, leaves, node_map)
        make_threaded(host_process_configurator_nodegroup, [self.groups, str(HOST_NETMASK), leaves, self.hosts], self.nodes)
        print('DONE!')

        end_config_timestamp = time.time()
        print('Setting up cluster for ' + str(end_config_timestamp-self.begin_config_timestamp) + ' sec.')

        # Simulation
        if CLI_MODE:
            self.cluster_info['switch_number'] = len(set(G.nodes()).difference(set(leaves)))
            node_info = {}
            for id, group in self.groups.items():
                if id != 'no_group':
                    h_num = len(set(group['vertexes']).intersection(leaves))
                    sw_num = len(group['vertexes']) - h_num
                    node_info[id] = (h_num, sw_num)
            self.cluster_info['node_info'] = node_info
            cli_mode(self.hosts, self.nodes, self.cluster_info)
            print('Turn OFF CLI interface'.ljust(STRING_ALIGNMENT, ' ')),
            print('DONE!')

        # Shutdown all cluster nodes.
        print('Sending exit to Mininet on nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_mininet_cmd_to_cluster_node, ['exit',], self.nodes)
        print('DONE!')

        # Deleting ovs bridges from nodes
        print('Deleting ovs bridges from cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_cmd_to_cluster_node, ['ovs-vsctl list-br | xargs -L1 ovs-vsctl del-br',], self.nodes)
        print('DONE!')

        # close ssh sessions to nodes
        print('Sending exit to cluster nodes'.ljust(STRING_ALIGNMENT, ' ')),
        make_threaded(send_cmd_to_cluster_node, ['exit',], self.nodes)
        print('DONE!')

        print('Sending CLOSE to all ssh connections'.ljust(STRING_ALIGNMENT, ' ')),
        close_ssh_to_nodes(self.nodes)
        print('DONE!')

        print('FINISH')



if __name__ == '__main__':
    if str(sys.argv[1]) == '--clean':
        nps = NPS("NO FILE")
        nps.clean()
    else:
        nps = NPS(str(sys.argv[1]))
        nps.start()