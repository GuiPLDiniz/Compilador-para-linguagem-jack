import sys
from pathlib import Path

from tokenizer import remove_comments, basic_tokenize

from compilation_engine import CompilationEngine


def compile_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        content = remove_comments(content)

    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return

    tokens = basic_tokenize(content)

    engine = CompilationEngine(tokens)
    engine.compile_class()

    vm_content = engine.get_vm_code()

    output_path = file_path.with_suffix(".vm")

    try:
        output_path.write_text(vm_content, encoding="utf-8")

    except Exception as e:
        print(f"Erro ao escrever VM: {e}")
        return

    print(f"[OK] Gerado: {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <arquivo.jack | diretorio>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Caminho não encontrado: {input_path}")
        sys.exit(1)

    # arquivo único
    if input_path.is_file():

        if input_path.suffix.lower() != ".jack":
            print("O arquivo deve possuir extensão .jack")
            sys.exit(1)

        compile_file(input_path)

    # diretório
    elif input_path.is_dir():

        jack_files = list(input_path.rglob("*.jack"))

        if not jack_files:
            print("Nenhum arquivo .jack encontrado.")
            sys.exit(1)

        for file_path in jack_files:
            compile_file(file_path)


if __name__ == "__main__":
    main()