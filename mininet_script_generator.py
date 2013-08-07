from config.config_constants import SCRIPT_FOLDER, REMOTE_CONTROLLER_IP, REMOTE_CONTROLLER_PORT

def gen_turn_on_script_by_template(file, nodes_ext_intf, node_group, edge_group, leaves):
    file.write('import re\n')

    file.write('from mininet.cli import CLI\n')
    file.write('from mininet.log import setLogLevel, info, error\n')
    file.write('from mininet.net import Mininet\n')
    file.write('from mininet.link import Intf\n')
    file.write('from mininet.topo import Topo\n')
    file.write('from mininet.util import quietRun\n')
    file.write('from mininet.node import RemoteController\n')
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
    file.write(REMOTE_CONTROLLER_IP)
    file.write('\',port=int(\'')
    file.write(REMOTE_CONTROLLER_PORT)
    file.write('\') ) )\n')
    file.write('\n')
    file.write('    switch = net.switches[ 0 ]\n')
    file.write('    info( \'*** Adding hardware interface\', intfName, \'to switch\',\n')
    file.write('        switch.name, \'\\n\' )\n')
    file.write('    _intf = Intf( intfName, node=switch )\n')
    file.write('\n')
    file.write('    info( \'*** Note: you may need to reconfigure the interfaces for \'\n')
    file.write('          \'the Mininet hosts:\\n\', net.hosts, \'\\n\' )\n')
    file.write('\n')
    file.write('    net.start()\n')
    file.write('    CLI( net )\n')
    file.write('    net.stop()\n')


def generate_mininet_turn_on_script_auto(node_intf_map, node_groups, edge_groups, leaves, node_map):
    for group in node_groups.keys():
        node_IP = node_map.keys()[group]
        filename = 'turn_on_script_for_' + node_IP + '.py'
        filepath = SCRIPT_FOLDER + filename


        file = open(filepath, 'w')
        gen_turn_on_script_by_template(file, node_intf_map[node_IP],
                                       node_groups[group], edge_groups[group], leaves)
        file.close()



if __name__ == '__main__':
    generate_mininet_turn_on_script( '1.1.1.231', 'vlan17', 100 )


