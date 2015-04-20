"""
Tools for creating and editing networks, and algorithms for computing their properties.

Classes:
Network  -- a network of nodes
RSTree  -- rooted spanning tree, created from a Network objects
NetworkFactory -- generate classic networks (star, clique, erdos-renyi, etc.)
"""
__all__ = ['Network', 'RSTree']

import jbheap as jbh

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
    def __init__(self, from_dict=None):
        """Create a network, optionally from a dictionary, else empty.

        Keyword arguments:
        fromDict -- dictionary from which to create the network

        Dictionary format: {node1:{node2:1, node3:1}}
        """
        self._rstree = None
        if from_dict is None:
            self._net = {}
        else:
            self._net = from_dict

    def __len__(self):
        return self.node_count

    def add_node(self, node):
        """Create a new (unconnected) node in the graph."""
        if node not in self._net:
            self._net[node] = {}

    def add_link(self, node1, node2, weight=1):
        """Make a link between nodes.

        n1 and n2 are created if they did not already exist."""
        self.add_node(node1)
        self.add_node(node2)
        self._net[node1][node2] = weight
        self._net[node2][node1] = weight

    def del_link(self, node1, node2):
        """Delete link between nodes"""
        del self._net[node1][node2]
        del self._net[node2][node1]

    def del_node(self, node):
        """Delete node and all links to it."""
        del self._net[node]
        for node2 in self._net:
            if node in self._net[node2]:
                del self._net[node2][node]

    def link_weight(self, node1, node2):
        return self._net[node1][node2]

    def prune_network_random(self, prob):
        for node in self.nodes:
            if random.random() > prob:
                self.del_node(node)

    def prune_network(self, nodes_to_keep):
        for node in self.nodes:
            if not node in nodes_to_keep:
                self.del_node(node)
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

    @property
    def bridge_links(self):
        """Bridge links."""
        if self._rstree == None:
            self._rstree = RSTree(self, self.nodes[0])
        return self._rstree.bridge_links

    def map_distance_to_node(self, node):
        """Map the distance between node n and every reachable node in the graph."""
        open_list = [node]
        distance_from_start = {}
        distance_from_start[node] = 0
        while len(open_list) > 0:
            current = open_list[0]
            del open_list[0]
            for neighbor in self.find_neighbors(current):
                if neighbor not in distance_from_start:
                    distance_from_start[neighbor] = distance_from_start[current] + 1
                    open_list.append(neighbor)
        return distance_from_start

    def compute_node_centrality(self, node):
        """Return the average distance from node to all other reachable nodes."""
        distances = self.map_distance_to_node(node)
        return float(sum(distances.values())/len(distances))

    def map_ac(self, nodes='all'):
        """
        Map the average centrality of nodes in the graph.

        Keyword arguments:
        nodes -- (optional) list of nodes to map. By default, map all nodes.
        """
        if nodes == 'all':
            nodes = self.nodes()
            acmap = {}
            for node in nodes:
                acmap[node] = self.compute_node_centrality(node)
            return acmap

    def map_ac2(self):
        """
        Map average centrality using algorithm that splits the network at bridge edges.

        In practice appears to be slower than map_ac.
        Keyword arguments:
        nodes -- (optional) list of nodes to map. By default, map all nodes.
         """
        # pylint: disable=missing-docstring
        # pylint: disable=invalid-name
        def _merge_acmaps(acm, dm, r):
            acmap = {}
            wt = [len(m) for m in dm]

            for i, j in [(0, 1), (1, 0)]:
                for n in dm[i]:
                    acmap[n] = (acm[i][n]*wt[i] + (dm[i][n] + 1 + acm[j][r[j]]*wt[j])) / sum(wt)
            return acmap

        b_links = self.bridge_links
        for link in b_links:
            self.del_link(link[0], link[1])

        dmap0 = self.map_distance_to_node(b_links[0][0])
        reachable = [n for n in dmap0]
        acmap0 = self.map_ac(nodes=reachable)

        open_list = b_links
        while open_list != []:
            bridge = open_list.pop(0)
            if bridge[0] in acmap0:
                dmap0 = self.map_distance_to_node(bridge[0])
                dmap1 = self.map_distance_to_node(bridge[1])
                reach1 = [n for n in dmap1]
                acmap1 = self.map_ac(nodes=reach1)
                acmap0 = _merge_acmaps([acmap0, acmap1], [dmap0, dmap1], bridge)
                self.add_link(bridge[0], bridge[1])
            else:
                # If the bridge doesn't connect, flip it
                open_list.insert(len(open_list), (bridge[1], bridge[0]))
        return acmap0

    # pylint: disable=invalid-name
    def compute_node_cc(self, node):
        """Compute connectivity coefficient (cc) of node n.

        cc = 2 * nv / kv(kv-1)

        where
        kv = number of nodes neighboring n
        nv = number of links between neighbors of n
        """
        neighbors = self.find_neighbors(node)
        kv = len(neighbors)
        nv = 0

        if kv < 2:
            return 0

        for i in range(kv-1):
            for j in range(i+1, kv):
                if neighbors[j] in self.find_neighbors(neighbors[i]):
                    nv += 1

        return 2.0*nv/(kv*(kv+1))

    def map_weighted_distance_to_node(self, node):
        """
        Map shortest weighted paths to a node using Djikstra algorithm.

        Return a map of format {node: (shortest_path, number_of_hops)}.
        """
        dist_so_far = jbh.HeapOfTuples(1, elements=[(node, 0, 0)])
        final_dist = {}
        while len(dist_so_far) > 0:
            current, dist, hops = dist_so_far.pop()
            final_dist[current] = (dist, hops)

            for nbor in self.find_neighbors(current):
                if nbor not in final_dist:
                    dist_so_far_list = dist_so_far.list()
                    new_dist = final_dist[current][0] + self.link_weight(current, nbor)
                    new_hops = final_dist[current][1] + 1
                    try:
                        # This is relying on implementation details of
                        # jbheap - need to add interface to do this
                        i_x = [n[0] for n in dist_so_far_list].index(nbor)
                        if new_dist < dist_so_far_list[i_x][1]:
                            dist_so_far._heap[i_x] = (nbor, new_dist, new_hops)
                            dist_so_far._up_heapify(i_x)
                    except ValueError:
                        dist_so_far.insert((nbor, new_dist, new_hops))

        return final_dist

    # def map_weighted_distances(self):
    #     """
    #     Map shortest weighted paths between all pairs of nodes using Floyd-Warshall algorithm.
    #     """
    #     pass

    # def estimate_node_cc(self, node):
    #     pass

    # def estimate_cc(self):
    #     pass


# pylint: disable=too-many-instance-attributes
class RSTree:
    """ A rooted spanning tree, created from a Network object.

    Properties
    root
    network
    po_map
    desc_map
    max_po_map
    min_po_map
    bridge_links
    """
    def __init__(self, network, root):
        """ Create a rooted spanning tree from a Network object."""
        self.root = root
        self.network = network
        self._po_map = None
        self._max_po_map = None
        self._desc_map = None
        self._min_po_map = None
        self._bridge_links = None

        tree = {root:{}}
        marked = [root]
        open_list = [root]

        def add_link(node1, node2, color):
            """Add link to tree."""
            if not node1 in tree:
                tree[node1] = {}
            if not node2 in tree:
                tree[node2] = {}
            tree[node1][node2] = color
            if color == 'red':
                tree[node2][node1] = 'red'

        while open_list != []:
            current = open_list.pop(0)
            neighbors = network.find_neighbors(current)

            for neighbor in neighbors:
                if neighbor not in marked:
                    marked.append(neighbor)
                    open_list.append(neighbor)
                    add_link(current, neighbor, 'green')
                elif neighbor not in tree[current] and current not in tree[neighbor]:
                    add_link(current, neighbor, 'red')
        self._tree = tree

    @property
    def po_map(self):
        """Rank of nodes in post-order traversal"""
        if self._po_map is not None:
            return self._po_map

        _po_map = {}

        # pylint: disable=missing-docstring
        def _rec_post_order(current, k):
            linked = self._tree[current]
            children = [n for n in linked if linked[n] == 'green']
            for child in children:
                k = _rec_post_order(child, k)
            _po_map[current] = k
            return k+1

        _rec_post_order(self.root, 1)
        self._po_map = _po_map
        return _po_map

    @property
    def desc_map(self):
        """Map of number of descendants of each node in the tree."""
        if self._desc_map is not None:
            return self._desc_map

        _desc_map = {}

        # pylint: disable=missing-docstring
        def _how_many_below(current):
            linked = self._tree[current]
            children = [n for n in linked if linked[n] == 'green']

            descendants = 1
            for child in children:
                descendants += _how_many_below(child)
            _desc_map[current] = descendants
            return descendants

        _how_many_below(self.root)
        self._desc_map = _desc_map
        return _desc_map

    @property
    def max_po_map(self):
        """
        Map of highest (post-order) rank of any descendant, removed by up to 1 degree.

        Meaning, any rode reachable through tree edges and at most one
        non-tree edge.
        """
        if self._max_po_map is not None:
            return self._max_po_map

        _max_po_map = {}

        # pylint: disable=missing-docstring
        def _max_po_below(current, has_crossed_red):
            linked = self._tree[current]
            neighbors = [n for n in linked]

            max_po = self.po_map[current]
            for nbor in neighbors:
                if linked[nbor] == 'green':
                    max_po = max(max_po, _max_po_below(nbor, has_crossed_red))
                elif linked[nbor] == 'red' and not has_crossed_red:
                    max_po = max(max_po, _max_po_below(nbor, 1))

            # the same node may be visited more than once because
            # through different paths because of red links, so
            # need to do this
            if current in _max_po_map:
                _max_po_map[current] = max(_max_po_map[current], max_po)
            else:
                _max_po_map[current] = max_po

        _max_po_below(self.root, 0)
        self._max_po_map = _max_po_map
        return _max_po_map

    @property
    def min_po_map(self):
        """
        Map of lowerst (post-order) rank of any descendant, removed by up to 1 degree.

        Meaning, any rode reachable through tree edges and at most one
        non-tree edge.
        """
        if self._min_po_map is not None:
            return self._min_po_map

        _min_po_map = {}

        # pylint: disable=missing-docstring
        def _min_po_below(current, has_crossed_red):
            linked = self._tree[current]
            neighbors = [n for n in linked]

            min_po = self.po_map[current]
            for nbor in neighbors:
                if linked[nbor] == 'green':
                    min_po = min(min_po, _min_po_below(nbor, has_crossed_red))
                elif linked[nbor] == 'red' and not has_crossed_red:
                    min_po = min(min_po, _min_po_below(nbor, 1))

            # the same node may be visited more than once because
            # through different paths because of red links, so
            # need to do this
            if current in _min_po_map:
                _min_po_map[current] = min(_min_po_map[current], min_po)
            else:
                _min_po_map[current] = min_po

        _min_po_below(self.root, 0)
        self._min_po_map = _min_po_map
        return _min_po_map

    @property
    def bridge_links(self):
        """
        Bridge links in the graph as list of links.

        A link is a bridge link if it is the only link
        connecting two components of the network.
        """
        if self._bridge_links is not None:
            return self._bridge_links

        _bridge_links = []

        # pylint: disable=missing-docstring
        def _is_bridge_link(node1, node2):
            if not self._tree[node1][node2] == 'green':
                return False
            if not self.max_po_map[node2] <= self.po_map[node2]:
                return False
            if not self.min_po_map[node2] > (self.po_map[node2] - self.desc_map[node2]):
                return False
            return True

        for node in self._tree:
            for nbor in self._tree[node]:
                if _is_bridge_link(node, nbor):
                    _bridge_links.append((node, nbor))

        self._bridge_links = _bridge_links
        return _bridge_links
