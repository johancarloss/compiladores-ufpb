from lexer import lex
from parser import parse
from semantico import VariavelNaoDeclarada, verificar


SEMANTICOS_VALIDOS = [
    ("resultado constante", "{ return 42; }"),
    ("declara e usa variavel", "x = 10;\n{ return x; }"),
    ("atribuicao a variavel declarada", "x = 10;\n{ x = x + 5; return x; }"),
    ("if e while com variaveis declaradas", "n = 1;\nm = 5;\n{ while n < m { n = n + 1; } return n; }"),
]

SEMANTICOS_INVALIDOS = [
    ("atribui a variavel nao declarada", "x = 1;\n{ y = 5; return x; }", "y"),
    ("expressao usa variavel nao declarada", "x = 1;\n{ x = x + z; return x; }", "z"),
    ("nao declarada dentro do if", "a = 1;\n{ if a < 10 { a = b; } else { a = 0; } return a; }", "b"),
    ("resultado usa variavel nao declarada", "{ return z; }", "z"),
]


def executar_testes_semanticos():
    print("[Semantico]")
    sucessos = 0
    total = len(SEMANTICOS_VALIDOS) + len(SEMANTICOS_INVALIDOS)

    for nome, fonte in SEMANTICOS_VALIDOS:
        print(f"Semantico valido: {nome}")
        try:
            programa = parse_fonte(fonte)
            verificado = verificar(programa)
            assert verificado is programa, "verificar deve retornar o programa validado"
        except Exception as e:
            print(f"  [FALHA] {e}")
        else:
            print("  [PASS]")
            sucessos += 1
        print("-" * 60)

    for nome, fonte, variavel in SEMANTICOS_INVALIDOS:
        print(f"Semantico invalido: {nome}")
        try:
            verificar(parse_fonte(fonte))
        except VariavelNaoDeclarada as e:
            assert e.nome == variavel, f"esperava erro da variavel {variavel}, recebeu {e.nome}"
            print(f"  [PASS] Erro semantico detectado: {e}")
            sucessos += 1
        except Exception as e:
            print(f"  [FALHA] Erro inesperado: {e}")
        else:
            print("  [FALHA] Programa semanticamente invalido foi aceito")
        print("-" * 60)

    print(f"[Semantico] Resultado: {sucessos}/{total}")
    print("-" * 60)
    return sucessos, total


def parse_fonte(fonte):
    lx = lex(fonte)
    if lx.houve_erro:
        raise AssertionError(f"erro lexico inesperado na posicao {lx.erro_pos}: {lx.erro_char}")
    return parse(lx.tokens)
