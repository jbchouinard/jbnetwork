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

class Graph:
    """This class represents a graph of labeled, attribute-less nodes
    and has two categories of methods: methods to modify the graph,
    and methods to get useful properties of the graph.

        ---Get methods
            getLinkCount
            getNodeCound
            getGraphAsDict
            getDistToNode
            getConnectivityCoefficient

        ---Graph methods
            makeNode
            makeLink"""
    def __init__(self):
        self.__g = {}

    def getAsDict(self):
        "Returns a dictionary representation of the graph structure."
        return self.__g

    def getLinkCount(self):
        "Returns the number of links (edges) in the graph."
        return int(sum([sum(self.__g[n].values()) for n in self.__g]) / 2)

    def getNodeCount(self):
        "Returns number of nodes (vertices) in the graph."
        return len(self.__g)

    def addNode(self, n):
        "Create a new (unconnected) node in the graph."
        if n not in self.__g:
            self.__g[n] = {}
        return 1

    def addLink(self, n1, n2):
        """Make a link between nodes n1 and n2. n1 and n2 are
        created if they did not already exist."""
        if (not self.makeNode(n1)):
            return -1
        if (not self.makeNode(n2)):
            return -1
        self.__g[n1][n2] = 1
        self.__g[n2][n1] = 1
        return 1
    
    def getDistToNode(self, n):
        """Returns a dictionary of the distance (shortest path) between
        node n and every reachable node (from n) in the graph."""
        currentDistance = 0
        shortestPaths = {n:0}
        currentlyVisiting = [n]

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

    def getConnectivityCoefficient(self, n):
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

    def findBridgeLinks(self):
        bridgeLinks = {}
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
        random

        ---Usage
        starGraphMaker = GraphFactory(gType = 'star', size = 10)

        Make a star graph with 10 nodes:
         starGraphMaker.constructGraph()

        Make a star graph with 20 nodes:
         starGraphMaker.constructGraph(size = 20)

        randomGraphMaker = GraphFactory(gType = 'random', size = 100, p = 0.3)

        Make a random graph with p = 0.3, 100 nodes
        (each pair of nodes has 30% of being linked)
          randomGraphMaker.constructGraph()

        Change defaults:
         randomGraphMaker.setDefaults(size = 200, p = 0.5)

        Make a randomgraph with 200 nodes, p = 0.5
         randomGraphMaker.constructGraph()

        Changing default graph type (misleading var name is misleading):
         randomGraphMaker.setDefaults(gType = 'clique')

        Size of hypercube is rounded down to nearest power of 2
         hyperMaker = GraphFactory(gType = 'hypercube', size = 64)
         graph = hyperMaker.constructGraph()
         graph.getNodeCount() 
            64

         graph = hyperMaker.constructGraph(size = 100)
         graph.getNodeCount()
            64
    """
    __validSettings = [ 'gType', 'size', 'p' ]

    __validGTypes = [ 'star', 'clique', 'random', 'ring', 'chain' ]
    
    def __init__(self, size = None, gType = None, p = None):
        self.__defaults = { 'gType': gType,
                            'size': size,
                            'p': p }

    def __checkSetting(self, name, value):
        if name == 'gType':
            if value in self.__validGTypes: return 1
            else: raise ValueError('invalid gType value')

        elif name == 'size':
            if type(value) is not int: raise TypeError('size must be an int')
            else: return 1

        elif name == 'p':
            if not 0 < value < 1: raise ValueError('invalid p value')
            else: return 1
            
        else: raise ValueError('Setting', name, 'does not exist.')

    def constructGraph(self, **kwargs):
        """This method constructs a Graph object of the type and
        size specified by the Factory settings (all defaults can
        be overriden by keyword arguments.

        See help(GraphFactory) for usage examples.
        """
        for kw in kwargs:
            self.__checkSetting(kw, kwargs[kw])

        args = {}

        for setting in self.__validSettings:
            if setting in kwargs:
                args[setting] = kwargs[setting]
            else:
                args[setting] = self.__defaults[setting]


        if args['gType'] == 'star': return self.__makeStarGraph(args['size'])
        elif args['gType'] == 'clique': return self.__makeCliqueGraph(args['size'])
        elif args['gType'] == 'random': return self.__makeRandomGraph(args['size'], args['p'])
        elif args['gType'] == 'hypercube': return self.__makeHypercubeGraph(args['size'])
        elif args['gType'] == 'ring': return self.__makeRingGraph(args['size'])
        elif args['gType'] == 'chain': return self.__makeChainGraph(args['size'])

        return -1

    def setDefaults(self, **kwargs):
        """Change settings of default graph produced by constructGraph.

        Usage: graphFactoryInstance.setDefaults(setting = value, setting = value...)"""
        for kw in kwargs:
            try:
                if(self.__checkSetting(kw, kwargs[kw])):
                    self.__defaults[kw] = kwargs[kw]
                    return 1
            except NameError:
                print('Valid settings are: ', self.__validSettings)
                return 0

    @staticmethod
    def __makeStarGraph(size):
        g = Graph()
        for i in range(1, size):
            g.makeLink(0, i)
        return g

    @staticmethod
    def __makeChainGraph(size):
        g = Graph()
        for i in range(size-1):
            g.makeLink(i, i+1)
        return g

    @staticmethod
    def __makeRingGraph(size):
        g = self.__makeChainGraph(size)
        g.makeLink(0, size)
        return g

    @staticmethod
    def __makeRandomGraph(size, p):
        g = Graph()
        for i in range(size-1):
            for j in range(i+1, size):
                if random.random() < p:
                    g.makeLink(i, j)
        return g

    @staticmethod
    def __makeCliqueGraph(size):
        g = Graph()
        for i in range(size-1):
            for j in range(i+1, size):
                g.makeLink(i, j)
        return g

    #TODO
    @staticmethod
    def __makeHypercubeGraph(size):
        return Graph()

    @staticmethod
    def __makeGridGraph(size):
        return Graph()
