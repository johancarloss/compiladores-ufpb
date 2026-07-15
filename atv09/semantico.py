from arvore import Const, OpBin, Var, Atrib, If, While


class ErroSemantico(Exception):
    pass


class VariavelNaoDeclarada(ErroSemantico):
    def __init__(self, nome):
        self.nome = nome
        super().__init__(f"variavel nao declarada: {nome}")


def verificar(programa):
    declaradas = set()

    # so as declaracoes adicionam variaveis ao conjunto de declaradas
    for decl in programa.declaracoes:
        verificar_exp(decl.exp, declaradas)
        declaradas.add(decl.nome)

    # os comandos do corpo apenas usam variaveis, nao declaram novas
    verificar_comandos(programa.comandos, declaradas)

    verificar_exp(programa.resultado, declaradas)
    return programa


def verificar_comandos(comandos, declaradas):
    for cmd in comandos:
        verificar_cmd(cmd, declaradas)


def verificar_cmd(cmd, declaradas):
    if isinstance(cmd, Atrib):
        # a variavel que recebe o valor tambem precisa ja estar declarada
        if cmd.nome not in declaradas:
            raise VariavelNaoDeclarada(cmd.nome)
        verificar_exp(cmd.exp, declaradas)
    elif isinstance(cmd, If):
        verificar_exp(cmd.cond, declaradas)
        verificar_comandos(cmd.corpo_then, declaradas)
        verificar_comandos(cmd.corpo_else, declaradas)
    elif isinstance(cmd, While):
        verificar_exp(cmd.cond, declaradas)
        verificar_comandos(cmd.corpo, declaradas)


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
