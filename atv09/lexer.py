import sys
from enum import Enum


class TokenTipo(Enum):
    NUMERO = "Numero"
    IDENT = "Ident"
    PAREN_ESQ = "ParenEsq"
    PAREN_DIR = "ParenDir"
    CHAVE_ESQ = "ChaveEsq"
    CHAVE_DIR = "ChaveDir"
    SOMA = "Soma"
    SUB = "Sub"
    MULT = "Mult"
    DIV = "Div"
    IGUAL = "Igual"
    PONTO_VIRGULA = "PontoVirgula"
    MENOR = "Menor"
    MAIOR = "Maior"
    IGUALDADE = "Igualdade"
    IF = "If"
    ELSE = "Else"
    WHILE = "While"
    RETURN = "Return"


PALAVRAS_CHAVE = {
    "if": TokenTipo.IF,
    "else": TokenTipo.ELSE,
    "while": TokenTipo.WHILE,
    "return": TokenTipo.RETURN,
}


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
    "{": TokenTipo.CHAVE_ESQ,
    "}": TokenTipo.CHAVE_DIR,
    "+": TokenTipo.SOMA,
    "-": TokenTipo.SUB,
    "*": TokenTipo.MULT,
    "/": TokenTipo.DIV,
    ";": TokenTipo.PONTO_VIRGULA,
    "<": TokenTipo.MENOR,
    ">": TokenTipo.MAIOR,
}


def lex(fonte):
    lx = Lexico()
    i = 0
    n = len(fonte)
    while i < n:
        c = fonte[i]
        if c in ESPACOS:
            i += 1
        elif c.isdigit():
            # agrupa todos os digitos seguidos em um unico numero
            inicio = i
            while i < n and fonte[i].isdigit():
                i += 1
            if i < n and fonte[i].isalpha():
                lx.houve_erro = True
                lx.erro_pos = i
                lx.erro_char = fonte[i]
                return lx
            lx.tokens.append(Token(TokenTipo.NUMERO, fonte[inicio:i], inicio))
        elif c.isalpha():
            inicio = i
            while i < n and fonte[i].isalnum():
                i += 1
            lexema = fonte[inicio:i]
            # se o lexema for uma palavra-chave, gera o token correspondente;
            # caso contrario e um identificador comum
            tipo = PALAVRAS_CHAVE.get(lexema, TokenTipo.IDENT)
            lx.tokens.append(Token(tipo, lexema, inicio))
        elif c == "=":
            # precisa olhar o proximo char pra diferenciar '=' de '=='
            if i + 1 < n and fonte[i + 1] == "=":
                lx.tokens.append(Token(TokenTipo.IGUALDADE, "==", i))
                i += 2
            else:
                lx.tokens.append(Token(TokenTipo.IGUAL, "=", i))
                i += 1
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
        print(f"Uso: {sys.argv[0]} <arquivo.ev>", file=sys.stderr)
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
