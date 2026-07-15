from lexer import TokenTipo, lex


LEXER_CASES = [
    (
        "{ return 42; }",
        [
            (TokenTipo.CHAVE_ESQ, "{"),
            (TokenTipo.RETURN, "return"),
            (TokenTipo.NUMERO, "42"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.CHAVE_DIR, "}"),
        ],
    ),
    (
        "if x < 10 { x = 1; } else { x = 0; }",
        [
            (TokenTipo.IF, "if"),
            (TokenTipo.IDENT, "x"),
            (TokenTipo.MENOR, "<"),
            (TokenTipo.NUMERO, "10"),
            (TokenTipo.CHAVE_ESQ, "{"),
            (TokenTipo.IDENT, "x"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.NUMERO, "1"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.CHAVE_DIR, "}"),
            (TokenTipo.ELSE, "else"),
            (TokenTipo.CHAVE_ESQ, "{"),
            (TokenTipo.IDENT, "x"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.NUMERO, "0"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.CHAVE_DIR, "}"),
        ],
    ),
    (
        "x = 1; y == 2 while",
        [
            (TokenTipo.IDENT, "x"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.NUMERO, "1"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.IDENT, "y"),
            (TokenTipo.IGUALDADE, "=="),
            (TokenTipo.NUMERO, "2"),
            (TokenTipo.WHILE, "while"),
        ],
    ),
]

LEXER_ERRORS = [
    "237abc",
    "9valor = 10;",
]


def executar_testes_lexer():
    print("[Lexer]")
    sucessos = 0
    total = len(LEXER_CASES) + len(LEXER_ERRORS)

    for i, (fonte, esperado) in enumerate(LEXER_CASES, 1):
        print(f"Lexer valido {i}/{len(LEXER_CASES)}")
        lx = lex(fonte)
        obtido = [(tok.tipo, tok.lexema) for tok in lx.tokens]
        if lx.houve_erro:
            print(f"  [FALHA] Erro lexico inesperado na posicao {lx.erro_pos}: '{lx.erro_char}'")
        elif obtido != esperado:
            print(f"  [FALHA] Tokens obtidos: {obtido}")
            print(f"          Tokens esperados: {esperado}")
        else:
            print("  [PASS] Tokens reconhecidos corretamente")
            sucessos += 1
        print("-" * 60)

    for i, fonte in enumerate(LEXER_ERRORS, 1):
        print(f"Lexer invalido {i}/{len(LEXER_ERRORS)}: '{fonte}'")
        lx = lex(fonte)
        if lx.houve_erro:
            print(f"  [PASS] Erro lexico detectado na posicao {lx.erro_pos}: '{lx.erro_char}'")
            sucessos += 1
        else:
            print("  [FALHA] Entrada invalida aceita pelo lexer")
        print("-" * 60)

    print(f"[Lexer] Resultado: {sucessos}/{total}")
    print("-" * 60)
    return sucessos, total
