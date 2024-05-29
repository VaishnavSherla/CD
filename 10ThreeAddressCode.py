class ThreeAddressGenerator:
    def __init__(self):
        self.count = 0
        self.code, self.variableStack, self.operatorStack = [], [], []
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def generate_code(self, result_variable, expression):
        for char in expression:
            if char == "(":
                self.operatorStack.append(char)
            elif char == ")":
                while self.operatorStack[-1] != "(":
                    self.applyOperation(self.operatorStack.pop())
                self.operatorStack.pop()
            elif char in self.precedence:
                while self.operatorStack and self.precedence.get(self.operatorStack[-1], 0) >= self.precedence[char]:
                    self.applyOperation(self.operatorStack.pop())
                self.operatorStack.append(char)
            else:
                self.variableStack.append(char)
        
        while self.operatorStack:
            self.applyOperation(self.operatorStack.pop())
        self.code.append(f"{result_variable} = {self.variableStack.pop()}")
    
    def applyOperation(self, operator):
        right_operand, left_operand = self.variableStack.pop(), self.variableStack.pop()
        self.count += 1
        result = f't{self.count}'
        self.code.append(
            f"{result} = {left_operand} {operator} {right_operand}")
        self.variableStack.append(result)

generator = ThreeAddressGenerator()
expression = "a=(b*c+d)"
result_variable, expression = map(str.strip, expression.split("="))
generator.generate_code(result_variable, expression)
for instruction in generator.code:
    print(instruction)
print(f"Result: {expression}")
