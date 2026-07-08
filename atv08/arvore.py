from enum import Enum


class Op(Enum):
    SOMA = "+"
    SUB = "-"
    MULT = "*"
    DIV = "/"


class Exp:
    pass


class Programa:
    def __init__(self, declaracoes, resultado):
        self.declaracoes = declaracoes
        self.resultado = resultado


class Decl:
    def __init__(self, nome, exp):
        self.nome = nome
        self.exp = exp


class Const(Exp):
    def __init__(self, valor):
        self.valor = valor

    def avaliar(self):
        return self.valor

    def __str__(self):
        return str(self.valor)


class OpBin(Exp):
    def __init__(self, op, esq, dir):
        self.op = op
        self.esq = esq
        self.dir = dir

    def avaliar(self):
        a = self.esq.avaliar()
        b = self.dir.avaliar()
        if self.op == Op.SOMA:
            return a + b
        elif self.op == Op.SUB:
            return a - b
        elif self.op == Op.MULT:
            return a * b
        else:
            return a // b

    def __str__(self):
        return f"({self.esq} {self.op.value} {self.dir})"


class Var(Exp):
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome


def desenhar_arvore(no):
    linhas = []
    _desenhar(no, "", "", linhas)
    return "\n".join(linhas)


def _desenhar(no, conector, prefixo, linhas):
    if isinstance(no, Const):
        rotulo = str(no.valor)
    elif isinstance(no, Var):
        rotulo = no.nome
    else:
        rotulo = no.op.value
    linhas.append(conector + rotulo)
    if isinstance(no, OpBin):
        # o operando esquerdo nao e o ultimo filho, o direito e
        _desenhar(no.esq, prefixo + "├── ", prefixo + "│   ", linhas)
        _desenhar(no.dir, prefixo + "└── ", prefixo + "    ", linhas)
