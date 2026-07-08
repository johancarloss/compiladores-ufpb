from arvore import Const, OpBin, Var


class ErroSemantico(Exception):
    pass


class VariavelNaoDeclarada(ErroSemantico):
    def __init__(self, nome):
        self.nome = nome
        super().__init__(f"variavel nao declarada: {nome}")


def verificar(programa):
    declaradas = set()

    for decl in programa.declaracoes:
        verificar_exp(decl.exp, declaradas)
        declaradas.add(decl.nome)

    verificar_exp(programa.resultado, declaradas)
    return programa


def verificar_exp(exp, declaradas):
    if isinstance(exp, Const):
        return
    if isinstance(exp, Var):
        if exp.nome not in declaradas:
            raise VariavelNaoDeclarada(exp.nome)
        return
    if isinstance(exp, OpBin):
        verificar_exp(exp.esq, declaradas)
        verificar_exp(exp.dir, declaradas)
        return
