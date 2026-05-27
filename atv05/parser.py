from arvore import Const, OpBin, Op
from lexer import TokenTipo


class ErroSintatico(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def proximo_token(self):
        if self.pos >= len(self.tokens):
            raise ErroSintatico("fim inesperado da entrada")
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def olhar_token(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def verifica_token(self, tipo):
        tok = self.proximo_token()
        if tok.tipo != tipo:
            raise ErroSintatico(f"esperava {tipo.value}, encontrou '{tok.lexema}'")
        return tok

    def analisa_exp(self):
        tok = self.olhar_token()
        if tok is None:
            raise ErroSintatico("expressao esperada, mas a entrada acabou")

        if tok.tipo == TokenTipo.NUMERO:
            self.proximo_token()
            return Const(int(tok.lexema))
        elif tok.tipo == TokenTipo.PAREN_ESQ:
            self.proximo_token()
            esq = self.analisa_exp()
            op = self.analisa_operador()
            dir = self.analisa_exp()
            self.verifica_token(TokenTipo.PAREN_DIR)
            return OpBin(op, esq, dir)
        else:
            raise ErroSintatico(f"token inesperado: '{tok.lexema}'")

    def analisa_operador(self):
        tok = self.proximo_token()
        if tok.tipo == TokenTipo.SOMA:
            return Op.SOMA
        elif tok.tipo == TokenTipo.SUB:
            return Op.SUB
        elif tok.tipo == TokenTipo.MULT:
            return Op.MULT
        elif tok.tipo == TokenTipo.DIV:
            return Op.DIV
        else:
            raise ErroSintatico(f"operador esperado, encontrou '{tok.lexema}'")


def parse(tokens):
    p = Parser(tokens)
    arvore = p.analisa_exp()
    # um programa EC1 e uma unica expressao, entao nao pode sobrar token
    sobra = p.olhar_token()
    if sobra is not None:
        raise ErroSintatico(f"token inesperado apos o fim do programa: '{sobra.lexema}'")
    return arvore
