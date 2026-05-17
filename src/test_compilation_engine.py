from tokenizer import remove_comments, basic_tokenize
from compilation_engine import CompilationEngine

content = """
class Main {
    function void main(int x, boolean flag) {
        var int i, j;
        return;
    }
}
"""

content = remove_comments(content)
tokens = basic_tokenize(content)

engine = CompilationEngine(tokens)
engine.compile_class()

print(engine.get_vm_code())
print(engine.symbol_table.kind_of("x"), engine.symbol_table.index_of("x"))
print(engine.symbol_table.kind_of("flag"), engine.symbol_table.index_of("flag"))
print(engine.symbol_table.kind_of("i"), engine.symbol_table.index_of("i"))
print(engine.symbol_table.kind_of("j"), engine.symbol_table.index_of("j"))