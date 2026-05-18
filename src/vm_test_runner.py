from pathlib import Path
import subprocess


TEST_DIRECTORIES = [
    "tests/ArrayTest",
    "tests/ExpressionLessSquare",
    "tests/Square"
]


def run_test(test_dir):
    print(f"\nTestando: {test_dir}")

    result = subprocess.run(
        ["python", "src/main.py", test_dir],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ERRO] Falha na compilação")
        print(result.stderr)
        return False

    print(result.stdout)

    vm_files = list(Path(test_dir).glob("*.vm"))

    if not vm_files:
        print("[ERRO] Nenhum arquivo .vm gerado")
        return False

    for vm_file in vm_files:
        print(f"[OK] {vm_file.name}")

    return True


def main():
    success = 0

    print("Validando geração de código VM...")

    for test_dir in TEST_DIRECTORIES:
        if run_test(test_dir):
            success += 1

    print("\nResumo:")
    print(f"{success}/{len(TEST_DIRECTORIES)} testes passaram")

    if success == len(TEST_DIRECTORIES):
        print("Compilador VM validado com sucesso!")
    else:
        print("Alguns testes falharam.")


if __name__ == "__main__":
    main()