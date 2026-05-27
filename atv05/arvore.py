from enum import Enum


class Op(Enum):
    SOMA = "+"
    SUB = "-"
    MULT = "*"
    DIV = "/"


class Exp:
    pass


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
