from constants import epsilon
from collections.abc import Iterable

def helper(node, nfa,  visited, symbols):
    res = set([node])
    visited.add(node)
    # if given state doesn't have any epsilon transitions then return that state
    if (node not in nfa.delta) or ((len(symbols) <= 1) and (epsilon in symbols)  and (epsilon not in nfa.delta[node])):
        return res
    
    for sym in symbols:
        if isinstance(nfa.delta[node][sym], Iterable):
            for i in nfa.delta[node][sym]:
                if i not in visited:
                    res = res.union(nfa.state_closure(i, symbols))
        else:
            if nfa.delta[node][sym] not in visited:
                res = res.union(nfa.state_closure(nfa.delta[node][sym], symbols))

    return res

def DFS(nfa, s, symbols):
    visited = set()
    return helper(s, nfa, visited, symbols)

def BFS(nfa, s, symbols):
    # visited = set()
    # return helper(k, nfa, visited, symbols)
    res = set()
    s = list(s)[0]
    visited = [False] * (len(nfa.Q))
 
    # Create a queue for BFS
    queue = []
 
    # Mark the source node as
    # visited and enqueue it
    queue.append(s)
    visited[s] = True
    while queue:
        # Dequeue a vertex from
        # queue and print it
        s = queue.pop(0)
 
        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for sym in symbols:
            for i in nfa.delta[s][sym]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
    for i in range(len(nfa.Q)):
        if visited[i]:
            res.add(i)
    return res
