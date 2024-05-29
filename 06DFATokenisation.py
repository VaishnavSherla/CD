import re


class TokenType:
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    END = 'END'


class Token:

    def __init__(self, type, value=None):
        self.type = type
        self.value = value


def get_next_token(input_str):
    input_str = input_str.lstrip()
    if not input_str:
        return Token(TokenType.END)

    if input_str[0] == '+':
        return Token(TokenType.PLUS)
    elif input_str[0] == '-':
        return Token(TokenType.MINUS)
    elif input_str[0] == '*':
        return Token(TokenType.MULTIPLY)
    else:
        match = re.match(r'^(\d+)', input_str)
        if match:
            number = int(match.group())
            return Token(TokenType.NUMBER, number)
        else:
            raise ValueError(f"Invalid character '{input_str[0]}'")


def main():
    input_str = "12.3 + 34 - 5 * 6"
    while True:
        token = get_next_token(input_str)
        if token.type == TokenType.END:
            print("End of input")
            break
        elif token.type == TokenType.NUMBER:
            print("Number:", token.value)
        else:
            print("Operator:", token.type)
        input_str = input_str[
            len(str(token.value)
                ):] if token.type == TokenType.NUMBER else input_str[1:]


if __name__ == '__main__':
    main()
