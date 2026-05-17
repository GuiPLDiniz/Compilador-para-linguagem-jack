from vm_writer import VMWriter
from symbol_table import SymbolTable


class CompilationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

        self.vm_writer = VMWriter()
        self.symbol_table = SymbolTable()

        self.class_name = ""
        self.subroutine_name = ""

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
        self.advance()
        return token

    def get_vm_code(self):
        return self.vm_writer.get_output()
    
    def compile_class(self):
        self.consume("keyword", "class")

        _, class_name = self.consume("identifier")
        self.class_name = class_name

        self.consume("symbol", "{")

        while self.match("keyword", "static") or self.match("keyword", "field"):
            self.compile_class_var_dec()

        while (
            self.match("keyword", "constructor") or
            self.match("keyword", "function") or
            self.match("keyword", "method")
        ):
            # subrotinas serão implementadas nos próximos commits
            self.advance()

        self.consume("symbol", "}")


    def compile_class_var_dec(self):
        _, kind = self.consume("keyword")  # static | field
        var_type = self.compile_type()

        _, name = self.consume("identifier")
        self.symbol_table.define(name, var_type, kind)

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            _, name = self.consume("identifier")
            self.symbol_table.define(name, var_type, kind)

        self.consume("symbol", ";")


    def compile_type(self):
        if (
            self.match("keyword", "int") or
            self.match("keyword", "char") or
            self.match("keyword", "boolean")
        ):
            _, value = self.consume("keyword")
            return value

        if self.match("identifier"):
            _, value = self.consume("identifier")
            return value

        raise SyntaxError(f"Tipo inválido: {self.current_token()}")