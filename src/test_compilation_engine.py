from tokenizer import remove_comments, basic_tokenize
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
engine.compile_class()

print(engine.get_vm_code())