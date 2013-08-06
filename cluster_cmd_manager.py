from paramiko import *
from main import logger_MininetCE, SRC_SCRIPT_FOLDER, DST_SCRIPT_FOLDER, CLUSTER_NODE_MACHINE_NAME


def send_script_to_cluster_node(node_IP, script_filename, node_map):
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

def send_support_scripts_to_cluster_node(node_IP, node_map):
    '''Send helpful scripts to cluster nodes.

    This scripts used in malware propagation experiment ONLY!

    Args:
        node_IP: IP address of cluster node.
    '''
    script_name = 'turn_on_script_for_' + str(node_IP) + '.py'
    send_turn_on_script_to_cluster_node(node_IP, script_name, node_map)
    send_script_to_cluster_node(node_IP, 'scapy_packet_gen.py', node_map)
    send_script_to_cluster_node(node_IP, 'port_sniffer.py', node_map)

def send_turn_on_script_to_cluster_node(node_IP, script_filename, node_map):
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

def send_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map):
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

def exec_start_up_script(node_IP, node_intf_map, ssh_chan_map):
    '''Send the console command to cluster Node to execute the start up script.

    Args:
        node_IP: IP address of cluster node.
    '''
    # Flush options on eth1 interface on nodes in cluster. This interface will be use for inter
    # Mininet instances communications
    reset_intf_cmd = 'ifconfig ' + node_intf_map[node_IP] + ' 0'
    send_cmd_to_cluster_node(node_IP, reset_intf_cmd, ssh_chan_map)

    split_IP = node_IP.split('.')
    reset_vs_cmd = 'ovs-vsctl del-br s' + split_IP[3]
    send_cmd_to_cluster_node(node_IP, reset_vs_cmd, ssh_chan_map)

    # Turn On Mininet instance on nodes in cluster
    send_mn_turn_on_cmd_to_cluster_node(node_IP, ssh_chan_map)


def send_mn_turn_on_cmd_to_cluster_node(node_IP, ssh_chan_map):
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
