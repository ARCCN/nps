#from main import logger_MininetCE
import sys


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
        #while not buff.endswith('mininet> '):
        #    buff += ssh_chan_map[node_IP].recv(9999)
        ## print("SUCCESS:" + node_IP + ": " + cmd)
        ##    print buff
        #if not quite:
        #    buff_lines = buff.splitlines()
        #    for line in buff_lines[:-1]:
        #        print(line)

        last = ""
        while not buff.endswith('mininet> '):
            out = ssh_chan_map[node_IP].recv(1)
            if out:
                if out == '\n' and last != '\n': # remove duplication end of line
                    pass
                elif not quite:
                    sys.stdout.write(out)
            buff += out
            last = out
        # print("SUCCESS:" + node_IP + ": " + cmd)
        #    print buff

        #logger_MininetCE.info("SUCCESS:" + node_IP + ": " + cmd)


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
    #while not buff.endswith('mininet> '):
    #    if ssh_chan_map[node_IP].recv_ready():
    #        buff += ssh_chan_map[node_IP].recv(9999)
    #buff_lines = buff.splitlines()
    #for line in buff_lines[:-1]:
    #    print(line)
    last = ""
    while not buff.endswith('mininet> '):
        out = ssh_chan_map[node_IP].recv(1)
        if out:
            if out == '\n' and last != '\n': # remove duplication end of line
                pass
            else:
                sys.stdout.write(out)
        buff += out
        last = out

def test_delay_between_mn_hosts(node_IP, src_host_IP, dst_host_IP, threshold, ssh_chan_map):
    '''Send Mininet console command to test delay between hosts and compare to threshold.

    Args:
        node_IP: IP address of cluster node.
        src_host_IP: IP address of source host.
        dst_host_IP: IP address of destination host.
        threshold: Needed threshold of link delay.

    Returns:
        True: If link delay less then threshold.
        False: Of link delay overcome the threshold.
    '''
    pass
