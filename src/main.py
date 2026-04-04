import sys
from pathlib import Path


KEYWORDS = {
    "class", "constructor", "function", "method",
    "field", "static", "var",
    "int", "char", "boolean", "void",
    "true", "false", "null", "this",
    "let", "do", "if", "else", "while", "return"
}
SYMBOLS = set("{}()[].,;+-*/&|<>=~")

def remove_comments(content):
    i = 0
    n = len(content)
    result = ""

    while i < n:
        # comentário de linha //
        if content[i:i+2] == "//":
            i += 2
            while i < n and content[i] != "\n":
                i += 1

        # comentário de bloco /* */
        elif content[i:i+2] == "/*":
            i += 2
            while i < n-1 and content[i:i+2] != "*/":
                i += 1
            i += 2  # pula o */

        else:
            result += content[i]
            i += 1

    return result

def classify_token(token):
    if token in KEYWORDS:
        return "keyword"
    elif token.isdigit():
        return "integerConstant"
    else:
        return "identifier"


def basic_tokenize(content):
    tokens = []
    current = ""
    i = 0
    n = len(content)

    while i < n:
        char = content[i]

        # STRING CONSTANT
        if char == '"':
            i += 1
            string_value = ""

            while i < n and content[i] != '"':
                string_value += content[i]
                i += 1

            tokens.append(("stringConstant", string_value))
            i += 1
            continue

        # ESPAÇO
        if char.isspace():
            if current:
                token_type = classify_token(current)
                tokens.append((token_type, current))
                current = ""
            i += 1
            continue

        # SÍMBOLO
        if char in SYMBOLS:
            if current:
                token_type = classify_token(current)
                tokens.append((token_type, current))
                current = ""
            tokens.append(("symbol", char))
            i += 1
            continue

        # CONTINUA PALAVRA
        current += char
        i += 1

    if current:
        token_type = classify_token(current)
        tokens.append((token_type, current))

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
        content = remove_comments(content)
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