from tokenizer import remove_comments, basic_tokenize
from compilation_engine import CompilationEngine

content = """
class Main {
    static int x, y;
    field boolean ativo;
}
"""

content = remove_comments(content)
tokens = basic_tokenize(content)

engine = CompilationEngine(tokens)
engine.compile_class()

print(engine.class_name)
print(engine.symbol_table.kind_of("x"), engine.symbol_table.index_of("x"))
print(engine.symbol_table.kind_of("y"), engine.symbol_table.index_of("y"))
print(engine.symbol_table.kind_of("ativo"), engine.symbol_table.index_of("ativo"))