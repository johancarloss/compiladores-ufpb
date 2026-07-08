# Atividade 08 — Expressões com Variáveis (EV)

Este projeto implementa a evolução do compilador desenvolvido nas atividades anteriores, adaptando-o para a linguagem **EV** (Expressões com Variáveis). A principal mudança em relação à **Atividade 07 (EC2)** é a inclusão de declarações e uso de variáveis em expressões aritméticas.

O compilador realiza análise léxica, análise sintática, análise semântica, construção da Árvore de Sintaxe Abstrata (AST) e geração de código assembly **x86-64** para Linux.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 08

---

# Estrutura dos Arquivos em `atv08/`

```text
├── arvore.py        # Definição das classes da AST
├── lexer.py         # Analisador léxico
├── parser.py        # Parser da linguagem EV
├── semantico.py     # Análise semântica da linguagem EV
├── runtime.s        # Rotinas auxiliares em Assembly
├── compilador.py    # Gerador de código Assembly
├── testes.py        # Orquestrador dos testes automatizados
├── tests/
│   ├── __init__.py
│   ├── ambiente.py        # Detecção de ferramentas e execução via Docker
│   ├── lexer_tests.py     # Testes do analisador léxico
│   ├── parser_tests.py    # Testes do analisador sintático
│   ├── semantico_tests.py # Testes da análise semântica
│   └── geracao_tests.py   # Testes da geração de Assembly
├── Dockerfile       # Ambiente Linux x86-64 para testes end-to-end
├── Makefile         # Comandos auxiliares
└── README.md        # Este arquivo
```

---

# O que mudou em relação à Atividade 07?

Na linguagem EC2, o programa era apenas uma expressão aritmética:

```text
7 + 5 * 3
```

Na linguagem EV, o programa passa a ter zero ou mais declarações de variáveis, seguidas por uma expressão final indicada por `=`.

Exemplo:

```ev
x = (7 + 4) * 12;
y = x * 3 + 11;
= (x * y) + (x * 11) + (y * 13)
```

Também continuam válidos programas sem declarações:

```ev
= 42
```

---

# Gramática

O parser implementa a seguinte gramática:

```bnf
programa  ::= decl* resultado

decl      ::= ident '=' exp_a ';'

resultado ::= '=' exp_a

exp_a     ::= exp_m (('+' | '-') exp_m)*

exp_m     ::= prim (('*' | '/') prim)*

prim      ::= numero
            | ident
            | '(' exp_a ')'
```

Com essa divisão:

* Multiplicação e divisão possuem precedência sobre soma e subtração.
* Operadores de mesma precedência são avaliados da esquerda para a direita.
* Parênteses continuam podendo alterar a ordem de avaliação.
* Variáveis podem ser usadas em expressões depois de declaradas.

---

# Análise Léxica

O lexer reconhece os tokens já existentes da EC2:

```text
Numero, ParenEsq, ParenDir, Soma, Sub, Mult, Div
```

E adiciona os tokens necessários para EV:

```text
Ident, Igual, PontoVirgula
```

Identificadores seguem a regra:

```bnf
ident ::= letra (letra | digito)*
```

Entradas como `237abc` e `9valor` são tratadas como erro léxico, porque começam como número e depois misturam letras.

---

# AST

A AST foi estendida com novos nós:

```python
Programa(declaracoes, resultado)
Decl(nome, exp)
Var(nome)
```

Os nós já existentes continuam sendo usados para expressões:

```python
Const(valor)
OpBin(op, esq, dir)
```

Assim, um programa como:

```ev
x = 10;
y = x + 2;
= y * 3
```

É representado como um `Programa` com duas declarações e uma expressão final.

---

# Análise Semântica

A análise semântica verifica se toda variável usada já foi declarada anteriormente.

Este programa é válido:

```ev
x = 10;
y = x + 2;
= y * 3
```

Este programa é inválido:

```ev
x = y + 1;
y = 2;
= x
```

Nesse caso, o compilador sinaliza erro semântico porque `y` é usado antes da declaração.

---

# Geração de Código

O gerador emite assembly x86-64 no formato GAS.

Para variáveis, é gerada uma seção `.bss` com uma reserva de 8 bytes por identificador declarado:

```asm
.section .bss
    .lcomm x, 8
    .lcomm y, 8
```

Para cada declaração, a expressão é calculada em `%rax` e depois armazenada na variável:

```asm
    mov %rax, x
```

Para cada uso de variável, o valor é carregado para `%rax`:

```asm
    mov x, %rax
```

Ao final, a expressão resultado deixa seu valor em `%rax`, e o runtime imprime esse valor com `imprime_num`.

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

Em um ambiente Linux x86-64 com GNU assembler e linker disponíveis, o assembly pode ser montado e linkado com:

```bash
as --64 -o programa.o programa.s
ld -o programa programa.o
./programa
```

---

# Como Executar os Testes

Os testes locais podem ser executados com:

```bash
make test
```

ou:

```bash
python3 testes.py
```

A suíte é dividida por etapa do compilador:

* `lexer_tests.py`: tokens de EV e erros léxicos;
* `parser_tests.py`: estrutura de programas, declarações e expressão final;
* `semantico_tests.py`: uso correto e incorreto de variáveis;
* `geracao_tests.py`: assembly gerado e execução dos binários quando o ambiente permite.

Em máquinas que não possuem GNU `as`, `ld` ou não são Linux x86-64, os testes executáveis de geração são ignorados localmente.

Para rodar a validação completa em Docker:

```bash
make docker-test
```

Esse comando monta, linka e executa os binários gerados em um ambiente Linux x86-64.

---

# Objetivo da Atividade

O objetivo desta atividade foi adaptar o compilador para reconhecer programas com declarações e uso de variáveis, mantendo as regras de precedência e associatividade da EC2, adicionando análise semântica para variáveis não declaradas e gerando assembly funcional com armazenamento em memória.
