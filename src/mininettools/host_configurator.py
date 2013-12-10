from src.clustertools.cluster_mininet_cmd_manager  import send_mininet_cmd_to_cluster_node
from src.clustertools.cluster_support              import randomize_infected, get_next_IP, get_next_IP_pool
from config.config_constants                       import MALWARE_PROPAGATION_MODE, MALWARE_INIT_INF_PROB, FIRST_HOST_IP
from src.malwaretools.Malware_Propagation_Director import malware_list_semaphore



def host_process_configurator_nodegroup(node_IP, node_groups, node_IP_gr_map, node_IP_pool_map, CIDR_mask, leaves,
                                        host_to_node_map, host_map, host_IP_map, ssh_chan_map):
    '''Configurate hosts propcesses network interfaces in each nodegroup.

    Args:
        node_IP: IP address of node.
        node_groups: Group ID to Group node-list map.
        node_IP_gr_map: Node IP address to Group ID map.
        node_IP_pool_map: Cluster Node to pool of IP addresses map.
        CIDR_mask: CIRD mask of IP address for host network interface.
        leaves: List of leave-nodes in network graph.
        host_to_node_map: Host IP to node IP map.
        host_map: Host IP to host name map.
        host_IP_map: Host name to host IP map.
        ssh_chan_map: SSH session chan to cluster node map.
    '''
    # curr_host = first_host
    first_host_ip = node_IP_pool_map[node_IP]
    curr_host_ip = first_host_ip
    node_group = node_groups[node_IP_gr_map[node_IP]]
    for node in node_group:
        if node in leaves:
            # reset config on host interface
            curr_host = 'h' + str(node)
            cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 0'
            send_mininet_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map)
            # config new IP address on host interface
            cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 ' + curr_host_ip + '/' + CIDR_mask
            send_mininet_cmd_to_cluster_node(node_IP, cmd, ssh_chan_map)
            host_to_node_map[curr_host_ip] = node_IP
            host_map[curr_host_ip] = curr_host
            host_IP_map[curr_host] = curr_host_ip
            if MALWARE_PROPAGATION_MODE:
                malware_list_semaphore.acquire()
                malware_director.add_malware_node(curr_host_ip, node_IP, True,
                                                  randomize_infected(MALWARE_INIT_INF_PROB))
                malware_list_semaphore.release()
            # prepare for next host
            curr_host_ip = get_next_IP(curr_host_ip)



def define_node_ip_pool(node_groups, leaves, node_map):
    '''Defines the cluster node pool based on number of hosts and switches on conctere cluster node.

    Args:
        node_groups: Group ID to node-list map.
        node_IP_gr_map: Node IP address to group ID map.
        leaves: List of leave-nodes in network graph.
        node_map: Cluster node map.

    Returns:
        Cluster Node IP address pool.
    '''
    node_IP_gr_map = {}
    for gr_number in node_groups.keys():
        node_IP_gr_map[node_map.keys()[gr_number]] = gr_number

    node_IP_pool_map = {}
    next_IP_pool = FIRST_HOST_IP
    for node_IP in node_map.keys():
        host_num = len(node_groups[node_IP_gr_map[node_IP]])
        for node in node_groups[node_IP_gr_map[node_IP]]:
            if node not in leaves:
                host_num -= 1
        node_IP_pool_map[node_IP] = next_IP_pool
        next_IP_pool = get_next_IP_pool(next_IP_pool, host_num) # make not execute on last iteration
    return node_IP_pool_map, node_IP_gr_map