from Tree import Node
from parser import parser

epsilon = "ε"

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
                lnfa.delta[final1][epsilon] = rnfa.S

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

    def getDFA(self):
        pass



class DFA:
    def __init__(self, Q, sigma, delta, s, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

    def __str__(self):
        return "DFA = (" + "\n" + \
         "Q = " + str(self.Q) + "\n" + \
            "Σ = " + str(self.sigma) + "\n" + \
            "δ = " + str(self.delta) + "\n" + \
            "s = " + str(self.S) + "\n" + \
            "F = " + str(self.F) + "\n" + \
            ")" + "\n"

    def belongs(self, s):
        q = self.s
        for i in s:
            q = self.delta[q][i]
        return q in self.F

    def minimize(self):
        pass

    def complement(self):
        Fprime = self.Q
        for i in self.F:
            Fprime.discard(i)
        return DFA(self.Q, self.sigma, self.delta, self.s, Fprime)

    @staticmethod
    def string_to_DFA(s):
        nfa = NFA.string_to_NFA(s)
        return nfa.getDFA()

    @staticmethod
    def exp_to_DFA(exp):
        nfa = NFA.exp_to_NFA(exp)
        return nfa.getDFA()

exp = "star(union(symbol(a),symbol(b)))"
b = parser(exp)
c = NFA.exp_to_NFA(b)
print(c)