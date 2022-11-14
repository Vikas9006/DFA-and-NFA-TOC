from grep import DFA
from grep import NFA
from parser import parser

def run():
    T = int(input())
    outputs = []
    for i in range(T):
        expression = input()
        string = input()
        try:
            dfa = DFA.exp_to_DFA(parser(expression))
            dfa = dfa.minimize()
            if dfa.belongs(string):
                outputs.append("Yes")
            else:
                outputs.append("No")
        except:
            outputs.append("No")
    for i in outputs:
        print(i)

if __name__ == "__main__":
    run()

"""
5
star(symbol(a))
aaaa
concat(star(symbol(b)),symbol(a))
bba
concat(star(symbol(a)),union(symbol(b),symbol(c)))
aab
concat(star(union(symbol(a),union(symbol(b),symbol(c)))),symbol(d))
dabcd
concat(concat(symbol(0),symbol(1)),star(union(symbol(0),symbol(1))))
1011
"""