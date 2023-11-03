class State:
    def __init__(self, label=None, edges=None):
        self.edges = edges if edges else []
        self.label = label

class Fragment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def thompson(postfix):
    stack = []
    state_count = 0

    
    for char in postfix:
        if char.isalnum():
            end = State()
            start = State(char, [end])
            stack.append(Fragment(start, end))
            state_count += 2
        elif char == '*':
            frag = stack.pop()
            end = State()
            start = State(edges=[frag.start, end])
            frag.end.edges.append(frag.start)
            frag.end.edges.append(end)
            stack.append(Fragment(start, end))
            state_count += 2
        elif char == '+':
            frag2 = stack.pop()
            frag1 = stack.pop()
            start = State(edges=[frag1.start, frag2.start])
            end = State()
            frag1.end.edges.append(end)
            frag2.end.edges.append(end)
            stack.append(Fragment(start, end))
            state_count += 2
        elif char == '.':
            frag2 = stack.pop()
            frag1 = stack.pop()
            frag1.end.label = None
            frag1.end.edges.append(frag2.start)
            stack.append(Fragment(frag1.start, frag2.end))

    state_names = {}
    print_nfa(stack[0].start, state_names=state_names)
    return stack.pop()


def infix_to_postfix(regex):
    precedence = {'*': 3, '.': 2, '+': 1, '(': 0, ')': 0}
    temp = []
    for i in range(len(regex)):
        if i != 0\
            and (regex[i-1].isalnum() or regex[i-1] == ")" or regex[i-1] == "*")\
            and (regex[i].isalnum() or regex[i] == "("):
            temp.append(".")
        temp.append(regex[i])
    regex = temp
    output = ""
    stack1 = []

    for char in regex:
        if char.isalnum():
            output += char
        elif char == '(':
            stack1.append(char)
        elif char == ')':
            while stack1 and stack1[-1] != '(':
                output += stack1.pop()
            stack1.pop()
        else:
            while stack1 and precedence[char] <= precedence[stack1[-1]]:
                output += stack1.pop()
            stack1.append(char)

    while stack1:
        output += stack1.pop()

    return output


def print_nfa(start, visited=None, state_names=None):
    if visited is None:
        visited = set()
        state_names = {start: f'q0'}

    if start in visited:
        return

    visited.add(start)

    for edge in start.edges:
        if edge not in state_names:
            state_names[edge] = f'q{len(state_names)}'
        print(f"State: {state_names[start]}, Symbol: {start.label or 'epsilon'}, Next state: {state_names[edge]}")
        print_nfa(edge, visited, state_names)

    

# Test the function
regex = input("Enter regex: ")
postfix_regex = infix_to_postfix(regex)
print("The given regular expresson is : ",regex)
print("postfix of reular expression is : ",postfix_regex)
nfa_frag = thompson(postfix_regex)



