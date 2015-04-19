"""
Collection of useful algorithms for Udacity CS215

Functions:
build_graph
partition
top_k
"""
def build_graph(tsvfn):
    g = jb.Graph()

    rdr = csv.reader(open(tsvfn, 'r'), delimiter='\t')

    heroes = []
    books = []
    for row in rdr:
        n1 = row[0]
        n2 = row[1]
        g.addLink(n1, n2)
        books.append(n2)

    return (g, set(books))


def partition(L, v):
    left = []
    right = []
    for i in range(len(L)):
        if L[i] < v:
            left.append(L[i])
        elif L[i] > v:
            right.append(L[i])
    return (left, v, right)


def top_k(L, k):
    i = int(random.random() * len(L))
    (left, v, right) = partition(L, L[i])
    
    if len(left) == k:
        return left
    if len(left) == k-1:
        return left + [v]
    if len(left) < k:
        return left + [v] + top_k(right, k - (len(left) + 1))
    else:
        return top_k(left, k)


class Heap:
    def __init__(self, elements=None, is_heap=False):
        self._heap = []

        if elements is not None:
            if is_heap:
                self._heap = elements[:]

            else:
                for el in elements:
                    self.insert(el)

    def insert(self, element):
        self._heap.append(element)
        self.up_heapify(len(self._heap)-1)

    def index(self, element):
        return self._heap.index(element)

    def pop(self):
        if len(self._heap) == 1:
            return self._heap.pop()
        elif len(self._heap) == 0:
            return None
        else:
            val = self._heap[0]
            self._heap[0] = self._heap.pop()
            self.down_heapify(0)
            return val

    def up_heapify(self, i):
        L = self._heap
        parent = self.parent
        is_less_than = self.is_less_than

        while i > 0:
            try:
                if is_less_than(L[i],  L[parent(i)]):
                    L[i], L[parent(i)] = L[parent(i)], L[i]
                    i = parent(i)
                else:
                    break
            except IndexError:
                break
        return

    def down_heapify(self, i):
        L = self._heap
        left_child = self.left_child
        right_child = self.right_child
        is_less_than = self.is_less_than

        while i < len(L) - 1:
            try:
                if is_less_than(L[left_child(i)], L[i]):
                    L[i], L[left_child(i)] = L[left_child(i)], L[i]
                    i = left_child(i)
                elif i < len(L) - 2 and is_less_than(L[right_child(i)], L[i]):
                    L[i], L[right_child(i)] = L[right_child(i)], L[i]
                    i = right_child(i)
                else:
                    break
            except IndexError:
                break
        return

    def is_less_than(self, el1, el2):
        return el1 < el2

    @staticmethod
    def parent(i): 
        return (i-1)//2

    @staticmethod
    def left_child(i): 
        return 2*i+1

    @staticmethod
    def right_child(i): 
        return 2*i+2

    @staticmethod
    def is_leaf(i): 
        return (2*i+2 >= len(L)) and (2*i+1 >= len(L))

    @staticmethod
    def one_child(i): 
        return (2*i+1 < len(L)) and (2*i+2 >= len(L))


class HeapOfTuples(Heap):
    def __init__(self, i_val, elements=None, is_heap=False):
        self.i_val = i_val
        super().__init__(elements=elements, is_heap=is_heap)

    def is_less_than(self, el1, el2):
        return el1[self.i_val] < el2[self.i_val]


def test1():
    heap = Heap(elements=[1,5,21,41,213,41,52,2,1,414])
    print(heap._heap)
    print(heap.pop())
    print(heap._heap)
    heap.insert(88)
    print(heap._heap)


def test2():
    theap = HeapOfTuples(0, elements=zip(range(10), 'a'*10))
    print(theap._heap)
    theap.insert((5, 'a'))
    print(theap.pop())