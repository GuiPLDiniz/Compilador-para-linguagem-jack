from tokenizer import remove_comments, basic_tokenize
from compilation_engine import CompilationEngine

content = """
class Main {
    function void main() {
        var int x, y;
        let x = 10;
        let y = x + 2;
        return;
    }
}
"""

content = remove_comments(content)
tokens = basic_tokenize(content)

engine = CompilationEngine(tokens)
engine.compile_class()

print(engine.get_vm_code())