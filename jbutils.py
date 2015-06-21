"""
Various useful functions

Functions:
partition: partition a list around a given value
top_k: find the top k elements of a list
timeit: function decorator to print execution time of a function
profile: profile execution time for different input sizes
"""
import time
from pprint import pprint
import math


def partition(L, v):
    """
    Partition list L at value V.
    """
    left = []
    right = []
    for i in range(len(L)):
        if L[i] < v:
            left.append(L[i])
        elif L[i] > v:
            right.append(L[i])
    return (left, v, right)


def top_k(L, k):
    """
    Find the top k elements in list L.
    """
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
    """
    Modify a function to print cpu and wall-clock elapsed time when called.

    Can be used as a decorator:
    @timeit
    def func(x):
        ...
    """
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


def profile(func, input_gen, max_time=5, max_n=2**20, start_n=1, keep_returns=False):
    """
    Time a function for different input sizes and check if O(n^2), O(n), or O(log(n))
    """
    runtimes = []
    returns = [] if keep_returns else None
    last_runtime = 0
    n = start_n
    max_time_ms = max_time * 1000
    input_sizes = []

    while last_runtime <= max_time_ms and n <= max_n:
        inp = input_gen(n)
        start_time = time.process_time()
        rvalue = func(inp)
        end_time = time.process_time()
        last_runtime = end_time - start_time
        runtimes.append(last_runtime)
        input_sizes.append(n)
        if keep_returns:
            returns.append(rvalue)
        n *= 2

    lognfactors = []
    nfactors = []
    n2factors = []
    for i in range(1,len(runtimes)):
        lognfactors.append(runtimes[i]-runtimes[i-1])
        nfactors.append(runtimes[i]/runtimes[i-1])
        n2factors.append(math.sqrt(runtimes[i])/math.sqrt(runtimes[i-1]))

    print('If func is O(log(n)) these numbers should be the same:')
    pprint(lognfactors)
    print('\n')
    print('If func is O(n) these numbers should be the same:')
    pprint(nfactors)
    print('\n')
    print('If func is O(n^2) these numbers should be the same: ')
    pprint(n2factors)
    print('\n')

    return (input_sizes, runtimes, returns)