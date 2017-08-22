INTEGER =   'INTEGER'
OPERATOR=   'OPERATOR'  # +,-,*,/
EOF     =   'EOF'
LPAREN  =   'LPAREN'    # (
RPAREN  =   'RPAREN'    # )

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def str(self):
        return 'Token({type}, {value})'.format(
                    type = self.type,
                    value = repr(self.value)
                )
    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = self.get_next_token()

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        while current_char == ' ':
            self.pos += 1
            if self.pos == len(text):
                return Token(EOF, None)
            current_char = text[self.pos]

        if current_char.isdigit():
            integer = ''
            while current_char.isdigit():
                integer += current_char
                self.pos += 1
                if self.pos == len(text):
                    break
                current_char = text[self.pos]
            token = Token(INTEGER, int(integer))
            return token

        if current_char == '+':
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token
        if current_char == '-':
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token
        if current_char == '*':
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token
        if current_char == '/':
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token
        if current_char == '(':
            token = Token(LPAREN, current_char)
            self.pos +=1
            return token
        if current_char == ')':
            token = Token(RPAREN, current_char)
            self.pos +=1
            return token

        print(current_char)
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            print(self.current_token.type+' | '+token_type)
            self.error()
    
    def expr(self):
        result = self.term()

        while self.current_token.value in ('+', '-'):
            token = self.current_token
            self.eat(OPERATOR)
            if token.value == '+':
                result = result + self.term()
            elif token.value == '-':
                result = result - self.term()
        return result

    def term(self):
        result = self.factor()
        
        while self.current_token.value in ('*', '/'):
            token = self.current_token 
            self.eat(OPERATOR)
            if token.value == '*':
                result = result * self.factor()
            elif token.value == '/':
                result = result / self.factor()
        return result

    def factor(self):
        token =  self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            result = token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
        return result

def main():
    while True:
        try:
            text = input("calc>")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nGoodbye, and may the Force be with you, always.")
            print("[John Williams Intensifies]")
            return 0
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__=='__main__':
    main()

