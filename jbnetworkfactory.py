"""
Functions for generating several types of classic networks.

Functions:
build_star_network
build_chain_network
build_ring_network
build_random_network
build_clique_network
build_hypercube_network
build_grid_network
"""
def build_star_network(size):
    """Build a star network. Returns Network object."""
    network = Network()
    for i in range(1, size):
        network.add_link(0, i)
    return network


def build_chain_network(size):
    """Build a chain network. Returns Network object."""
    network = Network()
    for i in range(size-1):
        network.add_link(i, i+1)
    return network


def build_ring_network(size):
    """Build a ring network. Returns Network object."""
    network = Network()
    for i in range(size-1):
        network.add_link(i, i+1)
    network.add_link(0, size-1)
    return network


def build_random_network(size, prob):
    """Build a random (Erdos-Renyi) network. Returns Network object."""
    network = Network()
    for i in range(size):
        network.add_node(i)
    for i in range(size-1):
        for j in range(i+1, size):
            if random.random() < prob:
                network.add_link(i, j)
    return network


def build_clique_network(size):
    """Build a clique network. Returns Network object."""
    network = Network()
    for i in range(size-1):
        for j in range(i+1, size):
            network.add_link(i, j)
    return network


def build_hypercube_network(size):
    """Build a hypercube network. Returns Network object."""
    # pylint: disable=missing-docstring
    def _rec_build_hc_net(size):
        if size == 1:
            return {0:{}}

        network = {}
        network1 = _rec_build_hc_net(size/2)

        for node1 in network1:
            network[node1] = network1[node1]
            network[node1 + size/2] = {}
            for node2 in network1[node1]:
                network[node1 + size/2][node2 + size/2] = 1

            network[node1][node1 + size/2] = 1
            network[node1 + size/2][node1] = 1
        return network

    # Find largest power of 2 <= size
    pow2size = 2**int(math.log(size, 2))

    network = _rec_build_hc_net(pow2size)
    return Network(from_dict=network)


def build_grid_network(dim):
    """Build a grid network. Returns Network object.

    arguments
    dim -- (x, y) tuple of dimensions
    """
    network = Network()
    for node in range(size[0] * size[1]):
        if (node+1) % size[0] != 0:
            network.add_link(node, node+1)
        if node < (size[1] - 1)*size[0]:
            network.add_link(node, node+size[0])
    return network