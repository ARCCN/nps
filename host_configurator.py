from cluster_mininet_cmd_manager import send_mininet_cmd_to_cluster_node
from cluster_support import randomize_infected, get_next_IP
from main import MALWARE_PROPAGATION_MODE, MALWARE_INIT_INF_PROB
from Malware_Propagation_Director import malware_list_semaphore

# def host_process_configurator(node_IP, first_host, first_host_ip, CIDR_mask, hosts_number):
#     curr_host = first_host
#     curr_host_ip = first_host_ip
#     for i in xrange(hosts_number):
#         # reset config on host interface
#         cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 0'
#         send_mininet_cmd_to_cluster_node(node_IP, cmd)
#         # config new IP address on host interface
#         cmd = curr_host + ' ifconfig ' + curr_host + '-eth0 ' + curr_host_ip + '/' + CIDR_mask
#         send_mininet_cmd_to_cluster_node(node_IP, cmd)
#         host_to_node_map[curr_host_ip] = node_IP
#         host_map[curr_host_ip] = curr_host
#         if MALWARE_PROPAGATION_MODE:
#             malware_list_semaphore.acquire()
#             malware_director.add_malware_node(curr_host_ip, node_IP, True, randomize_infected(MALWARE_INIT_INF_PROB))
#             malware_list_semaphore.release()
#         # prepare for next host
#         curr_host    = get_next_host_name(curr_host)
#         curr_host_ip = get_next_IP(curr_host_ip)


def host_process_configurator_nodegroup(node_IP, node_group, first_host_ip, CIDR_mask, leaves, host_to_node_map, host_map, ssh_chan_map):
    # curr_host = first_host
    curr_host_ip = first_host_ip
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
            if MALWARE_PROPAGATION_MODE:
                malware_list_semaphore.acquire()
                malware_director.add_malware_node(curr_host_ip, node_IP, True, randomize_infected(MALWARE_INIT_INF_PROB))
                malware_list_semaphore.release()
            # prepare for next host
            curr_host_ip = get_next_IP(curr_host_ip)