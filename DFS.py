from constants import epsilon

def BFS(nfa, s, symbols):
    res = set()
    # s = list(s)[0]
    visited = [False] * (len(nfa.Q))
 
    # Create a queue for BFS
    queue = []
 
    # Mark the source node as
    # visited and enqueue it
    for i in s:
        queue.append(i)
        visited[i] = True
    while queue:
        # Dequeue a vertex from
        # queue and print it
        s = queue.pop()
 
        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        if s not in nfa.delta:
            continue
        for sym in symbols:
            if sym not in nfa.delta[s]:
                continue
            for i in nfa.delta[s][sym]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
    for i in range(len(nfa.Q)):
        if visited[i]:
            res.add(i)
    return res
