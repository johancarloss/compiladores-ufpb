# Atividade 05 — Expressões Constantes 1 (Análise Sintática)

> **Metadados do PDF original**
> - **Arquivo:** `CC - Atividade 05.pdf`
> - **Autor:** Andrei Formiga (professor)
> - **Data:** 20 de maio de 2026
> - **Páginas:** 14
> - **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Transcrição fiel + comentários do PDF. Citação textual em blockquote; comentário/inferência marcado como **Observação:**.

---

## Sumário

1. [Introdução](#1-introdução)
2. [A linguagem EC1](#2-a-linguagem-ec1)
3. [Análise sintática descendente recursiva](#3-análise-sintática-descendente-recursiva)
4. [Árvore de sintaxe abstrata](#4-árvore-de-sintaxe-abstrata)
5. [Representação da árvore](#5-representação-da-árvore)
6. [Análise das expressões em EC1](#6-análise-das-expressões-em-ec1)
7. [Interface entre léxico e sintático](#7-interface-entre-léxico-e-sintático)
8. [Um interpretador](#8-um-interpretador)
9. [Impressão da árvore](#9-impressão-da-árvore)
10. [Artefato para entrega](#10-artefato-para-entrega)

---

## 1. Introdução

> *"Continuando o processo de análise da linguagem EC1, nesta atividade vamos fazer a análise sintática. A análise sintática determina a estrutura sintática (gramatical) do programa de entrada, usando a sequência de tokens resultante da análise léxica. A saída da análise sintática pode ter várias formas, mas nos projetos da disciplina, o analisador sintático deve produzir uma árvore de sintaxe abstrata."*

**Objetivo:** análise sintática da EC1, produzindo uma AST.

---

## 2. A linguagem EC1

Mesma da atividade 04.

```bnf
<programa>  ::= <expressao>
<expressao> ::= <literal> | '(' <expressao> <operador> <expressao> ')'
<operador>  ::= '+' | '-' | '*' | '/'
<literal>   ::= <digito>+
<digito>    ::= '0' | '1' | ... | '9'
```

> *"Esta gramática mistura regras da micro-sintaxe léxica (literal e digito) com regras para a sintaxe em si (programa, expressao e operador)."*

O não-terminal `programa` contém apenas uma `expressao`, então só precisamos das regras de `expressao` e `operador`.

---

## 3. Análise sintática descendente recursiva

> *"Na análise descendente recursiva, criamos uma função para cada não-terminal que queremos analisar. No caso da gramática para a linguagem EC1, teremos duas funções, para analisar expressao e operador. Quando um não-terminal possui mais de uma regra, deve ser possível determinar qual regra deverá ser seguida olhando apenas para o próximo token na entrada."*

A `expressao` tem duas regras:
- Se o próximo token for **literal inteiro** → primeira regra (literal).
- Se for **parêntese abrindo** → segunda regra (operação binária).
- Senão → erro sintático.

Pseudo-código inicial (incompleto):

```
analisaExp():
    tok = proximo_token()
    if tok.tipo == LITERAL_INTEIRO:
        # analisa constante inteira
    else if tok.tipo == ABRE_PARENTESE:
        # analisa operação binária
    else:
        # sinaliza erro sintático
```

> *"O papel mais importante da análise sintática é determinar a estrutura do código de entrada. Nesse caso, nosso compilador vai retornar uma árvore sintática que será utilizada pelas etapas seguintes."*

---

## 4. Árvore de sintaxe abstrata

> *"Uma árvore sintática é uma árvore composta por nós que descrevem as estruturas do programa de entrada; esses nós podem possuir filhos na árvore que representam sub-componentes da estrutura representada pelo nó pai."*

**Exemplos:**

Programa `42` (só constante):
```
# arvore
42
```

Programa `(7 * 6)`:
```
# arvore
   *
  / \
 7   6
```

Programa `(33 + (912 * 11))`:
```
# arvore
   +
  / \
 33  *
    / \
  912  11
```

> *"Note que a estrutura da árvore captura a estrutura da expressão: a expressão é uma soma tendo como operando esquerdo a constante 33, e como operando direito uma multiplicação (entre 912 e 11). Para realizar a soma, é preciso saber o valor de ambos operandos, o que significa que a multiplicação deve ser efetuada antes da soma."*

**Observação:** a árvore codifica a ordem de avaliação. Filhos são avaliados antes do pai.

---

## 5. Representação da árvore

> *"Para a linguagem EC1, podemos definir uma classe-base `Exp` que representa expressões. Desta classe derivamos duas sub-classes: `Const` para uma constante inteira, e `OpBin` para uma operação binária."*

Pseudo-código (estilo Java):

```java
abstract class Exp { }

class Const extends Exp {
    int valor;
}

class OpBin extends Exp {
    op  operador;
    Exp esq;
    Exp dir;
}
```

> *"Neste código, não definimos o tipo `op` para o operador, mas esse campo apenas precisa distinguir entre as quatro operações possíveis: soma, subtração, multiplicação e divisão. Podemos usar uma enumeração ou um conjunto de constantes inteiras para isso."*

---

## 6. Análise das expressões em EC1

Pseudo-código completo da análise:

```
analisaExp():
    tok = proximo_token()
    if tok.tipo == LITERAL_INTEIRO:
        return new Const(inteiro(tok.lexema))
    else if tok.tipo == ABRE_PARENTESE:
        esq = analisaExp()
        operador = analisaOperador()
        dir = analisaExp()
        verificaProxToken(FECHA_PARENTESE)
        return new OpBin(operador, esq, dir)
    else:
        # sinaliza erro sintatico
```

> *"A função `verificaProxToken` verifica se o próximo token tem o tipo necessário (FECHA_PARENTESE, no caso) e sinaliza um erro caso não seja deste tipo."*

> *"A função `analisaOperador` é bem simples: verifica se o próximo token é um dos quatro operadores e cria um valor para representar o operador adequado; se não for um dos quatro operadores reconhecidos, é um erro sintático."*

> *"As funções `analisaExp` e `analisaOperador` fazem toda a análise sintática para a linguagem EC1."*

---

## 7. Interface entre léxico e sintático

> *"As funções de análise sintática acessam os tokens criados pela análise léxica em sequência, usando a função `proximo_token`. Essa função retorna o próximo token na entrada e avança a leitura da entrada para o token seguinte."*

> *"O analisador léxico pode ser organizado para retornar um token por vez (`proximo_token`) ou pode varrer a entrada inteira e retornar uma coleção com todos os tokens de uma vez. Nesse segundo caso, é fácil criar a função `proximo_token` a partir da coleção completa: toda vez que `proximo_token` é chamada, o token atual da coleção é retornado, e o índice do token atual é incrementado."*

**Observação:** nosso `lexer.py` da atv04 retorna a **lista completa** de tokens. Então vamos criar um `proximo_token` simples sobre essa lista (com um índice que avança a cada chamada). Também precisamos verificar fim da entrada.

---

## 8. Um interpretador

> *"A árvore sintática possui todas as informações necessárias para executar o programa EC1. Executar o programa de entrada sem traduzi-lo para outra linguagem é um processo chamado de interpretação. Uma forma simples de interpretador é o interpretador de varredura de árvore (tree-walking interpreter)."*

Processo recursivo:
- Se o nó é uma **constante**, o valor do nó é o valor da constante.
- Se o nó é uma **operação binária**, obtenha o valor do operando esquerdo e do direito; o valor do nó é o resultado de aplicar o operador.

> *"Se a árvore é representada com objetos de uma hierarquia de classes, uma forma de implementar o interpretador é definir um método na classe base `Exp` e implementar o método nas sub-classes de maneira adequada."*

**Observação:** vamos usar essa abordagem — método `avaliar()` em `Const` e `OpBin`.

---

## 9. Impressão da árvore

> *"Um outro processo de varredura da árvore é a impressão, que é útil para testes."*

Processo de impressão (similar ao programa de entrada):
- Se o nó é uma **constante**, imprimir a constante.
- Se o nó é uma **operação binária**, imprimir em sequência: parêntese `(`, operando esquerdo, operador, operando direito, parêntese `)`.

> *"Outra possibilidade é imprimir a árvore em um formato mais visual, usando caracteres ASCII ou graphviz."*

**Observação:** vamos implementar a impressão "linear" (reconstrói a expressão), via `__str__` nas classes.

---

## 10. Artefato para entrega

> *"O grupo deve entregar um programa que faz análise léxica e sintática do programa de entrada (usando o analisador léxico da atividade anterior), produz a árvore sintática do programa de entrada e obtém o valor do programa através de interpretação por varredura da árvore."*

> *"O projeto deve incluir um conjunto de testes que verifica tanto a produção correta da árvore sintática para um conjunto de programas, como o valor do programa obtido pela interpretação. Os testes também devem incluir exemplos de programas com erros de sintaxe, e o compilador deve ser capaz de detectar e reportar esses erros."*

> *"O projeto também deve incluir documentação sucinta e clara que explica como usar o analisador e executar os testes."*

**Checklist de entrega:**

- [ ] Programa que faz análise léxica + sintática (reusa lexer da atv04)
- [ ] Produz a árvore sintática (AST)
- [ ] Interpreta a árvore e obtém o valor (tree-walking)
- [ ] Testes: árvore correta + valor da interpretação + erros de sintaxe detectados
- [ ] Documentação sucinta (como usar + como rodar testes)

---

## Apêndice — Plano de implementação (Python)

Arquivos:

```
lexer.py          # reusado da atv04 (lista de tokens)
arvore.py         # AST: Const e OpBin, com métodos avaliar() e __str__()
parser.py         # analisa_exp(), analisa_operador(), proximo_token()
main.py           # CLI: lê arquivo -> lexer -> parser -> imprime árvore + valor
tests/            # casos: árvore correta, valor, erros de sintaxe
run_tests.sh      # roda os testes
```

Fluxo:

```
arquivo.ec1 -> lex() -> [tokens] -> parse() -> AST -> avaliar() -> valor
                                              -> str(AST) -> árvore impressa
```

**Última atualização:** 2026-05-27 (leitura inicial do PDF).
