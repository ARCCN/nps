import random

import networkx as nx

from src import metis


def split_graph_on_parts(G, number_pf_parts):
    if number_pf_parts == 1:
        (edgecuts, parts) = metis.part_graph(G, number_pf_parts, recursive=True)
    else:
        (edgecuts, parts) = metis.part_graph(G, number_pf_parts, contig=True, compress=True)

    node_groups = {}
    for p in parts:
        node_groups[p] = []
    for i,p in enumerate(parts):
        node_groups[p].append(i)

    edge_groups = {}
    for p in parts:
        edge_groups[p] = []
    edge_groups['no_group'] = []
    node_ext_intf_group = []
    for edge in G.edges():
        in_one_group_flag = False
        for group in node_groups.keys():
            if (edge[0] in node_groups[group]) and (edge[1] in node_groups[group]):
                in_one_group_flag = True
                break
        if in_one_group_flag:
            edge_groups[group].append(edge)
        else:
            edge_groups['no_group'].append(edge)
            if edge[0] not in node_ext_intf_group:
                node_ext_intf_group.append(edge[0])
            if edge[1] not in node_ext_intf_group:
                node_ext_intf_group.append(edge[1])
    return node_groups, edge_groups, node_ext_intf_group

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

def custom_mininet_script_parser(filename, G):
    mininet_sript = open(filename, 'r')
    lines = mininet_sript.readlines()
    for i, line in enumerate(lines):
        if 'class Topology' in line:

            if lines[i+1][0] in [' ', '\t', '\n']:
                print(lines[i+1][0])


def define_leaves_in_graph(G):
    leaves = []
    for key,value in nx.degree(G).items():
        if value == 1:
            leaves.append(key)
    return leaves


def nodes_number_optimization(G, node_map, node_intf_map):
    new_nodes_num = len(node_map)
    while len(G.nodes())/new_nodes_num < 2.0:
        new_nodes_num -= 1
        key = random.choice(node_map.keys())
        del node_map[key]
        del node_intf_map[key]
    return node_map, node_intf_map


if __name__ == '__main__':
    print('HELLO!\n')
    G = nx.Graph()



    G = nx.barabasi_albert_graph(17, 1, 777)
    pos = nx.spring_layout(G)

    leaves = define_leaves_in_graph(G)
    node_groups, edge_groups, node_ext_intf_group = split_graph_on_parts(G, 2)

    # generate_mininet_turn_on_script_auto("eth0", node_groups, edge_groups, leaves)

    draw_graph(G, node_groups, edge_groups)
