class First_Follow():
    def __init__(self, grammar):
        self.grammar = grammar
        self.non_terminals = grammar.keys()
        print(self.non_terminals)
        self.start = list(self.non_terminals)[0]
        self.rules = [(head, body) for head, bodies in grammar.items()
                      for body in bodies]
        
    def compute_first(self, variable):
        first = set()
        for production in self.grammar[variable]:
            if not production[0].isupper():
                first.add(production[0])
            else:
                first |= self.compute_first(production[0])
        return first

    def compute_follow(self, variable):
        follow = set()
        if variable == self.start:
            follow.add('$')
        for rule in self.rules:
            for j, char in enumerate(rule[1]):
                if char == variable:
                    while j < len(rule[1]) - 1:
                        if not rule[1][j + 1].isupper():
                            follow.add(rule[1][j + 1])
                            break
                        else:
                            follow |= self.compute_first(rule[1][j + 1])
                            if '@' not in self.compute_first(rule[1][j + 1]):
                                break
                        j += 1
                    else:
                        if rule[0] != variable:
                            follow |= self.compute_follow(rule[0])
        follow.discard('@')
        return follow

    def print_sets(self):
        print("First Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.compute_first(non_terminal)}")
        print("\nFollow Sets:")
        for non_terminal in self.non_terminals:
            print(f"{non_terminal}: {self.compute_follow(non_terminal)}")


def main():
    example_grammar = {
        'E': ['TZ'],
        'Z': ['+TZ', '@'],
        'T': ['FY'],
        'Y': ['*FY', '@'],
        'F': ['(E)', 'i'],
    }
    ff = First_Follow(example_grammar)
    print("Epsilon is printed as @")
    print()
    ff.print_sets()


if __name__ == '__main__':
    main()
