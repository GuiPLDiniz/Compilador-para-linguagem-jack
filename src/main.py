import sys
from pathlib import Path
from tokenizer import remove_comments, basic_tokenize, tokens_to_xml
from parser import Parser




def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <caminho-do-arquivo.jack>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"Erro: o arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)

    if file_path.suffix.lower() != ".jack":
        print("Erro: o arquivo informado deve ter extensão .jack")
        sys.exit(1)

    try:
        content = file_path.read_text(encoding="utf-8")
        content = remove_comments(content)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    print("Arquivo lido com sucesso.")

    tokens = basic_tokenize(content)

    parser = Parser(tokens)
    parser.compile_class()
    xml_content = parser.get_xml()

    output_path = file_path.with_name(file_path.stem + "P.xml")

    try:
        output_path.write_text(xml_content, encoding="utf-8")
    except Exception as e:
        print(f"Erro ao escrever o arquivo XML: {e}")
        sys.exit(1)

    print(f"Arquivo XML gerado: {output_path}")


if __name__ == "__main__":
    main()