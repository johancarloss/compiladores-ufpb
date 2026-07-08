from arvore import Const, Decl, Op, OpBin, Programa, Var
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

    def analisa_programa(self):
        declaracoes = []
        tok = self.olhar_token()

        while tok is not None and tok.tipo == TokenTipo.IDENT:
            declaracoes.append(self.analisa_decl())
            tok = self.olhar_token()

        resultado = self.analisa_result()
        return Programa(declaracoes, resultado)

    def analisa_decl(self):
        nome = self.verifica_token(TokenTipo.IDENT).lexema
        self.verifica_token(TokenTipo.IGUAL)
        exp = self.analisa_exp_a()
        self.verifica_token(TokenTipo.PONTO_VIRGULA)
        return Decl(nome, exp)

    def analisa_result(self):
        self.verifica_token(TokenTipo.IGUAL)
        return self.analisa_exp_a()

    def analisa_exp_a(self):
        """Analisa expressões aditivas (soma e subtração)."""
        esq = self.analisa_exp_m()
        tok = self.olhar_token()
        
        while tok is not None and tok.tipo in (TokenTipo.SOMA, TokenTipo.SUB):
            self.proximo_token()  # Consome o operador
            dir = self.analisa_exp_m()
            
            if tok.tipo == TokenTipo.SOMA:
                esq = OpBin(Op.SOMA, esq, dir)
            else:
                esq = OpBin(Op.SUB, esq, dir)
                
            tok = self.olhar_token()
            
        return esq

    def analisa_exp_m(self):
        """Analisa expressões multiplicativas (multiplicação e divisão)."""
        esq = self.analisa_prim()
        tok = self.olhar_token()
        
        while tok is not None and tok.tipo in (TokenTipo.MULT, TokenTipo.DIV):
            self.proximo_token()  # Consome o operador
            dir = self.analisa_prim()
            
            if tok.tipo == TokenTipo.MULT:
                esq = OpBin(Op.MULT, esq, dir)
            else:
                esq = OpBin(Op.DIV, esq, dir)
                
            tok = self.olhar_token()
            
        return esq

    def analisa_prim(self):
        """Analisa expressões primárias (constantes inteiras e parênteses)."""
        tok = self.proximo_token()
        
        if tok.tipo == TokenTipo.NUMERO:
            return Const(int(tok.lexema))
        elif tok.tipo == TokenTipo.IDENT:
            return Var(tok.lexema)
        elif tok.tipo == TokenTipo.PAREN_ESQ:
            # Dentro do parêntese, a precedência reinicia para a mais baixa (exp_a)
            exp = self.analisa_exp_a()
            self.verifica_token(TokenTipo.PAREN_DIR)
            return exp
        else:
            raise ErroSintatico(f"token inesperado: '{tok.lexema}'")


def parse(tokens):
    """Inicializa o parser e exige que toda a entrada seja consumida."""
    p = Parser(tokens)
    if not p.tokens:
        raise ErroSintatico("entrada vazia")

    arvore = p.analisa_programa()
    
    sobra = p.olhar_token()
    if sobra is not None:
        raise ErroSintatico(f"token inesperado apos o fim do programa: '{sobra.lexema}'")
        
    return arvore
