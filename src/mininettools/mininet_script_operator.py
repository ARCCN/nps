import random

import networkx as nx

from src        import metis


def split_graph_on_parts(G, nodes):
    '''Split graph on subgraphs.

    Args:

    Returns:

    '''
    number_of_parts = len(nodes)
    if number_of_parts == 1:
        (edgecuts, parts) = metis.part_graph(G, number_of_parts, recursive=True)
    else:
        (edgecuts, parts) = metis.part_graph(G, number_of_parts, contig=True, compress=True)

    groups = {}
    for p in set(parts):
        group = {}
        group['vertexes'] = []
        group['edges'] = []
        groups[p] = group

    for i,p in enumerate(parts):
        groups[p]['vertexes'].append(i)

    special_group = {}
    special_group['vertexes'] = []
    special_group['edges'] = []
    groups['no_group'] = special_group

    for edge in G.edges():
        no_group_flag = True
        for id, group in groups.items():
            if (edge[0] in group['vertexes']) and (edge[1] in group['vertexes']):
                group['edges'].append(edge)
                no_group_flag = False
                break
        if no_group_flag:
            group = groups['no_group']
            group['edges'].append(edge)
            if edge[0] not in group['vertexes']:
                group['vertexes'].append(edge[0])
            if edge[1] not in group['vertexes']:
                group['vertexes'].append(edge[1])

    #delete not used nodes
    for key, node in nodes.items():
        if node['group'] not in set(parts):
            del nodes[key]

    return groups, nodes


def standard_mininet_script_parser(filename, G):
    ''' Parse standart Mininet sript.

    Args:
        filename: Mininet script file name.
        G: NetworkX graph.

    Returns:
        NetworksX graph with added according to Mininet scripts nodes (hosts and switches).
    '''
    mininet_sript = open(filename, 'r')
    lines = mininet_sript.readlines()
    ID_counter = 0
    string_name_to_ID_map = {}
    for line in lines:
        if 'self.addHost' in line:
            splitted_line = line.split()
            host_name = splitted_line[3].split("'")[1]
            host_id = splitted_line[0]
            string_name_to_ID_map[host_id] = ID_counter
            ID_counter += 1
            G.add_node(string_name_to_ID_map[host_id], type='host')
        if 'self.addSwitch' in line:
            splitted_line = line.split()
            switch_name = splitted_line[3].split("'")[1]
            switch_id = splitted_line[0]
            string_name_to_ID_map[switch_id] = ID_counter
            ID_counter += 1
            G.add_node(string_name_to_ID_map[switch_id], type='switch')
        if 'self.addLink' in line:
            link_elem_1 = line.split()[1][:-1]
            link_elem_2 = line.split()[2]
            G.add_edge(string_name_to_ID_map[link_elem_1],string_name_to_ID_map[link_elem_2])
    return G


def define_leaves_in_graph(G):
    '''Create list of leave-nodes in network graph.

    Args:
        G: NetworkX graph.

    Returns:
        List of leave-nodes.
    '''
    leaves = []
    for key,value in nx.degree(G).items():
        if value == 1:
            leaves.append(key)
    return leaves


def nodes_number_optimization(G, nodes):
    '''Optimaze the number of cluster nodes to operate with network graph.

    Args:
        G: NetworkX graph.
        node_map: Cluster nodes map.
        node_intf_map: External network interface name to cluster node map.

    Returns:
        New cluster nodes map.
        New external network interface name to cluster node map.
    '''
    new_nodes_num = len(nodes)
    while len(G.nodes())/new_nodes_num < 2.0:
        new_nodes_num -= 1
        key = random.choice(nodes.keys())
        del nodes[key]
    return nodes


if __name__ == '__main__':
   pass
