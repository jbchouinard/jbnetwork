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
    """This class represents a graph of labeled, attribute-less node

        ---Get methods
            getLinkCount
            getNodeCount
            getAsDict
            getDistToNode
            getNeighbors
            getCC
            getNodes

        ---Graph modification methods
            addNode
            addLink
            """

    def __init__(self, fromDict = None):
        if fromDict is None:
            self.__g = {}
        else:
            self.__g = fromDict

    def getAsDict(self):
        "Returns a dictionary representation of the graph structure."
        return self.__g

    def getLinkCount(self):
        "Returns the number of links (edges) in the graph."
        return int(sum([sum(self.__g[n].values()) for n in self.__g]) / 2)

    def getNodeCount(self):
        "Returns number of nodes (vertices) in the graph."
        return len(self.__g)

    def getNodes(self):
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

    def removeLink(self, n1, n2):
        "Remove link between n1 and n2."
        del self.__g[n1][n2]
        del self.__g[n2][n1]
    
    def getNodeCentrality(self, v):
        """Returns the average distance (shortest path) between
        node n and every reachable node (from n) in the graph."""
        distance_from_start = self.getDistanceToNode(v)
        return float(sum(distance_from_start.values()))/len(distance_from_start) 

    def getDistanceToNode(self, v):
        """Returns the distance (shortest path) between
        node n and every reachable node (from n) in the graph."""
        open_list = [v]
        distance_from_start = {}
        distance_from_start[v] = 0
        while len(open_list) > 0:
            current = open_list[0]
            del open_list[0]
            for neighbor in self.__g[current].keys():
                if neighbor not in distance_from_start:
                    distance_from_start[neighbor] = distance_from_start[current] + 1
                    open_list.append(neighbor)
        return distance_from_start  

    def getNodeClusteringCoefficient(self, n):
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

    def getNeighbors(self, n):
        "Returns list of neighbors of node n."
        try:
            neighbors = [nb for nb in self.__g[n]]
        except KeyError:
            neighbors = []
        return neighbors

    def getBridgeLinks(self, root):
        s = RSTree(self.__g, root)
        return s.getBridgeLinks()


class RSTree:
    """ For creation and study of rooted spanning trees.

    Must be created from a Graph object and cannot be modified. 

    Directed tree edges are labeled 'green'; non-directed non-tree
    edges are labeled 'red'."""

    def __init__(self, G, root):
        self.__root = root
        self.__POMap = None
        self.__highPOMap = None
        self.__descMap = None
        self.__lowPOMap = None
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
            neighbors = G.getNeighbors(current)

            for nb in neighbors:
                if nb not in marked:
                    marked.append(nb)
                    openList.append(nb)
                    addGreenLink(current, nb)
                elif nb not in S[current] and current not in S[nb]:
                    addRedLink(current, nb)
        self.__S = S

    def getAsDict(self):
        return self.__S

    def getPostOrder(self):
        '''Returns mapping of node to rank in post-order traversal.'''
        if self.__POMap is not None:
            return self.__POMap

        POMap = {}

        def recPostOrder(current, k):
            # visit childen from left to right
            # children are green-linked nodes that are not the parent
            linked = self.__S[current]
            children = [n for n in linked if linked[n] == 'green']
            for child in children:
                k = recPostOrder(child, k)
            POMap[current] = k
            return k+1

        recPostOrder(self.__root, 1)
        self.__POMap = POMap
        return POMap

    def getDescCount(self):
        "Return mapping of node to number of descendants (including itself)"
        if self.__descMap is not None:
            return self.__descMap

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

    def getLowPostOrder(self):
        """Returns mapping of node to the lowest post-order value below it
        (including itself; and one none-tree (red) edge can be traversed."""
        if self.__lowPOMap is not None:
            return self.__lowPOMap

        lowPOMap = {}

        def whatIsTheLowestPOBelow(current,redTraversed):
            links = self.__S[current]
            children = [n for n in self.__S[current]]
            lowestPO = self.getPostOrder()[current]

            for child in children:
                if links[child] == 'green':
                    lowestPO = min(lowestPO, whatIsTheLowestPOBelow(child, redTraversed))
                elif links[child] == 'red' and redTraversed == 0:
                    lowestPO = min(lowestPO, whatIsTheLowestPOBelow(child, 1))

            lowPOMap[current] = min(lowPOMap.get(current, lowestPO), lowestPO)
            return lowestPO

        whatIsTheLowestPOBelow(self.__root, 0)
        self.__lowPOMap = lowPOMap
        return lowPOMap

    def getHighPostOrder(self):
        """Returns mapping of node to the lowest post-order value below it,
        including itself; and one none-tree (red) edge can be traversed."""
        if self.__highPOMap is not None:
            return self.__highPOMap

        highPOMap = {}

        def whatIsTheHighestPOBelow(current,redTraversed):
            linked = self.__S[current]
            children = [n for n in linked]

            highestPO = self.getPostOrder()[current]
            for child in children:
                if linked[child] == 'green':
                    highestPO = max(highestPO, whatIsTheHighestPOBelow(child,redTraversed))
                elif linked[child] == 'red' and redTraversed == 0:
                    highestPO = max(highestPO, whatIsTheHighestPOBelow(child, 1))
            highPOMap[current] = max(highPOMap.get(current, highestPO), highestPO)
            return highestPO

        whatIsTheHighestPOBelow(self.__root, 0)
        self.__highPOMap = highPOMap
        return highPOMap

    def getBridgeLinks(self):
        """Returns bridge links in the graph as list of links"""
        bridgeLinks = []

        def isBridgeLink(n1, n2):
            if (self.__S[n1][n2] == 'green' and
                    self.getHighPostOrder()[n2] <= self.getPostOrder()[n2] and
                    self.getLowPostOrder()[n2] > (self.getPostOrder()[n2] - self.getDescCount()[n2])):
                return True
            else:
                return False

        for n1 in self.__S:
            for n2 in self.__S[n1]:
                if isBridgeLink(n1, n2):
                    bridgeLinks.append((n1, n2))

        return bridgeLinks

                
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
        constructors = { 'star': (self.__makeStarGraph, ('size',)),
            'clique': (self.__makeCliqueGraph, ('size',)),
            'random': (self.__makeRandomGraph, ('size','p')),
            'hypercube': (self.__makeHypercubeGraph, ('size',)),
            'ring': (self.__makeRingGraph, ('size',)),
            'chain': (self.__makeChainGraph, ('size',)),
            'grid': (self.__makeGridGraph, ('sizeX', 'sizeY')) }

        gtype = kwargs.get('gtype', self.__defaults['gtype'])
        args = [ kwargs.get(name, self.__defaults[name]) for name in constructors[gtype][1] ]
        func = constructors[gtype][0]

        return func(*args)

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

import math

def test_PO():
    g = GraphFactory().constructGraph(gtype='ring', size=10)
    s = RSTree(g, 0)
    pomap = s.getPostOrder()
    ndmap = s.getDescCount()
    lopomap = s.getLowPostOrder()
    hipomap = s.getHighPostOrder()
    blinks = s.getBridgeLinks()
    return pomap, ndmap, lopomap, hipomap, blinks

def test_GF():
    sizeXs = [8, 16, 32, 64]
    sizeYs = sizeXs
    sizes = [n*n for n in sizeXs]
    ps = [(1/(len(sizes)))*n for n in range(len(sizes))]
    gtypes = [ 'random', 'star' , 'clique', 'ring', 'chain', 'grid', 'hypercube' ]
    lens = []
    print(sizes)

    for gtype in gtypes:
        for i in range(len(sizes)):
            g = GraphFactory().constructGraph(gtype=gtype, 
                size=sizes[i],
                sizeX=sizeXs[i],
                sizeY=sizeYs[i],
                p=ps[i])

            #g.getDistToNode()
            g.getCC(0)
            g.getNeighbors(0)
            lens.append((sizes[i], len(g.getAsDict())))
    return lens

def test_BL():
    g = GraphFactory().constructGraph(gtype='ring', size=10)
    s = RSTree(g, 0)
    print(s.getBridgeLinks() == [])

    links = [(0,1),(0,2),(2,3),(1,3),(3,4),(4,6),(4,5),(5,6)]

    g = Graph()
    for link in links:
        g.addLink(*link)

    s = RSTree(g, 0)
    print(s.getBridgeLinks() == [(3,4)])

    g = GraphFactory().constructGraph(gtype="chain", size=4)
    s = RSTree(g,0)
    print(s.getBridgeLinks() == [(0,1),(1,2),(2,3)])

    g = GraphFactory().constructGraph(gtype="clique", size=10)
    s = RSTree(g,0)
    print(s.getBridgeLinks() == [])