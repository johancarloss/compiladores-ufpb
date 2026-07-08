# Atividade 08 — Expressões com Variáveis (EV)

Este projeto implementará a evolução do compilador desenvolvido nas atividades anteriores, adaptando-o para a linguagem **EV** (Expressões com Variáveis).

Nesta primeira etapa, a pasta `atv08/` foi criada a partir da base funcional da **Atividade 07 (EC2)**. As próximas etapas adicionam declarações de variáveis, análise semântica e geração de código com seção `.bss`.

O compilador realiza análise léxica, análise sintática, construção da Árvore de Sintaxe Abstrata (AST) e geração de código assembly **x86-64** para Linux.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 08

---

# Estrutura dos Arquivos em `atv08/`

```text
├── arvore.py       # Definição das classes da AST
├── lexer.py        # Analisador léxico
├── parser.py       # Parser da linguagem EV
├── semantico.py    # Análise semântica da linguagem EV
├── runtime.s       # Rotinas auxiliares em Assembly
├── compilador.py   # Gerador de código Assembly
├── testes.py       # Orquestrador dos testes automatizados
├── tests/
│   ├── ambiente.py       # Detecção de ferramentas e fallback Docker
│   ├── lexer_tests.py    # Testes do analisador léxico
│   ├── programa_tests.py # Testes da saída final do programa
│   └── out/              # Artefatos temporários gerados pelos testes
├── Makefile        # Comandos auxiliares
└── README.md       # Este arquivo
```

---

# Situação atual

Esta etapa apenas cria a base da Atividade 08. O código ainda preserva o comportamento da Atividade 07 para garantir que a cópia inicial continue funcional.

As próximas etapas do plano de implementação vão adicionar:

* tokens para identificadores, `=` e `;`;
* novos nós de AST para programa, declaração e variável;
* parser iniciado pelo não-terminal `<programa>`;
* análise semântica para detectar variáveis não declaradas;
* geração de código com variáveis na seção `.bss`;
* testes específicos da linguagem EV.

---

# Base herdada da Atividade 07

Na linguagem EC1, todas as operações precisavam estar obrigatoriamente entre parênteses.

Exemplo:

```text
(7 + (5 * 3))
```

Na EC2, base usada para iniciar esta atividade, os parênteses passam a ser opcionais sempre que a precedência natural dos operadores for suficiente.

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

# Geração de Código Atual

Até a conclusão das próximas etapas, o gerador de código ainda é o mesmo da Atividade 07.

Como a estrutura da AST permaneceu inalterada, o módulo `compilador.py` continua produzindo código Assembly x86-64 exatamente da mesma forma implementada na Atividade 06.

A árvore produzida pelo parser respeita as regras de precedência e associatividade da linguagem EC2, que será estendida para EV.

---

# Como Executar

Para compilar um arquivo EV para Assembly:

```bash
python3 compilador.py <arquivo.ev> <saida.s>
```

Exemplo:

```bash
python3 compilador.py programa.ev programa.s
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

# Objetivo da Atividade 08

O objetivo desta atividade é adaptar o compilador para reconhecer programas com declarações e uso de variáveis, preservando as regras de precedência e associatividade já implementadas na EC2.
