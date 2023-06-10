from collections import deque

def get_list(ls):
    return (fuck3(fuck2(fuck(ls))))


def fuck(ls):
    while (ls[0] == ')' and ls[-1] == '('):
        ls = ls[1:-1]
    result = []
    i = 0
    par_num = 0
    while i < len(ls):
        if ls[i] != '(':
            result.append(ls[i])
            i += 1
            continue
        if (ls[i] == '('):
            i += 1
            temp = []
            while not (ls[i] == ')' and par_num == 0):
                if ls[i] == '(':
                    par_num += 1
                elif ls[i] == ')':
                    par_num -= 1
                temp.append(ls[i])
                i += 1
            i += 1
            result.append(fuck(temp))
    return result


def fuck2(ls: list):
    for it in range(len(ls)):
        i = ls[it]
        if isinstance(i, list):
            if not (len(i) == 2 and i[1] in ['+', '*', '?']):
                ls[it] = fuck2(i)
    while '*' in ls:
        ind = ls.index('*')
        res = []
        if (ind > 1): res += ls[:ind - 1]
        res.append([ls[ind - 1], ls[ind]])
        if ind < len(ls) - 1:
            res += ls[ind + 1:]
        ls = res
    return ls


def fuck3(ls: list):
    for it in range(len(ls)):
        i = ls[it]
        if isinstance(i, list):
            ls[it] = fuck3(i)
    while '+' in ls:
        ind = ls.index('+')
        res = []
        res.append(ls[:ind])
        res.append('or')
        res.append(ls[ind + 1:])
        ls = res
    return ls


class state:
    num=1
    def __init__(self):
        self.name=state.num
        state.num+=1
        self.ls = []
        self.visited=False


# tuple :( weight , dest)
# And

landa = "L"


def nfa_generator(ls: list, Current: state):
    if len(ls) == 3 and ls[1] == 'or':
        Current=or_generator(ls,Current)
    elif len(ls) == 2 and ls[1] == '*':
        Current=star_generator(ls,Current)
    else:
        Current = and_generator(ls, Current)
    return Current


def and_generator(trans: list, Current: state):
    for i in trans:
        if (type(i) is list and len(i) > 1):
            Current = nfa_generator(i, Current)
        else:
            if (type(i) is list):
                i = i[0]
            b = state()
            Current.ls.append((i, b))
            Current = b
    return Current


def or_generator(trans: list, Current: state):
    a = state()
    b = state()
    c = nfa_generator(trans[0], a)
    d = nfa_generator(trans[2], b)
    Current.ls.append((landa, a))
    Current.ls.append((landa, b))
    e = state()
    c.ls.append((landa, e))
    d.ls.append((landa, e))
    return e


def star_generator(trans:list,Current:state):
    b=nfa_generator(trans[0],Current)
    b.ls.append((landa,Current))
    Current.ls.append((landa,b))
    return b

def print_grammar(Current:state):
    visited=set()
    grammar(Current,visited)

def grammar(Current:state,visited):
    visited.add(Current)
    for i in Current.ls:
        print(Current.name,'--',i[0],'->',i[1].name)
        if(i[1] not in visited):grammar(i[1],visited)

num=1
start=state()
end=nfa_generator(get_list(list(input())),start)
print_grammar(start)
