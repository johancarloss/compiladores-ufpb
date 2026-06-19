# Atividade 06 — Expressões Constantes 1 (Compilador)

> **Metadados do PDF original**
>
> * **Arquivo:** `CC - Atividade 06.pdf`
> * **Autor:** Andrei Formiga (professor)
> * **Data:** 30 de maio de 2026
> * **Páginas:** 13
> * **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Transcrição resumida + comentários da especificação oficial. Citações textuais são destacadas; comentários e decisões de implementação aparecem como **Observação**.

---

# Sumário

1. Introdução
2. A linguagem EC1
3. Geração de código
4. Uso da pilha para armazenamento
5. Inclusão do código no modelo completo
6. Artefato para entrega
7. Nota sobre otimização
8. Plano de implementação adotado

---

# 1. Introdução

> *"Nesta atividade vamos reunir o que vimos nas atividades anteriores e adicionar um gerador de código, criando assim um compilador completo para a linguagem EC1."*

Até a Atividade 05, o projeto já realizava:

* análise léxica;
* análise sintática;
* construção da AST;
* interpretação da árvore.

O objetivo da Atividade 06 é adicionar uma etapa de **geração de código assembly**, transformando o projeto em um compilador completo.

**Objetivo:** gerar código assembly x86-64 a partir da AST produzida pelo parser.

---

# 2. A linguagem EC1

A linguagem continua exatamente a mesma utilizada nas atividades anteriores.

```bnf
<programa> ::= <expressao>

<expressao> ::= <literal-inteiro>
              | '(' <expressao> <operador> <expressao> ')'

<operador> ::= '+'
             | '-'
             | '*'
             | '/'

<literal-inteiro> ::= <digito>+

<digito> ::= '0' | '1' | ... | '9'
```

Exemplos válidos:

```text
333

(6 * 7)

(3 + (4 + (11 + 7)))

(33 + (912 * 11))

((427 / 7) + (11 * (231 + 5)))
```

**Observação:** como todas as operações são obrigatoriamente parentizadas, não existe preocupação com precedência de operadores.

---

# 3. Geração de código

> *"A geração de código é a etapa que produz o programa de saída na linguagem destino."*

A geração de código é realizada através de uma travessia recursiva da AST.

A convenção adotada é:

* todo resultado deve ficar em `%rax`;
* ao final do programa, o valor em `%rax` será impresso.

## Tradução de constantes

Para um nó do tipo `Const`:

```ec1
42
```

gera:

```assembly
mov $42, %rax
```

Na implementação:

```python
if isinstance(no, Const):
    mov $valor, %rax
```

---

## Tradução de operações binárias

Para nós do tipo `OpBin`, o código gerado deve combinar:

* código do operando esquerdo;
* código do operando direito;
* instrução correspondente ao operador.

A geração é recursiva, da mesma forma que:

* impressão da árvore;
* interpretação;
* análise sintática.

---

# 4. Usando a pilha para armazenamento

O PDF mostra que utilizar apenas registradores não escala para expressões arbitrariamente grandes.

A solução adotada é utilizar a pilha do sistema.

Instruções utilizadas:

```assembly
push %rax
pop %rbx
```

A pilha permite armazenar resultados intermediários sem depender de uma quantidade fixa de registradores.

---

## 4.1 Esquema de tradução usando pilha

A implementação do projeto segue o esquema sugerido no PDF.

### Passo 1

Gerar código do operando direito.

```assembly
...
resultado -> %rax
```

### Passo 2

Empilhar o resultado.

```assembly
push %rax
```

### Passo 3

Gerar código do operando esquerdo.

```assembly
...
resultado -> %rax
```

### Passo 4

Recuperar o operando direito.

```assembly
pop %rbx
```

### Passo 5

Executar a operação.

---

### Soma

```assembly
add %rbx, %rax
```

Resultado:

```text
rax = esquerdo + direito
```

---

### Subtração

```assembly
sub %rbx, %rax
```

Resultado:

```text
rax = esquerdo - direito
```

---

### Multiplicação

```assembly
imul %rbx, %rax
```

Resultado:

```text
rax = esquerdo * direito
```

---

### Divisão

```assembly
cqto
idiv %rbx
```

Resultado:

```text
rax = esquerdo / direito
```

---

## Correspondência com o código implementado

No arquivo `compilador.py`:

```python
self.gerar(no.dir)

push %rax

self.gerar(no.esq)

pop %rbx
```

Em seguida:

```python
if no.op == Op.SOMA:
    add %rbx, %rax

elif no.op == Op.SUB:
    sub %rbx, %rax

elif no.op == Op.MULT:
    imul %rbx, %rax

elif no.op == Op.DIV:
    cqto
    idiv %rbx
```

**Observação:** a implementação gera primeiro o operando direito exatamente para preservar a ordem correta em subtrações e divisões.

---

# 5. Inclusão do código no modelo completo

O código gerado para a expressão não constitui um programa completo.

O assembly final deve seguir o modelo:

```assembly
.section .text

.globl _start

_start:

    ## código gerado

    call imprime_num
    call sair

    .include "runtime.s"
```

Na implementação, o método `compilar()` encapsula automaticamente o código gerado dentro desse template.

---

# 6. Artefato para entrega

> *"O grupo deve entregar o código para o compilador EC1 completo, gerando assembly correto para todos os possíveis programas corretos na linguagem EC1."*

O compilador deve:

* realizar análise léxica;
* realizar análise sintática;
* construir AST;
* gerar assembly;
* produzir arquivo pronto para montagem;
* incluir testes;
* incluir documentação.

---

# 7. Uma nota sobre otimização

> *"O esquema usando pilha é simples de implementar, mas não gera o melhor código possível."*

Problemas:

* acesso à RAM é mais lento que registradores;
* há instruções extras (`push` e `pop`);
* expressões simples poderiam usar apenas registradores.

O PDF menciona uma otimização importante:

## Propagação de constantes

Como toda expressão EC1 contém apenas constantes:

```ec1
(7 * (78 / (5 + 8)))
```

poderia ser calculada durante a compilação.

Resultado:

```assembly
mov $42, %rax
```

Essa otimização não foi implementada nesta atividade.

---

# 8. Plano de implementação adotado

Estrutura do projeto:

```text
lexer.py
parser.py
arvore.py
compilador.py
runtime.s
testes.py
Makefile
tests/
```

Fluxo do compilador:

```text
arquivo.ec1
      |
      v
    lexer
      |
      v
    tokens
      |
      v
    parser
      |
      v
     AST
      |
      v
 gerador de código
      |
      v
 assembly x86-64
      |
      v
 arquivo .s
```

---

**Última atualização:** 2026-06-19

