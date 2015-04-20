"""
A heap.

Classes:
Heap
HeapOfTuples
"""
class Heap:
    """
    Methods:
    insert
    pop
    index
    list
    check_heap_property
    is_less_than
    """
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
        self._up_heapify(len(self._heap)-1)

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
            self._down_heapify(0)
            return val

    def __len__(self):
        return len(self._heap)

    def list(self):
        return self._heap

    def _up_heapify(self, i):
        L = self._heap
        parent = self._parent
        is_less_than = self.is_less_than

        while i > 0:
            if is_less_than(L[i],  L[parent(i)]):
                L[i], L[parent(i)] = L[parent(i)], L[i]
                i = parent(i)
            else:
                break
        return

    def _down_heapify(self, i):
        L = self._heap
        lchild = self._left_child
        rchild = self._right_child
        is_less_than = self.is_less_than
        one_child = self._one_child
        is_leaf = self._is_leaf

        while i < len(L)-1:
            if is_leaf(i):
                break
            else:
                if one_child(i):
                    if is_less_than(L[lchild(i)], L[i]):
                        L[i], L[lchild(i)] = L[lchild(i)], L[i]
                    break
                else:
                    # Find smallest child
                    if is_less_than(L[rchild(i)], L[lchild(i)]):
                        i_child = rchild(i)
                    else:
                        i_child = lchild(i)

                    # If the smallest child is smaller, swap
                    if is_less_than(L[i_child], L[i]):
                        L[i], L[i_child] = L[i_child], L[i]
                        i = i_child
                    else:
                        break

    def is_less_than(self, el1, el2):
        return el1 < el2

    @staticmethod
    def _parent(i): 
        return (i-1)//2

    @staticmethod
    def _left_child(i): 
        return 2*i+1

    @staticmethod
    def _right_child(i): 
        return 2*i+2

    def _is_leaf(self, i): 
        return (2*i+2 >= len(self._heap)) and (2*i+1 >= len(self._heap))

    def _one_child(self, i): 
        return (2*i+1 < len(self._heap)) and (2*i+2 >= len(self._heap))



class HeapOfTuples(Heap):
    """
    A heap of tuples.

    Methods inherited from Heap:
    insert
    pop
    index
    list
    check_heap_property

    Extended methods:
    __init__

    Overriden methods:
    is_less_than
    """
    def __init__(self, i_val, elements=None, is_heap=False):
        """
        Arguments
        i_val -- the position (index) of the element of the tuple to compare
        elements -- list of elements to add to the heap
        is_heap -- set to True is elements is already a heap
        """
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


if __name__ == "__main__":
    test1()
    test2()