import sys

from tests.ambiente import run_with_docker
from tests.lexer_tests import executar_testes_lexer
from tests.parser_tests import executar_testes_parser


def imprimir_cabecalho():
    print("=" * 60)
    print(" Executando os testes da linguagem EV")
    print("=" * 60)
    print("-" * 60)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--docker":
        return run_with_docker()

    imprimir_cabecalho()

    lexer_sucessos, lexer_total = executar_testes_lexer()
    parser_sucessos, parser_total = executar_testes_parser()

    sucessos = lexer_sucessos + parser_sucessos
    total = lexer_total + parser_total
    print(f"Resultado final: {sucessos}/{total} testes passaram com sucesso.")
    return 0 if sucessos == total else 1


if __name__ == "__main__":
    sys.exit(main())
