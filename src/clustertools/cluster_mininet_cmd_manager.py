from main import logger_MininetCE


def send_mininet_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map, quite=True):
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
        # print("SUCCESS:" + node_IP + ": " + cmd)
        if not quite:
            buff_lines = buff.splitlines()
            for line in buff_lines[:-1]:
                print(line)
        logger_MininetCE.info("SUCCESS:" + node_IP + ": " + cmd)


def send_mininet_ping_to_cluster_node(node_IP, cmd, ssh_chan_map):
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
