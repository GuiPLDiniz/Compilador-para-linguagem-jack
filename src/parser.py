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

        if not self.match("symbol", ")"):
            self.compile_type()
            self.consume("identifier")

            while self.match("symbol", ","):
                self.consume("symbol", ",")
                self.compile_type()
                self.consume("identifier")

        self.close_tag("parameterList")
    
    def compile_subroutine_body(self):
        self.open_tag("subroutineBody")

        self.consume("symbol", "{")

        # varDec* (ignorado por enquanto)
        while self.match("keyword", "var"):
            self.compile_var_dec()

        self.compile_statements()

        self.consume("symbol", "}")

        self.close_tag("subroutineBody")
    
    def compile_var_dec(self):
        self.open_tag("varDec")

        self.consume("keyword", "var")
        self.compile_type()
        self.consume("identifier")

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")

        self.consume("symbol", ";")

        self.close_tag("varDec")
    
    def compile_statements(self):
        self.open_tag("statements")

        while (
            self.match("keyword", "let") or
            self.match("keyword", "if") or
            self.match("keyword", "while") or
            self.match("keyword", "do") or
            self.match("keyword", "return")
        ):
            if self.match("keyword", "let"):
                self.compile_let()
            elif self.match("keyword", "while"):
                self.compile_while()
            elif self.match("keyword", "do"):
                self.compile_do()
            elif self.match("keyword", "return"):
                self.compile_return()
            elif self.match("keyword", "if"):
                self.compile_if()

        self.close_tag("statements")
    
    def compile_return(self):
        self.open_tag("returnStatement")

        self.consume("keyword", "return")

        if not self.match("symbol", ";"):
            self.compile_expression()

        self.consume("symbol", ";")

        self.close_tag("returnStatement")
    
    def compile_let(self):
        self.open_tag("letStatement")

        self.consume("keyword", "let")
        self.consume("identifier")

        
        if self.match("symbol", "["):
            self.consume("symbol", "[")
            self.compile_expression()
            self.consume("symbol", "]")

        self.consume("symbol", "=")

        self.compile_expression()

        self.consume("symbol", ";")

        self.close_tag("letStatement")
    
    def compile_do(self):
        self.open_tag("doStatement")

        self.consume("keyword", "do")

        self.consume("identifier")

        if self.match("symbol", "."):
            self.consume("symbol", ".")
            self.consume("identifier")

        self.consume("symbol", "(")
        self.compile_expression_list()
        self.consume("symbol", ")")

        self.consume("symbol", ";")

        self.close_tag("doStatement")

    def compile_while(self):
        self.open_tag("whileStatement")

        self.consume("keyword", "while")

        self.consume("symbol", "(")

        self.compile_expression()

        self.consume("symbol", ")")

        self.consume("symbol", "{")

        self.compile_statements()

        self.consume("symbol", "}")

        self.close_tag("whileStatement")

    def compile_if(self):
        self.open_tag("ifStatement")

        self.consume("keyword", "if")
        self.consume("symbol", "(")

        self.compile_expression()

        self.consume("symbol", ")")
        self.consume("symbol", "{")

        self.compile_statements()

        self.consume("symbol", "}")

        if self.match("keyword", "else"):
            self.consume("keyword", "else")
            self.consume("symbol", "{")
            self.compile_statements()
            self.consume("symbol", "}")

        self.close_tag("ifStatement")
    
    def compile_expression(self):
        self.open_tag("expression")

        self.compile_term()

        while self.match("symbol") and self.current_token()[1] in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.consume("symbol")
            self.compile_term()

        self.close_tag("expression")

    
    def compile_term(self):
        self.open_tag("term")

        token = self.current_token()

        if token is None:
            raise SyntaxError("Fim inesperado de tokens")

        token_type, value = token

        # integerConstant
        if token_type == "integerConstant":
            self.consume("integerConstant")

        # stringConstant
        elif token_type == "stringConstant":
            self.consume("stringConstant")

        # keywordConstant
        elif token_type == "keyword" and value in ["true", "false", "null", "this"]:
            self.consume("keyword")

        # identifier (var, array, subroutine)
        elif token_type == "identifier":
            self.consume("identifier")

            if self.match("symbol", "["):
                self.consume("symbol", "[")
                self.compile_expression()
                self.consume("symbol", "]")

            elif self.match("symbol", "("):
                self.consume("symbol", "(")
                self.compile_expression_list()
                self.consume("symbol", ")")

            elif self.match("symbol", "."):
                self.consume("symbol", ".")
                self.consume("identifier")
                self.consume("symbol", "(")
                self.compile_expression_list()
                self.consume("symbol", ")")

        # (expression)
        elif self.match("symbol", "("):
            self.consume("symbol", "(")
            self.compile_expression()
            self.consume("symbol", ")")

        # unaryOp term
        elif self.match("symbol") and value in ["-", "~"]:
            self.consume("symbol")
            self.compile_term()

        else:
            raise SyntaxError(f"Termo inválido: {token}")

        self.close_tag("term")

    def compile_expression_list(self):
        self.open_tag("expressionList")

        if not self.match("symbol", ")"):
            self.compile_expression()

            while self.match("symbol", ","):
                self.consume("symbol", ",")
                self.compile_expression()

        self.close_tag("expressionList")