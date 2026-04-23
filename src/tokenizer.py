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

#funcao para aplicar o escape de caracteres
def escape_xml(value):
    if value == "<":
        return "&lt;"
    elif value == ">":
        return "&gt;"
    elif value == "&":
        return "&amp;"
    elif value == '"':
        return "&quot;"
    else:
        return value

def tokens_to_xml(tokens):
    lines = ["<tokens>"]

    for token_type, value in tokens:
        escaped_value = escape_xml(value)
        lines.append(f"<{token_type}> {escaped_value} </{token_type}>")

    lines.append("</tokens>")
    return "\n".join(lines) + "\n"