from Tree import Node

def parser(s):
    if len(s) == 0:
        return None
    
    # If s is alphabet member
    if "(" not in s:
        return Node(s)

    expr = []
    open_bracket = False
    bracket_count = 0
    child = ""
    data = ""
    for j in range(len(s)):
        i = s[j]
        if i == "(":
            bracket_count += 1
        elif i == ")":
            bracket_count -= 1

        # outer function
        if bracket_count == 1 and i ==  "(":
            pass
        elif bracket_count == 0 and i != ")":
            data += i
        elif bracket_count == 0 and i == ")" and len(child) > 0:
            expr.append(child)
            child = ""
        else:
            if bracket_count == 1:
                if i == ",":
                    continue
            child += i
            if bracket_count == 1:
                if i == ")":
                    expr.append(child)
                    child = ""

    node = Node(data)
    if len(expr) >= 1:
        node.left = parser(expr[0])
    
    if len(expr) == 2:
        node.right = parser(expr[1])
    return node