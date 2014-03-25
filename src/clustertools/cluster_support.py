from random      import randint
from src.KThread import KThread

import networkx  as nx


def read_nodelist_from_file(nodelist_filepath):
    '''Read list of cluster nodes from file.

    Args:
        nodelist_file: Name of file with list of cluster nodes.
    '''
    nodes = {}

    # open nodelist file
    nodelist_file = open(nodelist_filepath, 'r')
    file_lines = nodelist_file.readlines()
    for i, file_line in enumerate(file_lines):
        splitted_line = file_line.split(' ')

        node = {}
        node['IP'] = splitted_line[0]
        node['hostname'] = splitted_line[1] # node_mname_map
        node['username'] = splitted_line[2] # node_map
        node['out_intf'] = splitted_line[3] # node_intf_map
        node['controller'] = (splitted_line[4], splitted_line[5][:-1]) # node_ctrl_map
        node['group'] = i # node_IP_gr_map
        node['IP_pool'] = None # node_IP_pool_map
        node['ssh'] = None
        node['ssh_chan'] = None
        nodes[splitted_line[0]] = node

    return nodes


def get_next_IP(IP):
    '''Generate next IP address. The next IP address is the incrementation (+1) of current IP address.

    Args:
        IP: The current IP address.

    Returns:
        The next incremented IP address. The input and output IP addresses are strings.

    '''
    octets = IP.split('.')
    if int(octets[3]) + 1 >= 255:
        next_IP = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + 1) + '.' + '1'
    else:
        next_IP = octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + str(int(octets[3]) + 1)
    return next_IP


def get_next_IP_pool(IP, hosts_number):
    '''Generate the first IP address on next IP address pool. Depends on IP address pool size.

    Args:
        IP: The first address of current pool.
        hosts_number: The size of current pool.

    Returns:
        The first IP address of the next pool. The input and output IP addresses are strings.
    '''
    octets = IP.split('.')
    if int(octets[3]) + hosts_number >= 255:
        new_oct = divmod(int(octets[3]) + hosts_number, 255)
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2]) + int(new_oct[0])) \
                       + '.' + str(int(new_oct[1]) + int(new_oct[0]))
    else:
        next_IP_pool = octets[0] + '.' + octets[1] + '.' + str(int(octets[2])) \
                       + '.' + str(int(octets[3]) + hosts_number)
    return next_IP_pool


def get_next_host_name(host):
    '''Generate the next host name in Mininet network. he next host name is the incremention (+1)
        of current host name.

    Args:
        host: The current host name.

    Returns:
        The next host incremented name.
    '''
    next_nost = 'h' + str(int(host[1:]) + 1)
    return next_nost


def get_random_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    '''
    IP = str(randint(1,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255)) + '.' + str(randint(0,255))
    return IP


def get_random_test_IP():
    '''Generated random IP address.

    Returns:
        The random IP address.
    In this test function is a smaller pool of possible IP addresses. Used for experiments with malware
    propagation.
    '''
    IP = str(randint(1,1)) + '.' + str(randint(1,2)) + '.' + str(randint(1,254)) + '.' + str(randint(1,254))
    return IP


def randomize_infected(prob):
    '''Make decision of host infection, depends on infection probability.

    Args:
        prob: Host infection probability.

    Returns:
        True: If the host is infected.
        False: If the host is NOT infected.
    '''
    r = randint(1,100)
    if r <= prob:
        return True
    else:
        return False


def make_threaded(function, args, nodes):
    '''Launch fuction in threads. Number of thread equal to number of cluster nodes.

    Args:
        function: Threaded function.
        args: Threaded function arguments.
        node_map: Cluster nodes map.
    '''
    threads = []
    list_args = list(args)
    for node in nodes.values():
        list_args.insert(0, node)
        thread = KThread(target=function, args=tuple(list_args))
        threads.append(thread)
        list_args.pop(0)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def get_networkX_graph(graph_data):
    '''Generate networkX graph from json string.

    Args:
        graph_data: Json string, that describes graph.

    Returns:
        NetworkX graph.
    '''
    G = nx.Graph()
    pos = {}
    for edge in graph_data['edges']:
        if int(edge[0]) not in G.nodes():
            #G.add_node(node_counter)
            #node_num_map[edge[0]] = node_counter
            #pos[node_counter] = [graph_data['pos'][edge[0]][0], 0 - graph_data['pos'][edge[0]][1]]
            G.add_node(int(edge[0]))
            pos[int(edge[0])] = [graph_data['pos'][edge[0]][0], 0 - graph_data['pos'][edge[0]][1]]
        if int(edge[1]) not in G.nodes():
            #G.add_node(node_counter)
            #node_num_map[edge[1]] = node_counter
            #pos[node_counter] = [graph_data['pos'][edge[1]][0], 0 - graph_data['pos'][edge[1]][1]]
            G.add_node(int(edge[1]))
            pos[int(edge[1])] = [graph_data['pos'][edge[1]][0], 0 - graph_data['pos'][edge[1]][1]]
        G.add_edge(int(edge[0]), int(edge[1]))
    return G, pos, graph_data['netapps']

