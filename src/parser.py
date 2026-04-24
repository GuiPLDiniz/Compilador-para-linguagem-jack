from tokenizer import escape_xml


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.lines = []

    def current_token(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def advance(self):
        if self.current < len(self.tokens):
            self.current += 1

    def peek(self):
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None

    def match(self, token_type, value=None):
        token = self.current_token()

        if token is None:
            return False

        current_type, current_value = token

        if current_type != token_type:
            return False

        if value is not None and current_value != value:
            return False

        return True

    def consume(self, token_type, value=None):
        if not self.match(token_type, value):
            expected = token_type if value is None else f"{token_type} '{value}'"
            found = self.current_token()
            raise SyntaxError(f"Token inesperado. Esperado: {expected}. Encontrado: {found}")

        token = self.current_token()
        self.write_token(token)
        self.advance()
        return token

    def write_token(self, token):
        token_type, value = token
        escaped_value = escape_xml(value)
        self.lines.append(f"<{token_type}> {escaped_value} </{token_type}>")

    def open_tag(self, tag):
        self.lines.append(f"<{tag}>")

    def close_tag(self, tag):
        self.lines.append(f"</{tag}>")

    def get_xml(self):
        return "\n".join(self.lines) + "\n"
    
    def compile_class(self):
        self.open_tag("class")

        self.consume("keyword", "class")
        self.consume("identifier")  # nome da classe
        self.consume("symbol", "{")

        # classVarDec*
        while self.match("keyword", "static") or self.match("keyword", "field"):
            self.compile_class_var_dec()

        # subroutineDec*
        while self.match("keyword", "constructor") or \
            self.match("keyword", "function") or \
            self.match("keyword", "method"):
            
            self.compile_subroutine_dec()

        self.consume("symbol", "}")

        self.close_tag("class")

    def compile_class_var_dec(self):
        self.open_tag("classVarDec")

        self.consume("keyword")  # static | field
        self.compile_type()
        self.consume("identifier")  # varName

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")  # varName

        self.consume("symbol", ";")

        self.close_tag("classVarDec")

    def compile_type(self):
        if self.match("keyword", "int") or self.match("keyword", "char") or self.match("keyword", "boolean"):
            self.consume("keyword")
        elif self.match("identifier"):
            self.consume("identifier")
        else:
            raise SyntaxError(f"Tipo inválido encontrado: {self.current_token()}")
        
    def compile_subroutine_dec(self):
        self.open_tag("subroutineDec")

        # constructor | function | method
        self.consume("keyword")

        # void | type
        if self.match("keyword", "void"):
            self.consume("keyword", "void")
        else:
            self.compile_type()

        # nome da subrotina
        self.consume("identifier")

        self.consume("symbol", "(")
        self.compile_parameter_list()
        self.consume("symbol", ")")

        self.compile_subroutine_body()

        self.close_tag("subroutineDec")
    
    def compile_parameter_list(self):
        self.open_tag("parameterList")
        # vazio por enquanto
        self.close_tag("parameterList")
    
    def compile_subroutine_body(self):
        self.open_tag("subroutineBody")

        self.consume("symbol", "{")

        # varDec* (ignorado por enquanto)
        while self.match("keyword", "var"):
            self.advance()  # temporário

        # statements (ignorado por enquanto)
        while not self.match("symbol", "}"):
            self.advance()  # temporário

        self.consume("symbol", "}")

        self.close_tag("subroutineBody")