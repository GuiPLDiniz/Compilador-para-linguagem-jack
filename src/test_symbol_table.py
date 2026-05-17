from symbol_table import SymbolTable

table = SymbolTable()

table.define("x", "int", "static")
table.define("y", "boolean", "field")

table.start_subroutine()

table.define("a", "int", "arg")
table.define("b", "int", "var")

print(table.kind_of("x"))
print(table.index_of("x"))

print(table.kind_of("a"))
print(table.index_of("a"))