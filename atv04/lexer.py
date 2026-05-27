import sys
from enum import Enum


class TokenTipo(Enum):
    NUMERO = "Numero"
    PAREN_ESQ = "ParenEsq"
    PAREN_DIR = "ParenDir"
    SOMA = "Soma"
    SUB = "Sub"
    MULT = "Mult"
    DIV = "Div"


class Token:
    def __init__(self, tipo, lexema, posicao):
        self.tipo = tipo
        self.lexema = lexema
        self.posicao = posicao

    def __str__(self):
        return f'<{self.tipo.value}, "{self.lexema}", {self.posicao}>'


class Lexico:
    def __init__(self):
        self.tokens = []
        self.houve_erro = False
        self.erro_pos = None
        self.erro_char = None


ESPACOS = " \t\n\r"

OPERADORES = {
    "(": TokenTipo.PAREN_ESQ,
    ")": TokenTipo.PAREN_DIR,
    "+": TokenTipo.SOMA,
    "-": TokenTipo.SUB,
    "*": TokenTipo.MULT,
    "/": TokenTipo.DIV,
}


def lex(fonte):
    lx = Lexico()
    i, n = 0, len(fonte)
    while i < n:
        c = fonte[i]
        if c in ESPACOS:
            i += 1
        elif "0" <= c <= "9":
            inicio = i
            while i < n and "0" <= fonte[i] <= "9":
                i += 1
            lx.tokens.append(Token(TokenTipo.NUMERO, fonte[inicio:i], inicio))
        elif c in OPERADORES:
            lx.tokens.append(Token(OPERADORES[c], c, i))
            i += 1
        else:
            lx.houve_erro = True
            lx.erro_pos = i
            lx.erro_char = c
            return lx
    return lx


def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <arquivo.ec1>", file=sys.stderr)
        return 1

    try:
        with open(sys.argv[1], "r") as f:
            fonte = f.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir '{sys.argv[1]}'", file=sys.stderr)
        return 1

    lx = lex(fonte)
    for tok in lx.tokens:
        print(tok)

    if lx.houve_erro:
        print(f"Erro léxico na posição {lx.erro_pos}: "
              f"caractere inválido '{lx.erro_char}'")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
