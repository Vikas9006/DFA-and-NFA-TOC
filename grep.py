class NFA:
    def __init__(self, Q, sigma, delta, s, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

    def __str__(self):
        pass

class DFA:
    def __init__(self, Q, sigma, delta, s, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.s = s
        self.F = F

def string_to_NFA(s):
    nfa = NFA(set(), set(s), dict(), None, set())
    for i in s:
        if not nfa.Q:
            pass
    return nfa
