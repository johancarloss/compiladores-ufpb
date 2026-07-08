import sys
from lexer import lex
from parser import parse, ErroSintatico
from arvore import Const, Decl, OpBin, Op, Programa, Var
from semantico import ErroSemantico, verificar


class GeradorCodigo:
    def __init__(self):
        self.linhas = []
        self.variaveis = []

    def gerar_secao_bss(self):
        if not self.variaveis:
            return ""

        linhas = [".section .bss"]
        for nome in self.variaveis:
            linhas.append(f"    .lcomm {nome}, 8")
        return "\n".join(linhas)

    def gerar(self, no):
        if isinstance(no, Programa):
            declaradas = set()
            for decl in no.declaracoes:
                if decl.nome not in declaradas:
                    self.variaveis.append(decl.nome)
                    declaradas.add(decl.nome)

            for decl in no.declaracoes:
                self.gerar(decl)

            self.linhas.append("    # Resultado final")
            self.gerar(no.resultado)
        elif isinstance(no, Decl):
            self.linhas.append(f"    # Declaração: {no.nome}")
            self.gerar(no.exp)
            self.linhas.append(f"    mov %rax, {no.nome}")
        elif isinstance(no, Var):
            self.linhas.append(f"    # Variável {no.nome}")
            self.linhas.append(f"    mov {no.nome}, %rax")
        elif isinstance(no, Const):
            self.linhas.append(f"    # Constante {no.valor}")
            self.linhas.append(f"    mov ${no.valor}, %rax")
        elif isinstance(no, OpBin):
            self.linhas.append(f"    # Operação: {no}")
            
            # Passo 1: Incluir o código gerado para o operando direito
            self.linhas.append("    # Passo 1: operando direito")
            self.gerar(no.dir)
            
            # Passo 2: Usar a instrução push %rax para salvar o valor
            self.linhas.append("    # Passo 2: push %rax")
            self.linhas.append("    push %rax")
            
            # Passo 3: Incluir o código gerado para o operando esquerdo
            self.linhas.append("    # Passo 3: operando esquerdo")
            self.gerar(no.esq)
            
            # Passo 4: Desempilhar o resultado no topo da pilha colocando-o no registrador %rbx usando pop %rbx
            self.linhas.append("    # Passo 4: pop %rbx")
            self.linhas.append("    pop %rbx")
            
            # Passo 5: Executar a operação aritmética adequada
            self.linhas.append(f"    # Passo 5: aplicar operador {no.op.value}")
            if no.op == Op.SOMA:
                self.linhas.append("    add %rbx, %rax")
            elif no.op == Op.SUB:
                self.linhas.append("    sub %rbx, %rax")
            elif no.op == Op.MULT:
                self.linhas.append("    imul %rbx, %rax")
            elif no.op == Op.DIV:
                self.linhas.append("    cqto")
                self.linhas.append("    idiv %rbx")
            else:
                raise ValueError(f"Operador desconhecido: {no.op}")
        else:
            raise TypeError(f"Tipo de nó inválido na AST: {type(no)}")


def compilar(fonte: str) -> str:
    """Recebe uma string com codigo EV, realiza analise lexica, sintatica,

    e gera o código assembly x86-64 correspondente.
    """
    # 1. Análise Léxica
    lx = lex(fonte)
    if lx.houve_erro:
        raise ErroSintatico(f"Erro léxico na posição {lx.erro_pos}: caractere inválido '{lx.erro_char}'")
    
    # 2. Análise Sintática
    arvore = parse(lx.tokens)
    
    # 3. Analise Semantica
    verificar(arvore)

    # 4. Geração de Código
    gerador = GeradorCodigo()
    gerador.gerar(arvore)
    
    secao_bss = gerador.gerar_secao_bss()
    codigo_expressao = "\n".join(gerador.linhas)
    
    # Modelo de arquivo assembly final
    secoes = []
    if secao_bss:
        secoes.append(secao_bss)

    secoes.append(f""".section .text
.globl _start
_start:
    # --- Início do Código Gerado ---
{codigo_expressao}
    # --- Fim do Código Gerado ---

    call imprime_num
    call sair
    .include "runtime.s"
""")
    assembly = "\n".join(secoes)
    return assembly


def main():
    if len(sys.argv) != 3:
        print(f"Uso: python3 {sys.argv[0]} <arquivo.ev> <arquivo_saida.s>", file=sys.stderr)
        return 1

    caminho_entrada = sys.argv[1]
    caminho_saida = sys.argv[2]

    try:
        with open(caminho_entrada, "r") as f:
            fonte = f.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir '{caminho_entrada}'", file=sys.stderr)
        return 1

    try:
        assembly_gerado = compilar(fonte)
    except (ErroSintatico, ErroSemantico, ValueError, TypeError) as e:
        print(f"Erro ao compilar: {e}", file=sys.stderr)
        return 1

    try:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(assembly_gerado)
    except OSError:
        print(f"Erro: nao foi possivel escrever em '{caminho_saida}'", file=sys.stderr)
        return 1

    print(f"Compilação concluída com sucesso! Código salvo em: {caminho_saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
