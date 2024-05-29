class Op:
    def __init__(self, l, r):
        self.l = l
        self.r = r

def eliminate_unreachable_code(intermediate_code):
    reachable_vars = set()
    for item in intermediate_code:
        reachable_vars.add(item.l)
        for char in item.r:
            if char.isalpha():
                reachable_vars.add(char)
    return [item for item in intermediate_code if item.l in reachable_vars]

def removing_redundant(intermediate_code):
    optimized_operations = []
    num_operations = len(intermediate_code)
    
    for i in range(num_operations - 1):
        current_op = intermediate_code[i]
        if current_op.l == current_op.r:
            continue
        
        left_operand = current_op.l
        for j in range(num_operations):
            if left_operand in intermediate_code[j].r:
                optimized_operations.append(Op(current_op.l, current_op.r))
                break
    
    last_op = intermediate_code[num_operations - 1]
    optimized_operations.append(Op(last_op.l, last_op.r))
    
    return optimized_operations

def printCode(code, optimized=False):
    print("Intermediate Code") if not optimized else print("Optimized Code")
    for item in code:
        print(f"{item.l}={item.r}")

def main():
    op = [
        Op('m', '1'),
        Op('x', 'a+b'),
        Op('y', 'c+d'),
        Op('z', 'x^2'),
        Op('u', 'x*y'),
        Op('w', 'u'),
        Op('v', 'z')
    ]
    printCode(op)
    pr = removing_redundant(op)
    print("\nAfter Removing Redundant Code")
    printCode(pr)
    op = eliminate_unreachable_code(pr)
    print("\nAfter Eliminating Unreachable Code")
    printCode(op)

if __name__ == "__main__":
    main()
