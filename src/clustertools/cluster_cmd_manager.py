from paramiko                import *
#from main                    import logger_MininetCE
from config.config_constants import SRC_SCRIPT_FOLDER, DST_SCRIPT_FOLDER, MALWARE_MODE_ON, \
    DST_SCRIPT_FOLDER, MALWARE_CENTER_IP, MALWARE_CENTER_PORT, INFECTED_HOSTS_FILENAME


def send_script_to_cluster_node(node, script_filename):
    '''Send file with python script to cluster node.

    Args:
        node_IP: IP address of cluster node.
        script_filename: Name of script file. File on Cluster Manager machine and on cluster node
                         node machine will have the same name.
    '''
    # open SFTP session to node
    transport = Transport((node['IP'], 22))
    transport.connect(username=node['username'], password=node['username'])
    sftp = SFTPClient.from_transport(transport)

    # config script file paths
    src_script_filepath = SRC_SCRIPT_FOLDER + script_filename
    dst_script_filepath = DST_SCRIPT_FOLDER + script_filename

    # send script via SFTP
    sftp.put(src_script_filepath, dst_script_filepath)

    # close SFTP session to node
    sftp.close()
    transport.close()


def send_support_scripts_to_cluster_node(node):
    '''Send helpful scripts to cluster nodes.

    This scripts used in malware propagation experiment ONLY!

    Args:
        node_IP: IP address of cluster node.
    '''

    # delete old scripts
    del_old_support_scripts_cmd = 'rm ' + DST_SCRIPT_FOLDER + '*'
    send_cmd_to_cluster_node(node, del_old_support_scripts_cmd)

    script_name = 'turn_on_script_for_' + node['IP'] + '.py'
    send_turn_on_script_to_cluster_node(node, script_name)
    send_script_to_cluster_node(node, 'scapy_packet_gen.py')
    send_script_to_cluster_node(node, 'port_sniffer.py')
    send_script_to_cluster_node(node, 'file_monitor.py')
    send_script_to_cluster_node(node, 'worm_instance.py')



def send_turn_on_script_to_cluster_node(node, script_filename):
    '''Send start up script to cluster node.

    This script generated for each cluster node specially. The generation algorithm depends on mapping
    of simulated topology on cluster topology.

    Args:
        node_IP: IP address of cluster node.
        script_filename: Name of script file. File on Cluster Manager machine and on cluster node
                         node machine will have the same name.
    '''
    # open SFTP session to node
    transport = Transport((node['IP'], 22))
    transport.connect(username=node['username'], password=node['username'])
    sftp = SFTPClient.from_transport(transport)

    # config script file paths
    src_sricpt_filepath = SRC_SCRIPT_FOLDER + 'nodes/' + script_filename
    dst_script_filepath = DST_SCRIPT_FOLDER + script_filename

    # send script via SFTP
    sftp.put(src_sricpt_filepath, dst_script_filepath)

    # close SFTP session to node
    sftp.close()
    transport.close()


def send_cmd_to_cluster_node(node, cmd):
    '''Send console command to cluster node.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.
    '''
    cmd += '\n'
    node['ssh_chan'].send(cmd)
    if cmd != 'exit\n':
        buff = ''
        #endswith_str = 'root@' + CLUSTER_NODE_MACHINE_NAME + ':~# '
        endswith_str = 'root@' + node['hostname'] + ':~# '
        while not buff.endswith(endswith_str): # Need to change name, or use the variable.
            buff += node['ssh_chan'].recv(9999)
        #logger_MininetCE.info('SUCCESS:' + node_IP + ': ' + cmd)


def exec_start_up_script(node):
    '''Send the console command to cluster Node to execute the start up script.

    Args:
        node_IP: IP address of cluster node.
    '''

    reset_vs_db_cmd = 'ovs-vsctl list-br | xargs -L1 ovs-vsctl del-br'
    send_cmd_to_cluster_node(node, reset_vs_db_cmd)

    # Flush options on eth1 interface on nodes in cluster. This interface will be use for inter
    # Mininet instances communications
    reset_intf_cmd = 'ifconfig ' + node['out_intf'] + ' 0'
    send_cmd_to_cluster_node(node, reset_intf_cmd)

    split_IP = node['IP'].split('.')
    reset_vs_cmd = 'ovs-vsctl del-br s' + split_IP[3]
    send_cmd_to_cluster_node(node, reset_vs_cmd)

    clean_infected_hosts_file_cmd = '> ' + DST_SCRIPT_FOLDER + INFECTED_HOSTS_FILENAME
    send_cmd_to_cluster_node(node, clean_infected_hosts_file_cmd)

    # Turn On Mininet instance on nodes in cluster
    send_mn_turn_on_cmd_to_cluster_node(node)


def send_mn_turn_on_cmd_to_cluster_node(node):
    '''Send the console command to cluster node to start up the Mininet.

    Args:
        node_IP: IP address of cluster node.
    '''
    turn_on_mininet_script_name = 'turn_on_script_for_' + node['IP'] + '.py'
    cmd = 'python ' + DST_SCRIPT_FOLDER + turn_on_mininet_script_name
    cmd += '\n'
    node['ssh_chan'].send(cmd)
    buff = ""
    while not buff.endswith('mininet> '):
        buff += node['ssh_chan'].recv(9999)


