class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

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