# Atividade 07 — Expressões Constantes 2 (EC2)

Este projeto implementa a evolução do compilador desenvolvido nas atividades anteriores, adaptando-o para a linguagem **EC2** (Expressões Constantes 2). A principal mudança consiste na remoção da obrigatoriedade de parênteses em todas as operações, passando a respeitar automaticamente as regras de **precedência** e **associatividade** dos operadores aritméticos.

O compilador realiza análise léxica, análise sintática, construção da Árvore de Sintaxe Abstrata (AST) e geração de código assembly **x86-64** para Linux.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 07

---

# Estrutura dos Arquivos em `atv07/`

```text
├── arvore.py       # Definição das classes da AST
├── lexer.py        # Analisador léxico
├── parser.py       # Parser da linguagem EC2
├── runtime.s       # Rotinas auxiliares em Assembly
├── compilador.py   # Gerador de código Assembly
├── testes.py       # Testes automatizados
├── Makefile        # Comandos auxiliares
└── README.md       # Este arquivo
```

---

# O que mudou em relação à Atividade 06?

Na linguagem EC1, todas as operações precisavam estar obrigatoriamente entre parênteses.

Exemplo:

```text
(7 + (5 * 3))
```

Na EC2, os parênteses passam a ser opcionais sempre que a precedência natural dos operadores for suficiente.

Agora são aceitas expressões como:

```text
7 + 5 * 3

10 - 8 - 2

100 - 2 * 10 + 20

3 + 4 * 2 / (1 - 5)
```

---

# Precedência e Associatividade

O parser foi reorganizado para implementar a seguinte gramática:

```bnf
exp_a ::= exp_m (('+' | '-') exp_m)*

exp_m ::= prim (('*' | '/') prim)*

prim ::= numero
       | '(' exp_a ')'
```

Com essa divisão:

* Multiplicação e divisão possuem precedência sobre soma e subtração.
* Operadores de mesma precedência são avaliados da esquerda para a direita.
* Parênteses continuam podendo alterar a ordem de avaliação.

---

# Implementação do Parser

O analisador sintático foi dividido em três funções principais:

* `analisa_exp_a()`

  * Reconhece operações de soma e subtração.

* `analisa_exp_m()`

  * Reconhece multiplicação e divisão.

* `analisa_prim()`

  * Reconhece constantes inteiras e expressões entre parênteses.

Também foi utilizada a função `olhar_token()` para consultar o próximo token sem consumi-lo, permitindo reconhecer cadeias de operadores da mesma precedência.

A construção da AST continua utilizando apenas os nós `Const` e `OpBin`, mantendo compatibilidade com o gerador de código desenvolvido na atividade anterior.

---

# Geração de Código

Nenhuma alteração foi necessária no gerador de código.

Como a estrutura da AST permaneceu inalterada, o módulo `compilador.py` continua produzindo código Assembly x86-64 exatamente da mesma forma implementada na Atividade 06.

A única diferença é que a árvore produzida pelo parser agora respeita automaticamente as regras de precedência e associatividade da linguagem EC2.

---

# Como Executar

Para compilar um arquivo EC2 para Assembly:

```bash
python3 compilador.py <arquivo.ec2> <saida.s>
```

Exemplo:

```bash
python3 compilador.py expressao.ec2 expressao.s
```

---

# Como Executar os Testes

Os testes podem ser executados utilizando:

```bash
make test
```

ou

```bash
python3 testes.py
```

Além dos testes das atividades anteriores, foram adicionados casos específicos para validar a nova gramática:

```text
42
7+5*3
10-8-2
100/2/2
10*5+20/4
100-2*10+20
3+4*2/(1-5)
```

Esses testes verificam:

* precedência de operadores;
* associatividade à esquerda;
* utilização de parênteses;
* compatibilidade com expressões da EC1.

Em ambientes Linux x86-64, os testes compilam, montam, linkam e executam os binários gerados.

Em outros sistemas, como Windows, é realizada a validação da sintaxe do Assembly gerado, conforme disponibilidade das ferramentas (`as` e `ld`).

---

# Objetivo da Atividade

O objetivo desta atividade foi adaptar o compilador para reconhecer expressões aritméticas escritas de forma natural, respeitando automaticamente as regras de precedência e associatividade dos operadores, sem modificar a estrutura da AST nem o gerador de código desenvolvido anteriormente.


