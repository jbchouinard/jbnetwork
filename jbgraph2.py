"""
Tools for editing networks, and algorithms for computing their properties.

Classes:
Network  -- a network of nodes
RSTree  -- rooted spanning tree, created from a Network objects
NetworkFactory -- generate classic networks (star, clique, erdos-renyi, etc.)

Functions:

Written by me@jeromebchouinard.ca
"""
__all__ = ['Network']

class Network:
    """
    A network of nodes.

    Methods:
    add_node -- add node to the network
    add_link -- add link between two nodes

    Properties:
    nodes -- list of nodes in the network
    node_count -- number of nodes in the network
    link_count -- number of links in the network
    """
    def __init__(self, fromDict=None):
        """Create a network, optionally from a dictionary, else empty.

        Keyword arguments:
        fromDict -- dictionary from which to create the network

        Dictionary format: {node1:{node2:1, node3:1}}
        """manipulating
        if fromDict is None:
            self._net = {}
        else:
            self._net = fromDict

    def add_node(self, node):
        """Create a new (unconnected) node in the graph."""
        if node not in self._net:
            self._net[node] = {}

    def add_link(self, node1, node2):
        """Make a link between nodes.

        n1 and n2 are created if they did not already exist."""
        if not self.add_node(node1):
            return -1
        if not self.add_node(node2):
            return -1
        self._net[node1][node2] = 1
        self._net[node2][node1] = 1

    def del_link(self, node1, node2):
        """Delete link between nodes"""
        del self._net[node1][node2]
        del self._net[node2][node1]

    def find_neighbors(self, node):
        """Return list of neighbors of node."""
        return [neighbor for neighbor in self._net[node]]

    @property
    def link_count(self):
        """Number of links in the network."""
        return int(sum([sum(self._net[n].values()) for n in self._net]) / 2)

    @property
    def node_count(self):
        """Number of nodes in the network."""
        return len(self._net)

    @property
    def nodes(self):
        """Nodes in the network."""
        return [node for node in self._net]

    def compute_distances_to_node(self, node):
        pass

    def compute_node_centrality(self, node):
        pass

    def map_ac_naive(self, nodes='all'):
        pass

    def map_ac_split(self, nodes='all'):
        pass

    def compute_node_cc(self, node):
        pass

    def find_shortest_paths_to_node(self, node, algo="floyd-warshall"):
        pass

    def estimate_node_cc(self, node):
        pass

    def estimate_cc(self):
        pass