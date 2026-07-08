import sys

from tests.ambiente import run_with_docker
from tests.geracao_tests import executar_testes_geracao
from tests.lexer_tests import executar_testes_lexer
from tests.parser_tests import executar_testes_parser
from tests.semantico_tests import executar_testes_semanticos


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
    semantico_sucessos, semantico_total = executar_testes_semanticos()
    geracao_sucessos, geracao_total = executar_testes_geracao()

    sucessos = lexer_sucessos + parser_sucessos + semantico_sucessos + geracao_sucessos
    total = lexer_total + parser_total + semantico_total + geracao_total
    print(f"Resultado final: {sucessos}/{total} testes passaram com sucesso.")
    return 0 if sucessos == total else 1


if __name__ == "__main__":
    sys.exit(main())
