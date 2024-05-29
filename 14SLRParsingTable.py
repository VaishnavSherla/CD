from collections import defaultdict

class SLRParser:
    def __init__(self, grammar, terminals):
        self.grammar = grammar
        self.terminals = terminals
        self.NT = list(grammar.keys())
        self.rules = [(head, body) for head, bodies in grammar.items() for body in bodies]
        self.start_symbol = self.rules[0][0]
        self.new_start_symbol = 'Z'
        self.closure = [(self.new_start_symbol, '.' + self.start_symbol)]
        self.states = {0: self.findClosure(self.closure)}
        self.statemap = {}
        self.count = 0
        self.buildParsingTable()
    
    def findClosure(self, closure):
        while True:
            n = len(closure)
            temp_cl = closure.copy()
            for lhs, rhs in closure:
                if rhs[-1] == '.':
                    continue
                dot_index = rhs.index('.')
                B = rhs[dot_index+1]
                if B.isupper():
                    for prod in self.grammar[B]:
                        item = (B, '.'+prod)
                        if item not in temp_cl:
                            temp_cl.append(item)
            closure = temp_cl
            if len(closure) == n:
                return closure
    
    def findGOTO(self, state_num):
        closure = self.states[state_num]
        new = set()
        gotos = defaultdict(list)
        for lhs, rhs in closure:
            if rhs[-1] == '.':
                continue
            dot_index = rhs.index('.')
            charNextToDot = rhs[dot_index+1]
            rhs = rhs[:dot_index] + charNextToDot + '.' + rhs[dot_index+2:]
            new_cl = [(lhs, rhs)]
            new_cl = self.findClosure(new_cl)
            gotos[charNextToDot].extend(new_cl)

        for lhs, new_cl in gotos.items():
            for num, cl in self.states.items():
                if new_cl == cl:
                    self.statemap[(state_num, lhs)] = num
                    break
            else:
                self.count += 1
                self.states[self.count] = new_cl
                self.statemap[(state_num, lhs)] = self.count
                new.add(self.count)
        return new
    
    def GOTO(self, num):
        new = self.findGOTO(num)
        while True:
            n = len(new)
            new1 = new.copy()
            for i in new:
                new1 |= self.findGOTO(i)
            new = new1
            if len(new) == n:
                break
    
    def buildParsingTable(self):
        self.GOTO(0)
        cols = self.terminals + ['$'] + self.NT
        Table = [['']*len(cols) for _ in range(self.count+1)]
        for map, s in self.statemap.items():
            num, char = map
            index = cols.index(char)
            if char in self.NT:
                Table[num][index] = f'{s}'
            else:
                Table[num][index] = f'S{s}'
        for num, cl in self.states.items():
            for lhs, rhs in cl:
                if rhs[-1] == '.':
                    if rhs[0] == self.start_symbol and lhs == self.new_start_symbol:
                        index = cols.index('$')
                        Table[num][index] = 'Accept'
                    else:
                        prod_num = self.rules.index((lhs, rhs[:-1]))
                        follow = self.computeFollow(lhs)
                        for i in follow:
                            index = cols.index(i)
                            Table[num][index] = f'R{prod_num+1}'
        print("\nSLR(1) parsing table:\n")
        frmt = "{:>8}" * len(cols)
        print("   ", frmt.format(*cols), "\n")
        ptr = 0
        j = 0
        for y in Table:
            print(f"{{:>3}} {frmt.format(*y)}".format('I' + str(j)))
            j += 1

    def computeFirst(self, variable):
        first = set()
        if not variable.isupper():
            first.add(variable)
        else:
            for production in self.grammar[variable]:
                first |= self.computeFirst(production[0])
                if "ε" not in first:
                    break
        return first

    def computeFollow(self, variable):
        follow = set()
        if variable == self.start_symbol:
            follow.add('$')

        for lhs, rhs in self.rules:
            for index, nonTerminal in enumerate(rhs):
                if nonTerminal == variable:
                    while index < len(rhs) - 1:
                        beta = rhs[index + 1]
                        if not beta.isupper():
                            follow.add(beta)
                            break
                        else:
                            follow |= self.computeFirst(beta)
                            if 'ε' not in self.computeFirst(beta):
                                break
                        index += 1
                    else:
                        if lhs != variable:
                            follow |= self.computeFollow(lhs)

        follow.discard('ε')
        return follow

# Test Case - 1
CFG = {'E': ['E+T', 'T'],
       'T': ['T*F', 'F'],
       'F': ['(E)', 'i']}

T = ['+', '*', '(', ')', 'i']

SLRParser(CFG, T)
