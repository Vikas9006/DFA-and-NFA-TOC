def find(x, parent):
    if x != parent[x]:
        parent[x] = find(parent[x], parent)
    return parent[x]

def union(x, y, parent, rank):
    x = find(parent[x], parent)
    y = find(parent[y], parent)
    if rank[x] < rank[y]:
        parent[x] = y
    elif rank[x] > rank[y]:
        parent[y] = x
    else:
        parent[y] = x
    return

def dsu(n, pairsUnion):
    parent = list()
    rank = list()
    for i in range(n):
        parent.append(i)
        rank.append(0)

    for (x, y) in pairsUnion:
        union(x, y, parent, rank)

    for i in range(n):
        find(i, parent)
    return parent

def renumber(parent, unMarkedStates):
    res = dict()
    for i in range(len(parent)):
        if i in unMarkedStates:
            if parent[i] == i:
                res[i] = len(res)
    return res
    
"""
0   N   Y
1   Y
2
"""