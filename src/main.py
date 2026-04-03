import sys
from pathlib import Path


def main():
    # Verifica se o usuário informou o caminho do arquivo
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <caminho-do-arquivo.jack>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    # Verifica se o arquivo existe
    if not file_path.exists():
        print(f"Erro: o arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)

    # Verifica se o arquivo tem extensão .jack
    if file_path.suffix.lower() != ".jack":
        print("Erro: o arquivo informado deve ter extensão .jack")
        sys.exit(1)

    # Lê o conteúdo do arquivo
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    # Exibe o conteúdo lido
    print("Arquivo lido com sucesso.\n")
    
    # Define o nome do arquivo de saída
    output_path = file_path.with_name(file_path.stem + "T.xml")

    # Conteúdo inicial do XML (ainda sem tokens reais)
    xml_content = "<tokens>\n</tokens>"

    try:
        output_path.write_text(xml_content, encoding="utf-8")
    except Exception as e:
        print(f"Erro ao escrever o arquivo XML: {e}")
        sys.exit(1)

    print(f"Arquivo XML gerado: {output_path}")



if __name__ == "__main__":
    main()