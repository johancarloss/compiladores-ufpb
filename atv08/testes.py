import sys

from tests.ambiente import (
    can_run_linux_binaries,
    check_tool,
    has_gnu_as,
    preparar_diretorio_testes,
    run_with_docker,
    running_in_docker,
)
from tests.lexer_tests import executar_testes_lexer
from tests.parser_tests import executar_testes_parser
from tests.programa_tests import executar_testes_programa


def imprimir_cabecalho(has_as, has_ld, can_run):
    print("=" * 60)
    print(" Executando os testes do compilador EV (base EC2, x86-64)")
    print("=" * 60)
    print(f"GNU Assembler (as) disponivel: {'Sim' if has_as else 'Nao'}")
    print(f"GNU Linker (ld) disponivel:    {'Sim' if has_ld else 'Nao'}")
    print(f"Pode executar binarios Linux:  {'Sim' if can_run else 'Nao'}")
    print("-" * 60)


def main():
    if not has_gnu_as() and not running_in_docker():
        return run_with_docker()

    tests_dir = preparar_diretorio_testes()
    has_as = has_gnu_as()
    has_ld = check_tool("ld")
    can_run = can_run_linux_binaries()

    imprimir_cabecalho(has_as, has_ld, can_run)

    lexer_sucessos, lexer_total = executar_testes_lexer()
    parser_sucessos, parser_total = executar_testes_parser()
    programa_sucessos, programa_total = executar_testes_programa(
        tests_dir=tests_dir,
        has_as=has_as,
        has_ld=has_ld,
        can_run=can_run,
    )

    sucessos = lexer_sucessos + parser_sucessos + programa_sucessos
    total = lexer_total + parser_total + programa_total
    print(f"Resultado final: {sucessos}/{total} testes passaram com sucesso.")
    return 0 if sucessos == total else 1


if __name__ == "__main__":
    sys.exit(main())
