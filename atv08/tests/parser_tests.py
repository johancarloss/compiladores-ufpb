from lexer import lex
from parser import ErroSintatico, parse


PARSER_INVALIDOS = [
    ("sem resultado final", "x = 10;"),
    ("declaracao sem ponto-e-virgula", "x = 10\n= x"),
    ("declaracao sem expressao", "x = ;\n= x"),
    ("resultado final com ponto-e-virgula sobrando", "x = 10;\n= x;"),
    ("tokens depois do resultado final", "= 10\nx = 2;"),
]


def executar_testes_parser():
    print("[Parser]")
    sucessos = 0
    total = len(PARSER_VALIDOS) + len(PARSER_INVALIDOS)

    for nome, fonte, testar_programa in PARSER_VALIDOS:
        print(f"Parser valido: {nome}")
        try:
            programa = parse_fonte(fonte)
            testar_programa(programa)
        except Exception as e:
            print(f"  [FALHA] {e}")
        else:
            print("  [PASS]")
            sucessos += 1
        print("-" * 60)

    for nome, fonte in PARSER_INVALIDOS:
        print(f"Parser invalido: {nome}")
        try:
            parse_fonte(fonte)
        except ErroSintatico as e:
            print(f"  [PASS] Erro sintatico detectado: {e}")
            sucessos += 1
        except Exception as e:
            print(f"  [FALHA] Erro inesperado: {e}")
        else:
            print("  [FALHA] Entrada invalida aceita pelo parser")
        print("-" * 60)

    print(f"[Parser] Resultado: {sucessos}/{total}")
    print("-" * 60)
    return sucessos, total


def parse_fonte(fonte):
    lx = lex(fonte)
    if lx.houve_erro:
        raise AssertionError(f"erro lexico inesperado na posicao {lx.erro_pos}: {lx.erro_char}")
    return parse(lx.tokens)


def verificar_programa_base(programa):
    assert hasattr(programa, "declaracoes"), "parse deve retornar um Programa com declaracoes"
    assert hasattr(programa, "resultado"), "parse deve retornar um Programa com resultado"


def testar_resultado_sem_declaracoes(programa):
    verificar_programa_base(programa)
    assert len(programa.declaracoes) == 0, "programa sem declaracoes deve ter lista vazia"
    assert getattr(programa.resultado, "valor", None) == 42, "resultado final deve ser Const(42)"


def testar_uma_declaracao_e_resultado(programa):
    verificar_programa_base(programa)
    assert len(programa.declaracoes) == 1, "programa deve ter uma declaracao"
    decl = programa.declaracoes[0]
    assert decl.nome == "x", "declaracao deve ser da variavel x"
    assert getattr(decl.exp, "valor", None) == 10, "expressao da declaracao deve ser Const(10)"
    assert getattr(programa.resultado, "nome", None) == "x", "resultado final deve ser Var('x')"


def testar_declaracoes_preservam_precedencia(programa):
    verificar_programa_base(programa)
    assert len(programa.declaracoes) == 2, "programa deve ter duas declaracoes"
    decl_x = programa.declaracoes[0]
    assert decl_x.nome == "x", "primeira declaracao deve ser x"
    assert getattr(decl_x.exp, "op", None).value == "+", "expressao de x deve somar no nivel externo"
    assert getattr(decl_x.exp.dir, "op", None).value == "*", (
        "multiplicacao deve ficar abaixo da soma por precedencia"
    )
    assert getattr(programa.resultado, "nome", None) == "y", "resultado final deve ser Var('y')"


PARSER_VALIDOS = [
    ("resultado sem declaracoes", "= 42", testar_resultado_sem_declaracoes),
    ("uma declaracao e resultado", "x = 10;\n= x", testar_uma_declaracao_e_resultado),
    (
        "declaracoes preservam precedencia",
        "x = 7 + 5 * 3;\ny = x - 2;\n= y",
        testar_declaracoes_preservam_precedencia,
    ),
]
