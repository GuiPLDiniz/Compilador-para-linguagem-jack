from tokenizer import remove_comments, basic_tokenize
from compilation_engine import CompilationEngine

content = """
class Square {
    method void test() {
        do move();
        return;
    }

    method void move() {
        return;
    }
}
"""

content = remove_comments(content)
tokens = basic_tokenize(content)

engine = CompilationEngine(tokens)
engine.compile_class()

print(engine.get_vm_code())