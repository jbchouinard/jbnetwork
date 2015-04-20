"""
Collection of useful algorithms for Udacity CS215

Functions:
partition
top_k
"""
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
