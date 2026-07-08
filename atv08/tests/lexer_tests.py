from lexer import TokenTipo, lex


LEXER_CASES = [
    (
        "x = 10;\n= x",
        [
            (TokenTipo.IDENT, "x"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.NUMERO, "10"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.IDENT, "x"),
        ],
    ),
    (
        "altura2 = 30;\nlargura = altura2 + 5;\n= largura",
        [
            (TokenTipo.IDENT, "altura2"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.NUMERO, "30"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.IDENT, "largura"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.IDENT, "altura2"),
            (TokenTipo.SOMA, "+"),
            (TokenTipo.NUMERO, "5"),
            (TokenTipo.PONTO_VIRGULA, ";"),
            (TokenTipo.IGUAL, "="),
            (TokenTipo.IDENT, "largura"),
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
