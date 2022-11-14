from Tree import Node
from parser import parser
from DFS import DFS, BFS
from constants import epsilon
from DSU import dsu, renumber, find

class NFA:
    def __init__(self, Q, sigma, delta, S, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.S = S
        self.F = F

    def __str__(self):
        return "NFA = (" + "\n" + \
         "Q = " + str(self.Q) + "\n" + \
            "Σ = " + str(self.sigma) + "\n" + \
            "Δ = " + str(self.delta) + "\n" + \
            "S = " + str(self.S) + "\n" + \
            "F = " + str(self.F) + "\n" + \
            ")" + "\n"

    def renumber(self, k):
        newQ = set()
        newDelta = dict()
        newS = set()
        newF = set()

        for i in self.Q:
            newQ.add(i + k)
        for i in self.S:
            newS.add(i + k)
        for i in self.F:
            newF.add(i + k)

        for curr in self.delta:
            newDelta[curr + k] = dict()
            for sym in self.delta[curr]:
                newDelta[curr + k][sym] = set()
                for nxt in self.delta[curr][sym]:
                    newDelta[curr + k][sym].add(nxt + k)

        return NFA(newQ, self.sigma, newDelta, newS, newF)

    # Step 1a
    # Function gives a NFA which only accepts the given string
    @staticmethod
    def string_to_NFA(s):
        nfa = NFA(set(), set(s), dict(), set([0]), set())

        # Intially, there will be only one state in NFA
        nfa.Q.add(0)

        # For each character add a new state and make transtitions
        for i, j in enumerate(s):
            nfa.Q.add(i + 1)
            nfa.delta[i] = dict()
            nfa.delta[i][j] = set([i + 1])

        # Final states will be last state which was added (i.e. corresponding to end of string)
        nfa.F = set([len(s)])
        return nfa

    @staticmethod
    def exp_to_NFA(exp):
        # if expression is symbol (base case)
        nfa = NFA(set(), set(), dict(), set(), set())
        if exp.data == "symbol":
            nfa = NFA.string_to_NFA(exp.left.data)

        elif exp.data == "concat":
            lnfa = NFA.exp_to_NFA(exp.left)
            rnfa = NFA.exp_to_NFA(exp.right)

            # Re-numbering states of second NFA
            rnfa = rnfa.renumber(len(lnfa.Q))
        
            # Make epsilon transitions
            for final1 in lnfa.F:
                if final1 not in lnfa.delta:
                    lnfa.delta[final1] = dict()
                if epsilon not in lnfa.delta[final1]:
                    lnfa.delta[final1][epsilon] = set()
                lnfa.delta[final1][epsilon] = lnfa.delta[final1][epsilon].union(rnfa.S)

            # Remove final states of first NFA
            lnfa.F.clear()

            # Remove start state of second NFA
            rnfa.S.clear()
        
            # merge these two NFA and get bigger NFA
            nfa.Q = lnfa.Q.union(rnfa.Q)
            nfa.sigma = lnfa.sigma.union(rnfa.sigma)
            nfa.delta = lnfa.delta | rnfa.delta
            nfa.S = lnfa.S.union(rnfa.S)
            nfa.F = lnfa.F.union(rnfa.F)

        elif exp.data == "union":
            lnfa = NFA.exp_to_NFA(exp.left)
            rnfa = NFA.exp_to_NFA(exp.right)

            nfa.Q = set([0])
            # Re-numbering states of second NFA
            lnfa = lnfa.renumber(1)
            rnfa = rnfa.renumber(len(lnfa.Q) + 1)

            # Make epsilon transitions
            nfa.delta[0] = dict()
            nfa.delta[0][epsilon] = lnfa.S.union(rnfa.S)

            # Remove start states of NFA1 and NFA2
            lnfa.S.clear()
            rnfa.S.clear()

            # merge these two NFA and get bigger NFA
            nfa.Q = nfa.Q.union(lnfa.Q.union(rnfa.Q))
            nfa.sigma = lnfa.sigma.union(rnfa.sigma)
            nfa.delta = nfa.delta | lnfa.delta | rnfa.delta
            nfa.S = set([0])
            nfa.F = lnfa.F.union(rnfa.F)

        elif exp.data == "star":
            lnfa = NFA.exp_to_NFA(exp.left)

            nfa.Q = set([0])
            lnfa = lnfa.renumber(1)

            # Make epsilon transitions from start state to start states of NFA1
            nfa.delta[0] = dict()
            nfa.delta[0][epsilon] = set()
            nfa.delta[0][epsilon] = nfa.delta[0][epsilon].union(lnfa.S)

            # Make epsilon transitions from final states of NFA1 to start states of NFA1
            for final in lnfa.F:
                if final not in dict():
                    lnfa.delta[final] = dict()
                if epsilon not in dict():
                    lnfa.delta[final][epsilon] = set()
                lnfa.delta[final][epsilon] = (lnfa.delta[final][epsilon]).union(lnfa.S)
            
            # Remove start states of NFA1 and NFA2
            lnfa.S.clear()

            # Merge
            nfa.Q = nfa.Q.union(lnfa.Q)
            nfa.sigma = lnfa.sigma
            nfa.delta = nfa.delta | lnfa.delta
            nfa.S = set([0])
            nfa.F = lnfa.F.union(set([0]))
        return nfa

    def state_closure(self, k, symbols):
        return DFS(self, k, symbols)

    def getDFA(self):
        dfa = DFA(set(), set(), dict(), None, set())
        newQ = set()
        newDelta = dict()
        newS = set()
        newF = set()
        # States Defined
        for i in range(1 << len(self.Q)):
                newQ.add(i)

        # define delta
        for i in range(1 << len(self.Q)):
            newDelta[i] = dict()
            for sym in self.sigma:
                reachable = set()
                reach_states = 0
                for j in range(i.bit_length()):
                    if (i & (1 << j)) != 0 and (j in self.delta) and (sym in self.delta[j]):
                        for k in self.delta[j][sym]:
                            reachable = self.state_closure(k, set([epsilon]))

                        for k in reachable:
                            reach_states = reach_states | (1 << k)
                newDelta[i][sym] = set([reach_states])

        # define s
        newS = 0
        for i in self.S:
            reachable = self.state_closure(i, set([epsilon]))
            for j in reachable:
                newS = newS | (1 << j)
        

        # define F
        for i in range(len(newQ)):
            states = set()
            for j in range(i.bit_length()):
                if (i & (1 << j)) != 0:
                    states.add(j)
            if len(states.intersection(self.F)):
                newF.add(i)
        return DFA(newQ, self.sigma, newDelta, set([newS]), newF)

class DFA(NFA):
    def belongs(self, s):
        q = list(self.S)[0]
        for i in s:
            q = list(self.delta[q][i])[0]
        return q in self.F

    def funDelta(self, q, a):
        if (q in self.delta) and (a in self.delta[q]):
            return self.delta[q][a]
        return None

    def minimize(self):
        newQ = set()
        newDelta = dict()
        newF = set()
        marked = set()
        unMarkd = set()
        reachable = BFS(self, self.S, self.sigma)
        while True:
            isMarked = False
            for i in range(len(self.Q)):
                if i not in reachable:
                    continue
                for j in range(i + 1, len(self.Q)):
                    if j not in reachable:
                        continue
                    if (i, j) in marked:
                        continue
                    for sym in self.sigma:
                        nexti = list(self.funDelta(i, sym))[0]
                        nextj = list(self.funDelta(j, sym))[0]
                        if (i in self.F and j not in self.F) or (i not in self.F and j in self.F) or ((nexti, nextj) in marked):
                            marked.add((i, j))
                            isMarked = True

            # No marked occured in current round
            if not isMarked:
                break
        for i in range(len(self.Q)):
            for j in range(i + 1, len(self.Q)):
                if (i in reachable) and (j in reachable) and ((i, j) not in marked):
                    unMarkd.add((i, j))
        parent = dsu(len(self.Q), unMarkd)
        renum = renumber(parent, reachable)

        newS = renum[parent[list(self.S)[0]]]

        for i in self.F:
            if i not in reachable:
                continue
            newF.add(renum[parent[i]])

        for i in range(len(renum)):
            newQ.add(i)

        for i in range(len(self.Q)):
            if parent[i] not in renum or renum[parent[i]] in newDelta:
                continue
            newDelta[renum[parent[i]]] = dict()
            for sym in self.sigma:
                newDelta[renum[parent[i]]][sym] = set([renum[parent[list(self.delta[i][sym])[0]]]])
        return DFA(newQ, self.sigma, newDelta, set([newS]), newF)
        

    def complement(self):
        Fprime = self.Q
        for i in self.F:
            Fprime.discard(i)
        return DFA(self.Q, self.sigma, self.delta, self.S, Fprime)

    @staticmethod
    def string_to_DFA(s):
        nfa = NFA.string_to_NFA(s)
        return nfa.getDFA()

    @staticmethod
    def exp_to_DFA(exp):
        nfa = NFA.exp_to_NFA(exp)
        return nfa.getDFA()

    def intersection(self, dfa):
        newQ = set()
        newDelta = dict()
        newF = set()
        newS = self.S * len(dfa.Q) + dfa.S
        for i in range(len(self.Q) * len(dfa.Q)):
            newQ.add(i)
            newDelta[i] = dict()
        
        for i in range(len(self.Q) * len(dfa.Q)):
            for sym in self.sigma:
                first = i / len(dfa.Q)
                second = i % len(dfa.Q)
                nxt = self.delta[first][sym] * len(dfa.Q) + self.delta[second][sym]
                newDelta[i][sym] = nxt
        
        for i in range(len(self.Q)):
            for j in range(len(dfa.Q)):
                if i in self.F and j in dfa.F:
                    newF.add(i* len(dfa.Q) + j)
        return DFA(newQ, self.sigma, newDelta, newS, newF)
