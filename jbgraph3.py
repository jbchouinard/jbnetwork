"""
This module implements a Graph class, and a GraphFactory class,
which can construct a few types of classic graphs.

This was done mostly as a way to try my hand at OOP.

The goal being to write a Graph object that hides the implementation.
In this case, the implementation of the graph structure being a
dictionary of nodes.

Eventually the module will implement most of the concepts covered in Udacity's 
Intro to Algorithms (CS215) online course.

me@jeromebchouinard.ca
"""
import sys
import random

class Graph:
    """This class represents a graph of labeled, attribute-less nodes
    and has three categories of methods: methods to modify the graph,
    get methods to access attributes, and methods (algorithms) to compute 
    interesting properties of the graph.

        ---Get methods
            getLinkCount
            getNodeCount
            asDict

        ---Graph modification methods
            addNode
            addLink

        ---Graph algorithms
            findDistanceToNode
            findNeighbors
            computeConnectivityCoefficient"""

    def __init__(self, fromDict = None):
        if fromDict is None:
            self.__g = {}
        else:
            self.__g = fromDict

    def asDict(self):
        "Returns a dictionary representation of the graph structure."
        return self.__g

    def getLinkCount(self):
        "Returns the number of links (edges) in the graph."
        return int(sum([sum(self.__g[n].values()) for n in self.__g]) / 2)

    def getNodeCount(self):
        "Returns number of nodes (vertices) in the graph."
        return len(self.__g)

    def listNodes(self):
        "Returns a list of all nodes"
        return [n for n in g]

    def addNode(self, n):
        "Create a new (unconnected) node in the graph."
        if n not in self.__g:
            self.__g[n] = {}
        return 1

    def addLink(self, n1, n2):
        """Make a link between nodes n1 and n2. n1 and n2 are
        created if they did not already exist."""
        if (not self.addNode(n1)):
            return -1
        if (not self.addNode(n2)):
            return -1
        self.__g[n1][n2] = 1
        self.__g[n2][n1] = 1
        return 1
    
    def findDistToNode(self, n):
        """Returns a dictionary of the distance (shortest path) between
        node n and every reachable node (from n) in the graph."""
        currentDistance = 0
        shortestPaths = {n:0}
        currentlyVisiting = [n]

        # TODO: this function is super slow
        # Pretty sure there is a faster way to do this
        def findNewNeighbors(nodes):
            newNeighbors = []
            for n in nodes:
                try:
                    for nb in self.__g[n]:
                        if nb not in shortestPaths:
                            newNeighbors.append(nb)
                except KeyError:
                    raise ValueError('Node ' + str(n) + ' does not exist.')
            return newNeighbors

        while (currentlyVisiting != []):
            newNeighbors = findNewNeighbors(currentlyVisiting)

            for nb in newNeighbors:
                shortestPaths[nb] = currentDistance + 1

            currentlyVisiting = newNeighbors
            currentDistance += 1

        return shortestPaths

    def computeConnectivityCoefficient(self, n):
        """Returns connectivity coefficient (cc) of node n.

        cc = 2 * nv / kv(kv-1)

        where
        kv = number of nodes neighboring n
        nv = number of links between neighbors of n

        """
        try:
            neighbors = [i for i in self.__g[n]]
        except KeyError:
            raise ValueError('Node ' +str(n) + ' does not exist.')
        nv = 0
        for n1 in neighbors:
            for n2 in neighbors[neighbors.index(n1)+1:]:
                if n2 in self.__g[n1]:
                    nv+=1
        kv = len(neighbors)

        if kv > 1: return 2.0 * nv / (kv * (kv-1))
        else: return 0

    def findNeighbors(self, n):
        "Returns list of neighbors of node n."
        try:
            neighbors = [nb for nb in self.__g[n]]
        except KeyError:
            neighbors = []
        return neighbors

    def findBridgeLinks(self, root):
        s = RSTree(self.__g, root)
        return s.findBridgeLinks()


class RSTree:
    """ For creation and study of rooted spanning trees.

    Must be created from a Graph object and cannot be modified. 

    Directed tree edges are labeled 'green'; non-directed non-tree
    edges are labeled 'red'."""

    def __init__(self, G, root):
        self.__root = root
        S = {root:{}}
        marked = [root]
        openList = [root]

        def addGreenLink(n1, n2):
            if not n1 in S:
                S[n1] = {}
            if not n2 in S:
                S[n2] = {}
            S[n1][n2] = 'green'

        def addRedLink(n1, n2):
            if not n1 in S:
                S[n1] = {}
            if not n2 in S:
                S[n2] = {}
            S[n1][n2] = 'red'
            S[n2][n1] = 'red'

        while (openList != []):
            current = openList.pop(0)
            neighbors = G.findNeighbors(current)

            for nb in neighbors:
                if nb not in marked:
                    marked.append(nb)
                    openList.append(nb)
                    addGreenLink(current, nb)
                elif nb not in S[current] and current not in S[nb]:
                    addRedLink(current, nb)
        self.__S = S

    def asDict(self):
        return self.__S

    def postOrder(self):
        '''Returns mapping of node to rank in post-order traversal.'''
        POMap = {}

        def recPostOrder(current, n):
            # visit childen from left to right
            # children are green-linked nodes that are not the parent
            linked = self.__S[current]
            children = [n for n in linked if linked[n] == 'green']
            for child in children:
                n = recPostOrder(child, n)
            POMap[current] = n
            return n+1

        recPostOrder(self.__root, 1)
        self.__POMap = POMap
        return POMap

    def numberOfDescendants(self):
        "Return mapping of node to number of descendants (including itself)"
        descMap = {}

        def howManyAreYouBelow(current):
            linked = self.__S[current]
            children = [n for n in linked if linked[n] == 'green']

            n = 1
            for child in children:
                n = n + howManyAreYouBelow(child)
            descMap[current] = n
            return n

        howManyAreYouBelow(self.__root)
        self.__descMap = descMap
        return descMap

    def lowestPostOrder(self):
        """Returns mapping of node to the lowest post-order value below it
        (including itself; and one none-tree (red) edge can be traversed."""
        lowPOMap = {}

        def whatIsTheLowestPOBelow(current,redTraversed):
            links = self.__S[current]
            children = [n for n in self.__S[current]]
            lowestPO = self.__POMap[current]

            for child in children:
                if links[child] == 'green':
                    lowestPO = min(lowestPO, whatIsTheLowestPOBelow(child, redTraversed))
                elif links[child] == 'red' and redTraversed == 0:
                    lowestPO = min(lowestPO, whatIsTheLowestPOBelow(child, 1))

            lowPOMap[current] = lowestPO
            return lowestPO

        whatIsTheLowestPOBelow(self.__root, 0)
        self.__lowPOMap = lowPOMap
        return lowPOMap

    def highestPostOrder(self):
        """Returns mapping of node to the lowest post-order value below it,
        including itself; and one none-tree (red) edge can be traversed."""
        highPOMap = {}

        def whatIsTheHighestPOBelow(current,redTraversed):
            linked = self.__S[current]
            children = [n for n in linked]

            highestPO = self.__POMap[current]

            for child in children:
                if linked[child] == 'green':
                    highestPO = max(highestPO, whatIsTheHighestPOBelow(child,redTraversed))
                elif linked[child] == 'red' and redTraversed == 0:
                    highestPO = max(highestPO, whatIsTheHighestPOBelow(child, 1))

            highPOMap[current] = highestPO
            return highestPO

        whatIsTheHighestPOBelow(self.__root, 0)
        self.__highPOMap = highPOMap
        return highPOMap

    def findBridgeLinks(self):
        """Returns bridge links in the graph as list of links"""
        if not hasattr(self, __POMap):
            self.postOrder()
        if not hasattr(self, __descMap):
            self.numberOfDescendants()
        if not hasattr(self, __lowPOMap):
            self.lowestPostOrder()
        if not hasattr(self, __highPOMap):
            self.highestPostOrder()

        bridgeLinks = []

        

        return brigdeLinks

                
class GraphFactory():
    """
    This class is used to construct a number of different types of graphs.

    The constructGraph method does the work here, it constructs a graph
    based on the defaults of the instance, optionally overriden by
    arguments passed to constructGraph.

    This is maybe useful if you need to generate a lot of graphs for testing purposes.
    Or something.

        ---Types of graph
        star
        clique
        chain
        ring
        hypercube
        grid
        random (Erdos-Renyi)

        ---Usage
        starGraphMaker = GraphFactory(gtype = 'star', size = 10)

        Make a star graph with 10 nodes:
         starGraphMaker.constructGraph()

        Make a star graph with 20 nodes:
         starGraphMaker.constructGraph(size = 20)

        randomGraphMaker = GraphFactory(gtype = 'random', size = 100, p = 0.3)

        Change defaults:
         randomGraphMaker.setDefaults(size = 200, p = 0.5)

        Size of hypercube is rounded down to nearest power of 2
         hyperMaker = GraphFactory(gtype = 'hypercube', size = 64)
         graph = hyperMaker.constructGraph()
         graph.getNodeCount() 
            64

    """
    __validSettings = [ 'gtype', 'size', 'p', 'sizeX', 'sizeY' ]

    __validGTypes = [ 'star', 'clique', 'random', 'ring', 'chain', 'grid', 'hypercube' ]
    
    def __init__(self, size = None, gtype = None, p = None, sizeX = None, sizeY = None):
        self.__defaults = { 'gtype': gtype,
                            'size': size,
                            'p': p,
                            'sizeX': sizeX,
                            'sizeY': sizeY }

    def constructGraph(self, **kwargs):
        """This method constructs a Graph object of the type and
        size specified by the Factory settings (all defaults can
        be overriden by keyword arguments.

        See help(GraphFactory) for usage examples.
        """
        args = {}

        for setting in self.__validSettings:
            if setting in kwargs:
                args[setting] = kwargs[setting]
            else:
                args[setting] = self.__defaults[setting]

        if args['gtype'] == 'star': return self.__makeStarGraph(args['size'])
        elif args['gtype'] == 'clique': return self.__makeCliqueGraph(args['size'])
        elif args['gtype'] == 'random': return self.__makeRandomGraph(args['size'], args['p'])
        elif args['gtype'] == 'hypercube': return self.__makeHypercubeGraph(args['size'])
        elif args['gtype'] == 'ring': return self.__makeRingGraph(args['size'])
        elif args['gtype'] == 'chain': return self.__makeChainGraph(args['size'])
        elif args['gtype'] == 'grid': return self.__makeGridGraph(args['sizeX'], args['sizeY'])
        
        raise ValueError('Invalid graph type.')

    def setDefaults(self, **kwargs):
        """Change settings of default graph produced by constructGraph.

        Usage: graphFactoryInstance.setDefaults(setting = value, setting = value...)"""
        for kw in kwargs:
            if kw in self.__validSettings:
                self.__defaults[kw] = kwargs[kw]

    @staticmethod
    def __makeStarGraph(size):
        g = Graph()
        for i in range(1, size):
            g.addLink(0, i)
        return g

    @staticmethod
    def __makeChainGraph(size):
        g = Graph()
        for i in range(size-1):
            g.addLink(i, i+1)
        return g

    @staticmethod
    def __makeRingGraph(size):
        g = Graph()
        for i in range(size-1):
            g.addLink(i, i+1)
        g.addLink(0, size-1)
        return g

    @staticmethod
    def __makeRandomGraph(size, p):
        g = Graph()
        for i in range(size):
            g.addNode(i)
        for i in range(size-1):
            for j in range(i+1, size):
                if random.random() < p:
                    g.addLink(i, j)
        return g

    @staticmethod
    def __makeCliqueGraph(size):
        g = Graph()
        for i in range(size-1):
            for j in range(i+1, size):
                g.addLink(i, j)
        return g

    @staticmethod
    def __makeHypercubeGraph(size):
        def recMakeHG(n):
            if n == 1:
                return {0:{}}

            m = int(n/2)
            g = {}
            g1 = recMakeHG(m)

            for node1 in g1:
                g[node1] = g1[node1]
                g[node1 + m] = {}
                for node2 in g1[node1]:
                    g[node1 + m][node2 + m] = 1

                g[node1][node1 + m] = 1
                g[node1 + m][node1] = 1
            return g

        # Find largest power of 2 < size
        n = 1
        while(n <= size):
            n = n*2
        n = n/2

        g = recMakeHG(n)
        return Graph(fromDict = g)

    @staticmethod
    def __makeGridGraph(sizeX, sizeY):
        g = Graph()
        for n in range(sizeX * sizeY):
            if ((n+1) % sizeX != 0):
                g.addLink(n, n+1)
            if (n < (sizeY - 1)*sizeX):
                g.addLink(n, n+sizeX)
        return g


def test_PO():
    g = GraphFactory().constructGraph(gtype='ring', size=10)
    s = RSTree(g, 0)
    pomap = s.postOrder(0)
    ndmap = s.numberOfDescendants(0)
    lopomap = s.lowestPostOrder(0, pomap)
    hipomap = s.highestPostOrder(0, pomap)


def test_GF():
    sizeXs = [4, 8, 16, 32, 64, 128]
    sizeYs = sizeXs
    sizes = [n*n for n in sizeXs]
    ps = [0, 0.5, 1]
    gtypes = [ 'random', 'star' , 'clique', 'ring', 'chain', 'grid', 'hypercube' ]

    lens = []

    for gtype in gtypes:
        for i in range(len(sizes)):
            g = GraphFactory().constructGraph(gtype = gtype, 
                                            size = sizes[i],
                                            sizeX = sizeXs[i],
                                            sizeY = sizeYs[i],
                                            p = ps[i])
            

            #g.findDistToNode(0)
            g.computeConnectivityCoefficient(0)
            g.findNeighbors(0)

            lens.append((sizes[i], len(g.asDict())))

    return lens