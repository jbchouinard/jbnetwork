"""
Various useful functions

Functions:
partition
top_k
timeit
"""
import time

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

def timeit(f):
    def g(*args, **kwargs):
        start_etime = time.perf_counter()
        start_cputime = time.process_time()
        rvalue = f(*args, **kwargs)
        end_etime = time.perf_counter()
        end_cputime = time.process_time()
        print('elapsed time (s): ', end_etime - start_etime)
        print('cpu time (s)', end_cputime - start_cputime)
        return rvalue
    return g