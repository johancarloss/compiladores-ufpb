# Atividade 09 — Comandos (linguagem Cmd)

Este projeto implementa o compilador para a linguagem **Cmd**, a evolução da linguagem EV (Atividade 08). A Cmd adiciona **comando condicional (`if`/`else`), comando de repetição (`while`), atribuição e operadores de comparação** (`<`, `>`, `==`). Com `if` e `while`, a linguagem passa a ser **Turing-completa**.

O compilador realiza análise léxica, análise sintática, análise semântica, construção da AST e geração de código assembly **x86-64** para Linux (usando `cmp`, instruções `set` e saltos com rótulos).

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 09

## A linguagem Cmd

Um programa é `<declarações>* { <comandos>* return <exp>; }`:

```
n = 1;
m = 10;
soma = 0;
{
  while n < m {
    soma = soma + n;
    n = n + 1;
  }
  return soma;
}
```

- **Declarações** (antes do corpo) criam variáveis: `x = exp;`
- **Comandos** (dentro do `{}`): `if E { } else { }`, `while E { }`, atribuição `x = exp;`
- **Comparações** `<`, `>`, `==` têm a precedência mais baixa. Zero é falso; diferente de zero é verdadeiro.
- **Atribuição** só altera variável já declarada (não cria variável nova).
- As chaves nos corpos de `if` e `while` são obrigatórias, e o `else` também.

Especificação completa: [`../docs/atividade-09-especificacao.md`](../docs/atividade-09-especificacao.md).

---

# Estrutura dos Arquivos em `atv09/`

```text
├── arvore.py        # Definição das classes da AST
├── lexer.py         # Analisador léxico
├── parser.py        # Parser da linguagem Cmd
├── semantico.py     # Análise semântica da linguagem Cmd
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

# O que mudou em relação à Atividade 08 (EV)

A EV só tinha declarações de variáveis e uma expressão de resultado. A Cmd adiciona:

- **Comparações** `<`, `>`, `==` (precedência mais baixa que a aritmética).
- **Corpo com chaves e `return`**: `{ <comandos> return <exp>; }`.
- **Comandos**: `if E { } else { }`, `while E { }` e atribuição `x = exp;`.

Como agora dá pra tomar decisões e repetir, a linguagem é Turing-completa.

# Fases do compilador (o que cada uma ganhou)

- **Léxica** (`lexer.py`): tokens `{` `}` `<` `>` `==` e palavras-chave `if`/`else`/`while`/`return`. O `==` é diferenciado de `=` olhando o próximo caractere; palavras-chave são identificadores testados contra uma tabela.
- **AST** (`arvore.py`): nós de comando `If`, `While`, `Atrib`; o `Programa` passa a ter `(declaracoes, comandos, resultado)`. Comparações reusam `OpBin`.
- **Sintática** (`parser.py`): novo nível `analisa_exp` (comparação) acima do aditivo, e funções para corpo e comandos.
- **Semântica** (`semantico.py`): atribuição só a variável já declarada, verificando também dentro de `if`/`while`.
- **Geração** (`compilador.py`): comparações via `cmp` + `setl`/`setg`/`setz`; `if`/`while` via saltos (`jz`/`jmp`) e rótulos únicos gerados por um contador (`Lfalso0`, `Lfim0`, `Linicio1`...).

---

# Como Executar

Para compilar um arquivo Cmd para Assembly:

```bash
python3 compilador.py <arquivo.cmd> <saida.s>
```

Exemplo:

```bash
python3 compilador.py programa.cmd programa.s
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

* `lexer_tests.py`: tokens da Cmd (chaves, comparações, palavras-chave) e erros léxicos;
* `parser_tests.py`: declarações, corpo, `if`, `while` e precedência de comparação;
* `semantico_tests.py`: uso e atribuição a variáveis declaradas/não declaradas;
* `geracao_tests.py`: assembly gerado e execução dos binários quando o ambiente permite.

Em máquinas que não possuem GNU `as`, `ld` ou não são Linux x86-64, os testes executáveis de geração são ignorados localmente.

Para rodar a validação completa em Docker:

```bash
make docker-test
```

Esse comando monta, linka e executa os binários gerados em um ambiente Linux x86-64.

---

# Objetivo da Atividade

O objetivo desta atividade foi tornar a linguagem Turing-completa, adicionando comando condicional (`if`/`else`), comando de repetição (`while`), atribuição e operadores de comparação. Isso exigiu mudanças em todas as fases do compilador: novos tokens e palavras-chave na análise léxica, um novo nível de precedência e comandos na análise sintática, verificação de atribuição a variável declarada na análise semântica, e geração de código com comparações (via flags do processador) e saltos com rótulos únicos.
