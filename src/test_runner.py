from pathlib import Path


def compare_files(generated_file, official_file):
    """
    Compara dois arquivos linha por linha.
    Retorna True se forem idênticos.
    Caso contrário, mostra a primeira diferença encontrada e retorna False.
    """
    generated_path = Path(generated_file)
    official_path = Path(official_file)

    if not generated_path.exists():
        print(f"[ERRO] Arquivo gerado não encontrado: {generated_path}")
        return False

    if not official_path.exists():
        print(f"[ERRO] Arquivo oficial não encontrado: {official_path}")
        return False

    generated_lines = generated_path.read_text(encoding="utf-8").splitlines()
    official_lines = official_path.read_text(encoding="utf-8").splitlines()

    if generated_lines == official_lines:
        print(f"[OK] Arquivos idênticos: {generated_path.name}")
        return True

    print(f"[ERRO] Diferenças encontradas em {generated_path.name}")

    max_len = max(len(generated_lines), len(official_lines))

    for i in range(max_len):
        generated_line = generated_lines[i] if i < len(generated_lines) else "<linha inexistente>"
        official_line = official_lines[i] if i < len(official_lines) else "<linha inexistente>"

        if generated_line != official_line:
            print(f"  Linha {i + 1}:")
            print(f"    Gerado : {generated_line}")
            print(f"    Oficial: {official_line}")
            return False

    return False


def run_all_tests():
    """
    Executa a comparação de todos os arquivos XML gerados
    com seus respectivos arquivos oficiais.
    """
    test_cases = [
        ("tests/ArrayTest/MainT.xml", "tests/ArrayTest/MainT_oficial.xml"),

        ("tests/ExpressionLessSquare/MainT.xml", "tests/ExpressionLessSquare/MainT_oficial.xml"),
        ("tests/ExpressionLessSquare/SquareT.xml", "tests/ExpressionLessSquare/SquareT_oficial.xml"),
        ("tests/ExpressionLessSquare/SquareGameT.xml", "tests/ExpressionLessSquare/SquareGameT_oficial.xml"),

        ("tests/Square/MainT.xml", "tests/Square/MainT_oficial.xml"),
        ("tests/Square/SquareT.xml", "tests/Square/SquareT_oficial.xml"),
        ("tests/Square/SquareGameT.xml", "tests/Square/SquareGameT_oficial.xml"),
    ]

    total = len(test_cases)
    passed = 0

    print("Iniciando validação dos arquivos XML...\n")

    for generated, official in test_cases:
        if compare_files(generated, official):
            passed += 1

    print("\nResumo:")
    print(f"  Testes aprovados: {passed}/{total}")

    if passed == total:
        print("  Todos os arquivos estão idênticos aos oficiais.")
    else:
        print("  Existem diferenças em um ou mais arquivos.")


if __name__ == "__main__":
    run_all_tests()