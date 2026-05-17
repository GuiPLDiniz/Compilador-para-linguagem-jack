from tokenizer import basic_tokenize, remove_comments
from compilation_engine import CompilationEngine

content = """
class Main {
    function void main() {
        return;
    }
}
"""

content = remove_comments(content)
tokens = basic_tokenize(content)

engine = CompilationEngine(tokens)

print(engine.current_token())
engine.advance()
print(engine.current_token())