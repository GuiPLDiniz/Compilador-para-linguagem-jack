import sys
from pathlib import Path

SYMBOLS = set("{}()[].,;+-*/&|<>=~")


def basic_tokenize(content):
    tokens = []
    current = ""

    for char in content:
        # Se encontrar espaço em branco, fecha o token atual
        if char.isspace():
            if current:
                tokens.append(("token", current))
                current = ""
            continue

        # Se encontrar símbolo, fecha o token atual e adiciona o símbolo
        if char in SYMBOLS:
            if current:
                tokens.append(("token", current))
                current = ""
            tokens.append(("symbol", char))
            continue

        # Caso contrário, continua formando o token
        current += char

    # Adiciona o último token, se existir
    if current:
        tokens.append(("token", current))

    return tokens


def tokens_to_xml(tokens):
    lines = ["<tokens>"]

    for token_type, value in tokens:
        lines.append(f"<{token_type}> {value} </{token_type}>")

    lines.append("</tokens>")
    return "\n".join(lines)


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
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    print("Arquivo lido com sucesso.")

    tokens = basic_tokenize(content)
    xml_content = tokens_to_xml(tokens)

    output_path = file_path.with_name(file_path.stem + "T.xml")

    try:
        output_path.write_text(xml_content, encoding="utf-8")
    except Exception as e:
        print(f"Erro ao escrever o arquivo XML: {e}")
        sys.exit(1)

    print(f"Arquivo XML gerado: {output_path}")


if __name__ == "__main__":
    main()