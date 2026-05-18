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

        self.while_count = 0
        self.if_count = 0

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
            self.compile_subroutine_dec()

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
    

    def compile_subroutine_dec(self):
        _, subroutine_kind = self.consume("keyword")  # constructor | function | method

        self.symbol_table.start_subroutine()

        if subroutine_kind == "method":
            self.symbol_table.define("this", self.class_name, "arg")

        if self.match("keyword", "void"):
            self.consume("keyword", "void")
        else:
            self.compile_type()

        _, subroutine_name = self.consume("identifier")
        self.subroutine_name = subroutine_name

        self.consume("symbol", "(")
        self.compile_parameter_list()
        self.consume("symbol", ")")

        self.compile_subroutine_body(subroutine_kind)


    def compile_parameter_list(self):
        if self.match("symbol", ")"):
            return

        var_type = self.compile_type()
        _, name = self.consume("identifier")
        self.symbol_table.define(name, var_type, "arg")

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            var_type = self.compile_type()
            _, name = self.consume("identifier")
            self.symbol_table.define(name, var_type, "arg")


    def compile_subroutine_body(self, subroutine_kind):
        self.consume("symbol", "{")

        while self.match("keyword", "var"):
            self.compile_var_dec()

        full_name = f"{self.class_name}.{self.subroutine_name}"
        n_locals = self.symbol_table.var_count("var")

        self.vm_writer.write_function(full_name, n_locals)

        # constructor
        if subroutine_kind == "constructor":
            field_count = self.symbol_table.var_count("field")

            self.vm_writer.write_push("constant", field_count)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)

        # method
        elif subroutine_kind == "method":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)

        self.compile_statements()

        self.consume("symbol", "}")


    def compile_var_dec(self):
        self.consume("keyword", "var")
        var_type = self.compile_type()

        _, name = self.consume("identifier")
        self.symbol_table.define(name, var_type, "var")

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            _, name = self.consume("identifier")
            self.symbol_table.define(name, var_type, "var")

        self.consume("symbol", ";")

    def compile_statements(self):
        while (
            self.match("keyword", "let") or
            self.match("keyword", "if") or
            self.match("keyword", "while") or
            self.match("keyword", "do") or
            self.match("keyword", "return")
        ):
            if self.match("keyword", "let"):
                self.compile_let()
            
            elif self.match("keyword", "if"):
                self.compile_if()

            elif self.match("keyword", "while"):
                self.compile_while()

            elif self.match("keyword", "do"):
                self.compile_do()

            elif self.match("keyword", "return"):
                self.compile_return()

            else:
                self.advance()
    
    def compile_return(self):
        self.consume("keyword", "return")

        if not self.match("symbol", ";"):
            self.compile_expression()
        else:
            # return void
            self.vm_writer.write_push("constant", 0)

        self.consume("symbol", ";")
        self.vm_writer.write_return()


    def compile_expression(self):
        self.compile_term()

        while self.match("symbol") and self.current_token()[1] in [
            "+", "-", "*", "/", "&", "|", "<", ">", "="
        ]:
            _, op = self.consume("symbol")
            self.compile_term()
            self.write_operator(op)
    
    def compile_term(self):
        token = self.current_token()

        if token is None:
            raise SyntaxError("Fim inesperado de tokens")

        token_type, value = token

        # integerConstant
        if token_type == "integerConstant":
            self.consume("integerConstant")
            self.vm_writer.write_push("constant", value)

        # stringConstant
        elif token_type == "stringConstant":
            self.consume("stringConstant")
            self.write_string_constant(value)

        # keywordConstant: true, false, null, this
        elif token_type == "keyword" and value in ["true", "false", "null", "this"]:
            self.consume("keyword")
            self.write_keyword_constant(value)

        # unaryOp term
        elif token_type == "symbol" and value in ["-", "~"]:
            _, op = self.consume("symbol")
            self.compile_term()

            if op == "-":
                self.vm_writer.write_arithmetic("neg")
            elif op == "~":
                self.vm_writer.write_arithmetic("not")

        # (expression)
        elif token_type == "symbol" and value == "(":
            self.consume("symbol", "(")
            self.compile_expression()
            self.consume("symbol", ")")

        # identifier
        elif token_type == "identifier":
            _, name = self.consume("identifier")

            if self.match("symbol", "["):
                raise NotImplementedError("Acesso a array ainda não implementado")

            elif self.match("symbol", "("):
                raise NotImplementedError("Chamada de subrotina sem classe ainda não implementada")

            elif self.match("symbol", "."):
                # reposiciona: já consumimos o primeiro identificador
                # aqui vamos tratar chamada Classe.funcao(...)
                self.consume("symbol", ".")
                _, second_name = self.consume("identifier")

                full_name = f"{name}.{second_name}"

                self.consume("symbol", "(")
                n_args = self.compile_expression_list()
                self.consume("symbol", ")")

                self.vm_writer.write_call(full_name, n_args)

            else:
                self.write_push_identifier(name)

        else:
            raise SyntaxError(f"Termo não suportado: {token}")
    
    def write_push_identifier(self, name):
        kind = self.symbol_table.kind_of(name)
        index = self.symbol_table.index_of(name)

        if kind is None:
            raise NameError(f"Identificador não encontrado na tabela de símbolos: {name}")

        segment = self.kind_to_segment(kind)
        self.vm_writer.write_push(segment, index)
    
    def write_pop_identifier(self, name):
        kind = self.symbol_table.kind_of(name)
        index = self.symbol_table.index_of(name)

        if kind is None:
            raise NameError(f"Identificador não encontrado na tabela de símbolos: {name}")

        segment = self.kind_to_segment(kind)
        self.vm_writer.write_pop(segment, index)

    def kind_to_segment(self, kind):
        if kind == "static":
            return "static"
        if kind == "field":
            return "this"
        if kind == "arg":
            return "argument"
        if kind == "var":
            return "local"

        raise ValueError(f"Kind inválido: {kind}")
    

    def compile_let(self):
        self.consume("keyword", "let")

        _, name = self.consume("identifier")

        if self.match("symbol", "["):
            raise NotImplementedError("Atribuição em array ainda não implementada")

        self.consume("symbol", "=")

        self.compile_expression()

        self.consume("symbol", ";")

        self.write_pop_identifier(name)

    def write_operator(self, op):
        if op == "+":
            self.vm_writer.write_arithmetic("add")
        elif op == "-":
            self.vm_writer.write_arithmetic("sub")
        elif op == "*":
            self.vm_writer.write_call("Math.multiply", 2)
        elif op == "/":
            self.vm_writer.write_call("Math.divide", 2)
        elif op == "&":
            self.vm_writer.write_arithmetic("and")
        elif op == "|":
            self.vm_writer.write_arithmetic("or")
        elif op == "<":
            self.vm_writer.write_arithmetic("lt")
        elif op == ">":
            self.vm_writer.write_arithmetic("gt")
        elif op == "=":
            self.vm_writer.write_arithmetic("eq")
        else:
            raise ValueError(f"Operador inválido: {op}")
    


    def compile_do(self):
        self.consume("keyword", "do")

        self.compile_subroutine_call()

        self.consume("symbol", ";")

        # descarta valor retornado
        self.vm_writer.write_pop("temp", 0)


    def compile_subroutine_call(self):
        _, first_name = self.consume("identifier")

        self.consume("symbol", ".")

        _, second_name = self.consume("identifier")

        full_name = f"{first_name}.{second_name}"

        self.consume("symbol", "(")

        n_args = self.compile_expression_list()

        self.consume("symbol", ")")

        self.vm_writer.write_call(full_name, n_args)

    
    def compile_expression_list(self):
        count = 0

        if self.match("symbol", ")"):
            return count

        self.compile_expression()
        count += 1

        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.compile_expression()
            count += 1

        return count
    

    def compile_while(self):
        count = self.while_count
        self.while_count += 1

        exp_label = f"WHILE_EXP{count}"
        end_label = f"WHILE_END{count}"

        self.vm_writer.write_label(exp_label)

        self.consume("keyword", "while")
        self.consume("symbol", "(")

        self.compile_expression()

        self.consume("symbol", ")")

        # se a condição for falsa, sai do while
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(end_label)

        self.consume("symbol", "{")

        self.compile_statements()

        self.consume("symbol", "}")

        self.vm_writer.write_goto(exp_label)
        self.vm_writer.write_label(end_label)

    def compile_if(self):
        count = self.if_count
        self.if_count += 1

        true_label = f"IF_TRUE{count}"
        false_label = f"IF_FALSE{count}"
        end_label = f"IF_END{count}"

        self.consume("keyword", "if")
        self.consume("symbol", "(")

        self.compile_expression()

        self.consume("symbol", ")")

        self.vm_writer.write_if(true_label)
        self.vm_writer.write_goto(false_label)
        self.vm_writer.write_label(true_label)

        self.consume("symbol", "{")
        self.compile_statements()
        self.consume("symbol", "}")

        if self.match("keyword", "else"):
            self.vm_writer.write_goto(end_label)
            self.vm_writer.write_label(false_label)

            self.consume("keyword", "else")
            self.consume("symbol", "{")
            self.compile_statements()
            self.consume("symbol", "}")

            self.vm_writer.write_label(end_label)

        else:
            self.vm_writer.write_label(false_label)

    
    def write_string_constant(self, value):
        self.vm_writer.write_push("constant", len(value))
        self.vm_writer.write_call("String.new", 1)

        for char in value:
            self.vm_writer.write_push("constant", ord(char))
            self.vm_writer.write_call("String.appendChar", 2)
    
    def write_keyword_constant(self, value):
        if value == "true":
            self.vm_writer.write_push("constant", 0)
            self.vm_writer.write_arithmetic("not")

        elif value == "false" or value == "null":
            self.vm_writer.write_push("constant", 0)

        elif value == "this":
            self.vm_writer.write_push("pointer", 0)

        else:
            raise ValueError(f"Keyword constant inválida: {value}")