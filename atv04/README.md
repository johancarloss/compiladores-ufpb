# Atividade 04 — Análise Léxica da Linguagem EC1

Analisador léxico (lexer) para a linguagem **EC1** (Expressões Constantes 1): expressões aritméticas com constantes inteiras e os operadores `+ - * /`, com parênteses obrigatórios em toda operação.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 04

---

## Estrutura

```
token.h          # tipos de token (enum) e estrutura Token
lexer.h          # interface do analisador léxico
lexer.c          # implementação do analisador léxico
main.c           # CLI: lê arquivo, chama lexer, imprime tokens
Makefile         # build e testes
README.md        # este arquivo
tests/           # casos de teste (.ec1 com .out esperado)
```

## Como compilar

```bash
make
```

Gera o executável `lexer`.

## Como executar

```bash
./lexer <arquivo.ec1>
```

Imprime a sequência de tokens no formato `<tipo, "lexema", posicao>`, um por linha.

Em caso de erro léxico, imprime `Erro léxico na posição X: caractere inválido 'Y'` em `stderr` e retorna código de saída `1`.

## Como rodar os testes

```bash
make test
```

Compara a saída padrão do `lexer` (`stdout`) em cada arquivo `.ec1` de `tests/` com a saída esperada no arquivo `.out` de mesmo nome. Cada caso de teste usa um par `tests/{nome_teste}.ec1` e `tests/{nome_teste}.out`.

Exemplo de teste passando:

```text
== literal_simples ==
input: tests/literal_simples.ec1
expected: tests/literal_simples.out
PASS
```

Exemplo de teste falhando:

```text
== literal_simples ==
input: tests/literal_simples.ec1
expected: tests/literal_simples.out
FAIL
```

## Linguagem EC1 (gramática)

```bnf
<programa>   ::= <expressao>
<expressao>  ::= <literal> | '(' <expressao> <operador> <expressao> ')'
<operador>   ::= '+' | '-' | '*' | '/'
<literal>    ::= <digito>+
<digito>     ::= '0' | '1' | '2' | ... | '9'
```

Especificação completa: [`../docs/atividade-04-especificacao.md`](../docs/atividade-04-especificacao.md).

## Autores

- Johan Carlos
- Luiz Augusto
- Diego de Carvalho
- Gabriel Lizst
