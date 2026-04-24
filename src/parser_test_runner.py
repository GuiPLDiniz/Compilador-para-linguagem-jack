from pathlib import Path


def normalize_xml(content):
    return "\n".join(line.lstrip() for line in content.splitlines())


def compare_files(generated_file, official_file):
    generated_path = Path(generated_file)
    official_path = Path(official_file)

    if not generated_path.exists():
        print(f"[ERRO] Arquivo gerado não encontrado: {generated_path}")
        return False

    if not official_path.exists():
        print(f"[ERRO] Arquivo oficial não encontrado: {official_path}")
        return False

    generated = normalize_xml(generated_path.read_text(encoding="utf-8"))
    official = normalize_xml(official_path.read_text(encoding="utf-8"))

    if generated == official:
        print(f"[OK] {generated_path}")
        return True

    print(f"[ERRO] Diferença em {generated_path}")

    gen_lines = generated.splitlines()
    off_lines = official.splitlines()

    for i in range(max(len(gen_lines), len(off_lines))):
        g = gen_lines[i] if i < len(gen_lines) else "<linha inexistente>"
        o = off_lines[i] if i < len(off_lines) else "<linha inexistente>"

        if g != o:
            print(f"  Linha {i+1}:")
            print(f"    Gerado : {g}")
            print(f"    Oficial: {o}")
            break

    return False


def run_all_tests():
    test_cases = [

        #ArrayTest
        ("tests/ArrayTest/MainP.xml", "tests/ArrayTest/MainP_oficial.xml"),
        #Square
        ("tests/Square/MainP.xml", "tests/Square/MainP_oficial.xml"),
        ("tests/Square/SquareP.xml", "tests/Square/SquareP_oficial.xml"),
        ("tests/Square/SquareGameP.xml", "tests/Square/SquareGameP_oficial.xml"),
        #ExpressionLessSquare
        ("tests/ExpressionLessSquare/MainP.xml", "tests/ExpressionLessSquare/MainP_oficial.xml"),
        ("tests/ExpressionLessSquare/SquareP.xml", "tests/ExpressionLessSquare/SquareP_oficial.xml"),
        ("tests/ExpressionLessSquare/SquareGameP.xml", "tests/ExpressionLessSquare/SquareGameP_oficial.xml"),
    ]

    total = len(test_cases)
    passed = 0

    print("Validando parser...\n")

    for generated, official in test_cases:
        if compare_files(generated, official):
            passed += 1

    print("\nResumo:")
    print(f"  {passed}/{total} testes passaram")

    if passed == total:
        print("  ✔ Parser validado com sucesso!")
    else:
        print("  ✖ Existem diferenças")


if __name__ == "__main__":
    run_all_tests()