from config.config_constants import SCRIPT_FOLDER, REMOTE_CONTROLLER_IP, REMOTE_CONTROLLER_PORT
from mininet_ns_script_template import gen_mn_ns_script_by_template



def gen_turn_on_script_by_template(file, nodes_ext_intf, node_group, edge_group, ext_intf_list, leaves, node_ctrl_map):
    '''Generate turn on script for Cluster node.

    Args:
        file: File discriptor of future turn on script.
        nodes_ext_intf: Cluster node external network interface name.
        node_group: Group ID to node-list map.
        edge_group: Group ID to edge-list map.
        ext_intf_list: External network insterface name to the node group.
        leaves: List of leave-node in network graph.
    '''
    file.write('import re\n')

    file.write('from mininet.cli import CLI\n')
    file.write('from mininet.log import setLogLevel, info, error\n')
    file.write('from mininet.net import Mininet\n')
    file.write('from mininet.link import Intf\n')
    file.write('from mininet.topo import Topo\n')
    file.write('from mininet.util import quietRun\n')
    file.write('from mininet.node import RemoteController\n')
    file.write('\n')
    file.write('sw_ext_intf = [')
    for i, node in enumerate(ext_intf_list):
        file.write('\'s')
        file.write(str(node))
        file.write('\'')
        if i != len(ext_intf_list)-1:
            file.write(',')
    file.write(']')
    file.write('\n')
    file.write('\n')
    file.write('class MyTopo( Topo ):\n')
    file.write('    \"Auto generated topology for this Mininet Node\"\n')
    file.write('    def __init__( self ):\n')
    file.write('        Topo.__init__( self )\n')
    file.write('\n')
    file.write('        \"Add hosts and swiches\"\n')
    for node in node_group:
        if node in leaves:
            file.write('        h')
            file.write(str(node))
            file.write(' = self.addHost( \'h')
            file.write(str(node))
            file.write('\' )\n')
        else:
            file.write('        s')
            file.write(str(node))
            file.write(' = self.addSwitch( \'s')
            file.write(str(node))
            file.write('\' )\n')
    file.write('\n')
    file.write('        \"Add links\"\n')
    for edge in edge_group:
        file.write('        self.addLink( ')
        if edge[0] in leaves:
            file.write('h')
        else:
            file.write('s')
        file.write(str(edge[0]))
        file.write(', ')
        if edge[1] in leaves:
            file.write('h')
        else:
            file.write('s')
        file.write(str(edge[1]))
        file.write(' )\n')
    file.write('\n')
    file.write('\n')
    file.write('def checkIntf( intf ):\n')
    file.write('    "Make sure intf exists and is not configured."\n')
    file.write('    if ( \' %s:\' % intf ) not in quietRun( \'ip link show\' ):\n')
    file.write('        error( \'Error:\', intf, \'does not exist!\\n\' )\n')
    file.write('        exit( 1 )\n')
    file.write('    ips = re.findall( r\'\d+\.\d+\.\d+\.\d+\', quietRun( \'ifconfig \' + intf ) )\n')
    file.write('    if ips:\n')
    file.write('        error( \'Error:\', intf, \'has an IP address,\'\n')
    file.write('                               \'and is probably in use!\\n\' )\n')
    file.write('        exit( 1 )\n')
    file.write('\n')
    file.write('if __name__ == \'__main__\':\n')
    file.write('    setLogLevel( \'info\' )\n')
    file.write('\n')
    file.write('    intfName = \'')
    file.write(nodes_ext_intf)
    file.write('\'\n')
    file.write('    info( \'*** Checking\', intfName, \'\\n\' )\n')
    file.write('    checkIntf( intfName )\n')
    file.write('\n')
    file.write('    info( \'*** Creating network\\n\' )\n')
    file.write('    net = Mininet( topo=MyTopo(), controller=lambda name: RemoteController( name,ip=\'')
    file.write(node_ctrl_map[0])
    file.write('\',port=int(\'')
    file.write(node_ctrl_map[1])
    file.write('\') ) )\n')
    file.write('\n')
    file.write('    for sw in net.switches:\n')
    file.write('        if sw.name in sw_ext_intf:\n')
    file.write('            info( \'*** Adding hardware interface\', intfName, \'to switch\',\n')
    file.write('                sw.name, \'\\n\' )\n')
    file.write('            _intf = Intf( intfName, node=sw )\n')
    file.write('\n')
    file.write('    info( \'*** Note: you may need to reconfigure the interfaces for \'\n')
    file.write('          \'the Mininet hosts:\\n\', net.hosts, \'\\n\' )\n')
    file.write('\n')
    file.write('    net.start()\n')
    file.write('    CLI( net )\n')
    file.write('    net.stop()\n')


def generate_mininet_turn_on_script_auto(node_intf_map, node_groups, edge_groups, node_ext_intf_group, leaves,
                                         node_map, node_ctrl_map):
    '''Generate turn on script for Cluster node.

    Args:
        node_ext_intf: External network insterface name to the node.
        node_group: Group ID to node-list map.
        edge_group: Group ID to edge-list map.
        node_ext_insf_group: External network insterface name to the node group.
        leaves: List of leave-node in network graph.
        node_map: Cluster node map.
    '''
    for group in node_groups.keys():
        if group != 'ext_intf':
            node_IP = node_map.keys()[group]
            filename = 'turn_on_script_for_' + node_IP + '.py'
            filepath = SCRIPT_FOLDER + filename

            file = open(filepath, 'w')

            gen_turn_on_script_by_template(file, node_intf_map[node_IP], node_groups[group], edge_groups[group],
                                           node_ext_intf_group, leaves, node_ctrl_map[node_IP])
            file.close()




def generate_mn_ns_script_auto(node_intf_map, node_groups, edge_groups, node_ext_intf_group, leaves,
                                         node_map, node_ctrl_map, hosts_net_services):
    '''Generate turn on script for Cluster node.

    Args:
        node_ext_intf: External network insterface name to the node.
        node_group: Group ID to node-list map.
        edge_group: Group ID to edge-list map.
        node_ext_insf_group: External network insterface name to the node group.
        leaves: List of leave-node in network graph.
        node_map: Cluster node map.
    '''
    for group in node_groups.keys():
        if group != 'ext_intf':
            node_IP = node_map.keys()[group]
            filename = 'turn_on_script_for_' + node_IP + '.py'
            filepath = SCRIPT_FOLDER + filename

            file = open(filepath, 'w')

            gen_mn_ns_script_by_template(file, node_intf_map[node_IP], node_groups[group], edge_groups[group],
                                        node_ext_intf_group, leaves, node_ctrl_map[node_IP], hosts_net_services)
            file.close()



if __name__ == '__main__':
    pass

