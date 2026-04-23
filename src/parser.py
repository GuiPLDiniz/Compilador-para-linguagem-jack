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