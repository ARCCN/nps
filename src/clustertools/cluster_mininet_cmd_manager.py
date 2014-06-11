#from main import logger_MininetCE
import sys


def send_mininet_cmd_to_cluster_node(node, cmd, quite=True):
    '''Send Mininet console command to cluster node.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.
    '''

    cmd += '\n'
    node['ssh_chan'].send(cmd)
    buff = ""
    if cmd != 'exit\n':
        last = ""
        while not buff.endswith('mininet> '):
            out = node['ssh_chan'].recv(1)
            if out:
                if out == '\n' and last == '\n': # remove duplication end of line
                    pass
                elif not quite:
                    sys.stdout.write(out)
            buff += out
            last = out


def send_mininet_ping_to_cluster_node(node, cmd):
    '''Send Mininet console command PING to cluster node and check the result of its execution.

    Args:
        node_IP: IP address of cluster node.
        cmd: Console command scripts.

    Returns:
        True: If the ping reached the destination point successfully.
        False: If the ping failed to reach the destination point.
    '''
    cmd += '\n'
    node['ssh_chan'].send(cmd)
    buff = ''
    last = ""
    while not buff.endswith('mininet> '):
        out = node['ssh_chan'].recv(1)
        if out:
            if out == '\n' and last == '\n': # remove duplication end of line
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
