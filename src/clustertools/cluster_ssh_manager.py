from paramiko import *
from main     import logger_MininetCE



def open_ssh_to_nodes(node_map):
    '''Open SSH sessions to each node in cluster.

    Args:
        node_map: Cluster nodes map.

    Returns:
        SSH session to cluster node map.
        SSH session chan to cluster node map.
    '''
    ssh_map = {}
    ssh_chan_map = {}
    for node_IP in node_map.keys():
        ssh_map[node_IP] = SSHClient()
        ssh_map[node_IP].set_missing_host_key_policy(AutoAddPolicy())
        ssh_map[node_IP].connect(hostname=node_IP, username=node_map[node_IP], password=node_map[node_IP])
        ssh_chan_map[node_IP] = ssh_map[node_IP].invoke_shell()
        logger_MininetCE.info('opening SSH session to ' + str(node_IP))

    return ssh_map, ssh_chan_map


def close_ssh_to_nodes(ssh_map):
    '''Close SSH sessions to each node in cluster.

    Args:
        ssh_map: SSH session to cluster node map.
    '''
    for node_IP, ssh_session in ssh_map.items():
        ssh_session.close()
        # print('close SSH session to ' + str(node_IP))
        logger_MininetCE.info('close SSH session to ' + str(node_IP))
