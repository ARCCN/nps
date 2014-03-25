from src.clustertools.cluster_mininet_cmd_manager  import send_mininet_cmd_to_cluster_node
from src.clustertools.cluster_support              import get_next_IP, get_next_IP_pool
from config.config_constants                       import FIRST_HOST_IP



def host_process_configurator_nodegroup(node, groups, CIDR_mask, leaves, hosts):
    '''Configurate hosts propcesses network interfaces in each nodegroup.

    Args:
        node_IP: IP address of node.
        node_groups: Group ID to Group node-list map.
        node_IP_gr_map: Node IP address to Group ID map.
        node_IP_pool_map: Cluster Node to pool of IP addresses map.
        CIDR_mask: CIRD mask of IP address for host network interface.
        leaves: List of leave-nodes in network graph.

    '''
    # curr_host = first_host
    first_host_ip = node['IP_pool']
    curr_host_ip = first_host_ip
    group = groups[node['group']]
    for vertex in group['vertexes']:
        if vertex in leaves:
            # reset config on host interface
            curr_host = 'h' + str(vertex)
            cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 0'
            send_mininet_cmd_to_cluster_node(node, cmd)
            # config new IP address on host interface
            cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 ' + curr_host_ip + '/' + CIDR_mask
            send_mininet_cmd_to_cluster_node(node, cmd)

            host = {}
            host['nodeIP'] = node['IP']
            host['name'] = curr_host
            host['IP'] = curr_host_ip
            hosts[curr_host] = host

            # prepare for next host
            curr_host_ip = get_next_IP(curr_host_ip)


def define_node_ip_pool(groups, leaves, nodes):
    '''Defines the cluster node pool based on number of hosts and switches on conctere cluster node.

    Args:

    Returns:
        Cluster Node IP address pool.
    '''

    next_IP_pool = FIRST_HOST_IP
    for node in nodes.values():
        group = groups[node['group']]
        host_num = len(group['vertexes'])
        for node_in_gr in group['vertexes']:
            if node_in_gr not in leaves:
                host_num -= 1
        node['IP_pool'] = next_IP_pool
        next_IP_pool = get_next_IP_pool(next_IP_pool, host_num) # make not execute on last iteration
    return nodes