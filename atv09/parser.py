from arvore import Const, Decl, Op, OpBin, Programa, Var, Atrib, If, While
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
        # declaracoes vem antes do corpo; cada uma comeca com um identificador.
        # o corpo comeca no '{', entao as declaracoes terminam quando aparece '{'.
        declaracoes = []
        tok = self.olhar_token()
        while tok is not None and tok.tipo == TokenTipo.IDENT:
            declaracoes.append(self.analisa_decl())
            tok = self.olhar_token()

        comandos, resultado = self.analisa_corpo()
        return Programa(declaracoes, comandos, resultado)

    def analisa_decl(self):
        nome = self.verifica_token(TokenTipo.IDENT).lexema
        self.verifica_token(TokenTipo.IGUAL)
        exp = self.analisa_exp()
        self.verifica_token(TokenTipo.PONTO_VIRGULA)
        return Decl(nome, exp)

    def analisa_corpo(self):
        # corpo: '{' <cmd>* 'return' <exp> ';' '}'
        self.verifica_token(TokenTipo.CHAVE_ESQ)
        comandos = []
        tok = self.olhar_token()
        while tok is not None and tok.tipo != TokenTipo.RETURN:
            comandos.append(self.analisa_cmd())
            tok = self.olhar_token()
        self.verifica_token(TokenTipo.RETURN)
        resultado = self.analisa_exp()
        self.verifica_token(TokenTipo.PONTO_VIRGULA)
        self.verifica_token(TokenTipo.CHAVE_DIR)
        return comandos, resultado

    def analisa_cmd(self):
        # um comando comeca com 'if', 'while' ou um identificador (atribuicao)
        tok = self.olhar_token()
        if tok is None:
            raise ErroSintatico("comando esperado, mas a entrada acabou")
        if tok.tipo == TokenTipo.IF:
            return self.analisa_if()
        elif tok.tipo == TokenTipo.WHILE:
            return self.analisa_while()
        elif tok.tipo == TokenTipo.IDENT:
            return self.analisa_atrib()
        else:
            raise ErroSintatico(f"comando invalido comecando em '{tok.lexema}'")

    def analisa_if(self):
        self.verifica_token(TokenTipo.IF)
        cond = self.analisa_exp()
        corpo_then = self.analisa_bloco()
        self.verifica_token(TokenTipo.ELSE)
        corpo_else = self.analisa_bloco()
        return If(cond, corpo_then, corpo_else)

    def analisa_while(self):
        self.verifica_token(TokenTipo.WHILE)
        cond = self.analisa_exp()
        corpo = self.analisa_bloco()
        return While(cond, corpo)

    def analisa_atrib(self):
        nome = self.verifica_token(TokenTipo.IDENT).lexema
        self.verifica_token(TokenTipo.IGUAL)
        exp = self.analisa_exp()
        self.verifica_token(TokenTipo.PONTO_VIRGULA)
        return Atrib(nome, exp)

    def analisa_bloco(self):
        # bloco de comandos: '{' <cmd>* '}'
        self.verifica_token(TokenTipo.CHAVE_ESQ)
        comandos = []
        tok = self.olhar_token()
        while tok is not None and tok.tipo != TokenTipo.CHAVE_DIR:
            comandos.append(self.analisa_cmd())
            tok = self.olhar_token()
        self.verifica_token(TokenTipo.CHAVE_DIR)
        return comandos

    def analisa_exp(self):
        """Analisa comparacoes (<, >, ==). Precedencia mais baixa de todas."""
        esq = self.analisa_exp_a()
        tok = self.olhar_token()
        while tok is not None and tok.tipo in (
            TokenTipo.MENOR, TokenTipo.MAIOR, TokenTipo.IGUALDADE
        ):
            self.proximo_token()
            dir = self.analisa_exp_a()
            if tok.tipo == TokenTipo.MENOR:
                esq = OpBin(Op.MENOR, esq, dir)
            elif tok.tipo == TokenTipo.MAIOR:
                esq = OpBin(Op.MAIOR, esq, dir)
            else:
                esq = OpBin(Op.IGUALDADE, esq, dir)
            tok = self.olhar_token()
        return esq

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
            # dentro do parentese a precedencia reinicia para o topo (exp)
            exp = self.analisa_exp()
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
