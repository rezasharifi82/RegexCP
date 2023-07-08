landa = 'L'


class State:
    num = 1

    def __init__(self):
        self.name = 'q' + str(State.num)
        State.num += 1
        self.ls = []

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.name

    def __gt__(self, other):
        return int(self.name[-1]) > int(other.name[-1])


class Dfa:

    def __init__(self, begin, final_state, terminal):
        self.states = []
        self.transition = []
        self.terminal = terminal
        self.trap = None
        self.final = None
        self.states.append(begin)
        self.end = final_state
        self.start = begin

    def nfa_to_dfa(self):
        for j in self.states:
            for i in self.terminal:
                temp = set()
                fucking_des = fuck_this_shit(j, temp, i)
                complete_set_landatrans(fucking_des)
                if len(fucking_des) == 0:
                    continue
                if fucking_des not in self.states:
                    self.states.append(fucking_des)
                self.transition.append([j, i, fucking_des])
        self.add_trap()
        self.set_fin()

    def add_trap(self):
        trap = State()
        trap_state = set()
        trap_state.add(trap)
        self.trap = trap_state
        self.states.append(trap_state)
        for i in self.terminal:
            pass
        self.transition.append([trap_state, i, trap_state])
        ls = [i[:-1] for i in self.transition]
        for j in self.states:
            for i in self.terminal:
                if [j, i] not in ls:
                    self.transition.append([j, i, trap_state])

    def set_fin(self):
        finall = []
        for it, i in enumerate(self.states):
            if self.end in i:
                finall.append(it)
        self.final = finall

    def minimize(self):
        # Partition the states into two groups: final and non-final states
        non_final_states = [state_set for state_set in self.states if self.end not in state_set]
        final_states = [state_set for state_set in self.states if self.end in state_set]
        partitions = [non_final_states, final_states]
        transition_list = [i[:-1] for i in self.transition]
        while True:
            change = False
            for group in partitions:
                transition_numbers = []
                for state_set in group:
                    num = 1
                    for terminal in self.terminal:
                        temp_num = 0
                        index = transition_list.index([state_set, terminal])
                        des = self.transition[index][-1]
                        for i in partitions:
                            if des in i:
                                temp_num = partitions.index(i)
                                break
                        num *= 10
                        num += temp_num
                    transition_numbers.append(num)
                if (len(set(transition_numbers)) != 1):
                    change = True
                    fine_list = []
                    fine_list_numbers = []
                    for ind, state_set in enumerate(group):
                        if transition_numbers[ind] not in fine_list_numbers:
                            fine_list_numbers.append(transition_numbers[ind])
                            fine_list.append([state_set])
                        else:
                            fine_list[fine_list_numbers.index(transition_numbers[ind])].append(state_set)
                    partitions.remove(group)
                    for i in fine_list:
                        partitions.append(i)
                    break
            if not change:
                break
        for i in partitions:
            for j in i[1:]:
                self.states.remove(j)
                while j in [x[0] for x in self.transition]:
                    self.transition[[x[0] for x in self.transition].index(j)][0] = i[0]
                while j in [x[-1] for x in self.transition]:
                    self.transition[[x[-1] for x in self.transition].index(j)][-1] = i[0]
        self.trans_set()
        self.set_fin()

    def trans_set(self):
        for item in reversed(self.transition):
            while self.transition.count(item) > 1:
                self.transition.remove(item)

    def do_transition(self, start: set, trans):
        return self.transition[[x[:-1] for x in self.transition].index([start, trans])][-1]


def Compare_dfa(dfa1: Dfa, dfa2: Dfa):
    for i in dfa1.terminal:
        if i not in dfa2.terminal:
            return False
    for i in dfa2.terminal:
        if i not in dfa1.terminal:
            return False
    match = []  # [dfa1.state,dfa2.state,check?]
    all_states = []
    match.append([dfa1.start, dfa2.start])
    all_states.append(dfa1.start)
    all_states.append(dfa2.start)
    for i in match:
        if (i[0] in dfa1.final and i[1] not in dfa2.final) or (i[0] not in dfa1.final and i[1] in dfa2.final):
            return False
        for j in dfa1.terminal:
            if [dfa1.do_transition(i[0], j), dfa2.do_transition(i[1], j)] not in match:
                if (dfa2.do_transition(i[1], j) in all_states) or (dfa1.do_transition(i[0], j) in all_states):
                    return False
                match.append([dfa1.do_transition(i[0], j), dfa2.do_transition(i[1], j)])
                all_states.append(dfa1.do_transition(i[0], j))
                all_states.append(dfa2.do_transition(i[1], j))
    return True


def get_list(ls):
    return fuck3(fuck2(fuck(ls)))


def fuck(ls):
    while ls[0] == ')' and ls[-1] == '(':
        ls = ls[1:-1]
    result = []
    i = 0
    par_num = 0
    while i < len(ls):
        if ls[i] != '(':
            result.append(ls[i])
            i += 1
            continue
        if ls[i] == '(':
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
        if ind > 1:
            res += ls[: ind - 1]
        res.append([ls[ind - 1], ls[ind]])
        if ind < len(ls) - 1:
            res += ls[ind + 1:]
        ls = res
    return ls


def fuck3(ls: list):
    for it, i in enumerate(ls):
        if type(i) == list:
            ls[it] = fuck3(i)
    if '+' in ls:
        ind = ls.index('+')
        first_state = fuck3(ls[:ind])
        second = fuck3(ls[ind + 1:])
        res = [first_state, 'or', second]
        ls = res
    return ls


def nfa_generator(ls: list, current: State):
    print(ls)
    while(len(ls)==1 and type(ls)==list):
        ls=ls[0]
    if len(ls) == 3 and ls[1] == 'or':
        current = or_generator(ls, current)
    elif len(ls) == 2 and ls[1] == '*':
        current = star_generator(ls, current)
    else:
        current = and_generator(ls, current)
    return current


def and_generator(trans: list, currnet: State):
    for i in trans:
        temp=State()
        currnet.ls.append((landa,temp))
        currnet=temp
        if type(i) is list and len(i) > 1:
            currnet = nfa_generator(i, currnet)
        else:
            if type(i) is list:
                i = i[0]
            b = State()
            currnet.ls.append((i, b))
            currnet = b
    return currnet


def or_generator(trans: list, current: State):
    a = State()
    b = State()
    c = nfa_generator(trans[0], a)
    d = nfa_generator(trans[2], b)
    current.ls.append((landa, a))
    current.ls.append((landa, b))
    e = State()
    c.ls.append((landa, e))
    d.ls.append((landa, e))
    return e


def star_generator(trans: list, current: State):
    b = nfa_generator(trans[0], current)
    b.ls.append((landa, current))
    current.ls.append((landa, b))
    return b


def print_grammar(current: State):
    visited = set()
    grammar(current, visited)


def grammar(current: State, visited):
    visited.add(current)
    for i in current.ls:
        print(current.name, '--', i[0], '->', i[1].name)
        if i[1] not in visited:
            grammar(i[1], visited)


def save_states(states: set, first_state: State):
    states.add(first_state)
    for i in first_state.ls:
        if i[1] not in states:
            save_states(states, i[1])


def print_set(ls: set):
    for it, i in enumerate(ls):
        print(i.name, end='')
        if it != len(ls) - 1:
            print(',', end='')


def complete_set_landatrans(state_list: set):
    for temp in state_list:
        for j in temp.ls:
            if j[0] == landa and j[1] not in state_list:
                state_list.add(j[1])
                return complete_set_landatrans(state_list)
    return state_list


def complete_set(temp: State, des_set: set, transition: str):
    temp_set = des_set.copy()
    for i in temp.ls:
        if i[0] == transition and i[1] not in temp_set:
            temp_set.add(i[1])
    return temp_set


def fuck_this_shit(began_set, des_set, trans):
    final_set = set()
    for k in began_set:
        final_set = final_set.union(set(complete_set(k, des_set, trans)))
    return final_set


def print_dfa(dfa):
    for it, i in enumerate(dfa.states):
        print('state', it, ':', end='')
        print_set(i)
        if it != len(dfa.states) - 1:
            print('|', end='')
    for i in dfa.transition:
        print()
        print(dfa.states.index(i[0]), end='|')
        print(i[1], end='|')
        print(dfa.states.index(i[2]), end='')
    print('\nstart state: 0 ')
    print('finall states:', dfa.final)
    print('trap:', dfa.states.index(dfa.trap))


def get_terminal(reg):
    terminals = []
    for i in list(reg):
        if i not in ['+', '*', '(', ')', 'L'] and i not in terminals:
            terminals.append(i)
    return terminals


def get_min_dfa():
    print("enter regex:")
    reg = input()
    terminal = get_terminal(reg)
    print('terminal:', terminal)
    list1 = get_list(list(reg))
    print('list: ', list1)
    print('\n----------------nfa--------------------')
    first = State()
    first_set = set()
    end = nfa_generator(list1, first)
    print_grammar(first)
    save_states(first_set, first)
    start = set()
    start.add(first)
    complete_set_landatrans(start)
    print('\n----------------dfa--------------------')
    first_dfa = Dfa(start, end, terminal)
    first_dfa.nfa_to_dfa()
    print_dfa(first_dfa)
    print('\n----------------min--------------------')
    first_dfa.minimize()
    print_dfa(first_dfa)
    return first_dfa

while True:
    dfa1 = (get_min_dfa())
    dfa2 = (get_min_dfa())
    print(Compare_dfa(dfa1, dfa2))

# b*(abb*)*(a+L)
# (b+ab)*(a+L)
# b*+(b+ab)*ab*
