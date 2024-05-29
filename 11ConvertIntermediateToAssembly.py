class Operation:
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

def generate_assembly(intermediate_code):
    assembly_code = []

    for op in intermediate_code:
        if op.source.isdigit():
            assembly_code.append(f"mov {op.destination}, {op.source}")
        elif '+' in op.source:
            operands = op.source.split('+')
            assembly_code.append(f"mov eax, {operands[0]}")
            assembly_code.append(f"add eax, {operands[1]}")
            assembly_code.append(f"mov {op.destination}, eax")
        elif '*' in op.source:
            operands = op.source.split('*')
            assembly_code.append(f"mov eax, {operands[0]}")
            assembly_code.append(f"mul eax, {operands[1]}")
            assembly_code.append(f"mov {op.destination}, eax")
        elif '-' in op.source:
            operands = op.source.split('-')
            assembly_code.append(f"mov eax, {operands[0]}")
            assembly_code.append(f"sub eax, {operands[1]}")
            assembly_code.append(f"mov {op.destination}, eax")
        else:
            assembly_code.append(f"mov {op.destination}, {op.source}")
    
    return assembly_code

def print_assembly(assembly_code):
    print("Assembly Code:")
    for line in assembly_code:
        print(line)

# eax -> temp register in x86
def main():
    intermediate_code = [
        Operation('m', '1'),
        Operation('x', 'a+b'),
        Operation('y', 'c+d'),
        Operation('z', 'x*x'),
        Operation('u', 'x*y'),
        Operation('w', 'u'),
        Operation('v', 'z')
    ]
    
    assembly_code = generate_assembly(intermediate_code)
    print_assembly(assembly_code)

if __name__ == "__main__":
    main()