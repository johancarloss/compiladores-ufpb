# Atividade 05 — Análise Sintática da Linguagem EC1

Analisador sintático (parser) para a linguagem **EC1** (Expressões Constantes 1). A partir dos tokens do analisador léxico, constrói uma árvore de sintaxe abstrata (AST) e calcula o valor da expressão por interpretação (tree-walking).

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 05

---

## Estrutura

```
lexer.py         # análise léxica (reusado da atividade 04)
arvore.py        # AST: classes Const e OpBin, com avaliar() e __str__()
parser.py        # análise sintática descendente recursiva
main.py          # CLI: lê arquivo, analisa, imprime a árvore e o valor
run_tests.sh     # roda os casos de teste
Makefile         # atalhos (make test, make clean)
tests/           # casos de teste (.ec1 com .out esperado)
```

## Requisitos

Python 3 (sem dependências externas).

## Como executar

```bash
python3 main.py <arquivo.ec1>
```

Para um programa válido, imprime a árvore sintática (reconstruída) e o valor da expressão:

```
$ python3 main.py exemplo.ec1
Arvore: (33 + (912 * 11))
Valor: 10065
```

Em caso de erro léxico ou sintático, imprime a mensagem de erro e retorna código de saída `1`.

## Como rodar os testes

```bash
make test
```

Compara a saída do `main.py` em cada arquivo `.ec1` de `tests/` com a saída esperada no `.out` de mesmo nome. Os testes cobrem expressões válidas (verificando árvore e valor), erros de sintaxe e erro léxico.

## Linguagem EC1 (gramática)

```bnf
<programa>   ::= <expressao>
<expressao>  ::= <literal> | '(' <expressao> <operador> <expressao> ')'
<operador>   ::= '+' | '-' | '*' | '/'
<literal>    ::= <digito>+
<digito>     ::= '0' | '1' | '2' | ... | '9'
```

Especificação completa: [`../docs/atividade-05-especificacao.md`](../docs/atividade-05-especificacao.md).

## Autores

- Johan Carlos
- Luiz Augusto
- Diego de Carvalho
- Gabriel Lizst
