class First_Follow():
    def __init__(self, grammar):
        self.grammar = grammar
        self.non_terminals = grammar.keys()
        self.start = list(self.non_terminals)[0]
        self.rules = [(nonTerminal, prod) for nonTerminal, productions in grammar.items() for prod in productions]
        print(self.rules)

    def computeFirst(self, variable):
        first = set()
        if not variable[0].isupper():
            first.add(variable[0])
        else:
            for production in self.grammar[variable]:
                first |= self.computeFirst(production[0])
        return first
        
    def computeFollow(self, variable):
        follow = set()
        if variable == self.start:
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
                        # If the production rule does not contain variable at the end, 
                        # compute the follow set for the left-hand side non-terminal of this rule
                        if lhs != variable:
                            follow |= self.computeFollow(lhs)
        
        follow.discard('ε')
        return follow


    def print_sets(self):
        print("First Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.computeFirst(non_terminal)}")

        print("\nFollow Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.computeFollow(non_terminal)}")
    
    def compute_parsing_table(self):
        print('\nParsing Table')
        table = {}

        for rule in self.rules:
            lhs, rhs = rule
            first = list(self.computeFirst(rhs[0]))
            if 'ε' in first:
                first.extend(self.computeFollow(lhs))
                first.remove('ε')
            
            for terminal in first:
                key = (lhs, terminal)
                if key in table:
                    table[key].append(rhs)
                else:
                    table[key] = [rhs]
        
        for key, value in table.items():
            print(f'{key} : {value}')

# ε
def main():
    example_grammar = {
        'E': ['TA'],
        'A': ['+TA', 'ε'],
        'T': ['FB'],
        'B': ['*FB', 'ε'],
        'F': ['(E)', 'i']
    }

    ff = First_Follow(example_grammar)

    ff.print_sets()
    ff.compute_parsing_table()

if __name__ == '__main__':
    main()