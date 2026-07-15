from lexer import lex
from parser import ErroSintatico, parse
from arvore import If, While, Atrib, OpBin, Op


PARSER_INVALIDOS = [
    ("corpo sem return", "{ x = 1; }"),
    ("if sem else", "{ if 1 < 2 { } return 0; }"),
    ("while sem chaves no corpo", "{ while 1 < 2 return 0; }"),
    ("declaracao sem ponto-e-virgula", "x = 10\n{ return x; }"),
    ("tokens depois do fim", "{ return 1; } x = 2;"),
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


def testar_menor_programa(programa):
    assert len(programa.declaracoes) == 0
    assert len(programa.comandos) == 0
    assert getattr(programa.resultado, "op", None) == Op.MULT


def testar_if_no_corpo(programa):
    assert len(programa.declaracoes) == 1
    assert len(programa.comandos) == 1
    cmd = programa.comandos[0]
    assert isinstance(cmd, If), "comando deve ser um If"
    assert isinstance(cmd.cond, OpBin) and cmd.cond.op == Op.MENOR
    assert len(cmd.corpo_then) == 1 and isinstance(cmd.corpo_then[0], Atrib)
    assert len(cmd.corpo_else) == 1 and isinstance(cmd.corpo_else[0], Atrib)


def testar_while_no_corpo(programa):
    assert len(programa.comandos) == 1
    cmd = programa.comandos[0]
    assert isinstance(cmd, While), "comando deve ser um While"
    assert isinstance(cmd.cond, OpBin) and cmd.cond.op == Op.MENOR
    assert len(cmd.corpo) == 2, "corpo do while deve ter dois comandos"


def testar_comparacao_precedencia(programa):
    # 2 + 3 < 10 deve virar (2 + 3) < 10, a comparacao no nivel de fora
    res = programa.resultado
    assert res.op == Op.MENOR, "comparacao deve ficar no nivel externo"
    assert res.esq.op == Op.SOMA, "a soma deve ficar abaixo da comparacao"


PARSER_VALIDOS = [
    ("menor programa", "{ return 7 * 6; }", testar_menor_programa),
    (
        "if no corpo",
        "x = 1;\n{ if x < 2 { x = 10; } else { x = 20; } return x; }",
        testar_if_no_corpo,
    ),
    (
        "while no corpo",
        "n = 0;\n{ while n < 3 { n = n + 1; n = n; } return n; }",
        testar_while_no_corpo,
    ),
    (
        "precedencia da comparacao",
        "{ return 2 + 3 < 10; }",
        testar_comparacao_precedencia,
    ),
]
