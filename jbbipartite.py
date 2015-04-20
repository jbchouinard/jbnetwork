import csv

import jbnetwork as jbnet


def build_bp_network_from_csv(csvfn, delim=','):
    """
    Build a bipartite network from a csv file.
    """
    net = jbnet.Network()

    with open(csvfn, 'r') as csvf:
        rdr = csv.reader(csvf, delimiter=delim)

        nodes_left = []
        nodes_right = []
        for row in rdr:
            node1 = row[0]
            node2 = row[1]
            net.add_link(node1, node2)
            nodes_left.append(node1)
            nodes_right.append(node2)

    return (net, set(nodes_left), set(nodes_right))


def map_bp_str_of_connection(net, inter_nodes):
    """
    Compute the strength of connection between nodes in a bipartite network.

    Where the strength of connection is the number of paths of length 2 
    between two nodes.
    """
    str_of_connection = {}

    def strengthen_connection(n1, n2):
        for (v1, v2) in ((n1, n2), (n2, n1)):
            if not v2 in str_of_connection:
                str_of_connection[v2] = {}
            if not v1 in str_of_connection[v2]:
                str_of_connection[v2][v1] = 1
            else:
                str_of_connection[v2][v1] += 1

    for i_node in inter_nodes:
        nbors = net.find_neighbors(i_node)
        for i in range(len(nbors)-1):
            for j in range(i+1, len(nbors)):
                strengthen_connection(nbors[i], nbors[j])
    
    return str_of_connection


def map_bp_strongest_connections(str_of_connection):
    map_strongest = []

    for node in str_of_connection:
        strongest = max(str_of_connection[node], key=lambda k: str_of_connection[node][k])
        conn = str_of_connection[node][strongest]
        map_strongest.append((node, strongest, conn))

    return map_strongestdef find_diff_paths(network, nodes_to_check):
    # Find # of nodes for which the shortest weighted path
    # is not the same as the shortest path by number of hops
    diffpaths = 0

    for node in nodes_to_check:
        wt_dist_map = network.map_weighted_distance_to_node(node)
        nonwt_dist_map = network.map_distance_to_node(node)
        for linked_node in wt_dist_map:
            hops = nonwt_dist_map[linked_node]
            wt_hops = wt_dist_map[linked_node][1]
            if wt_hops != hops:
                if linked_node in nodes_to_check:
                    diffpaths += 0.5
                else:
                    diffpaths += 1.0

    return diffpaths
