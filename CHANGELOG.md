# Changelog

Histórico de evolução do projeto da disciplina de Construção de Compiladores (UFPB — P6 — 2026.1).

Organizado por atividade. Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Atividade 08] — Expressões com Variáveis (EV) — 2026-07-08

### Adicionado
- Linguagem EV: suporte a programas com declarações de variáveis e expressão final, usando a forma `x = exp;` para declarações e `= exp` para o resultado do programa.
- Lexer: reconhecimento de identificadores, sinal de igualdade e ponto-e-vírgula, além de erro léxico para sequências inválidas como `237abc` e `9valor`.
- AST: novos nós `Programa`, `Decl` e `Var`, mantendo `Const` e `OpBin` para expressões aritméticas.
- Parser: novo não-terminal inicial para programas, preservando precedência e associatividade da EC2 em expressões com números, variáveis e parênteses.
- Análise semântica (`semantico.py`): verificação de uso de variáveis somente após declaração, com erro específico para variável não declarada.
- Gerador de código: emissão de seção `.bss` para variáveis, armazenamento de declarações em memória e carregamento de variáveis para `%rax`.
- Suíte de testes modular em `tests/`, separada por lexer, parser, semântico, geração de código e infraestrutura de ambiente.
- Testes end-to-end via Docker para montar, linkar e executar os binários gerados em Linux x86-64.

### Reusado
- Runtime de impressão (`runtime.s`) e geração de expressões aritméticas herdados das atividades anteriores.

## [Atividade 06] — Compilador EC1 Completo — 2026-06-10

### Adicionado
- Gerador de código (`compilador.py`): traduz a árvore sintática para assembly x86-64, usando a pilha (`push`/`rax`/`pop`) para armazenar resultados intermediários. Gera o operando direito primeiro para manter a ordem correta em subtração e divisão. Salva a saída em arquivo `.s`.
- Runtime (`runtime.s`): funções `imprime_num` e `sair` (reusado da atividade 02).
- Suíte de 10 testes (`testes.py`) com verificação automática: interpreta a expressão, monta o assembly com `as`, linka com `ld` e executa o binário, comparando o resultado real. Em hosts não-x86-64, valida apenas a montagem.
- Dockerfile para rodar os testes (montagem + execução real) em ambiente x86-64.

### Reusado
- Léxico, parser e AST das atividades 04 e 05 (`lexer.py`, `parser.py`, `arvore.py`).

## [Atividade 05] — Análise Sintática da EC1 — 2026-05-27

### Adicionado
- Analisador sintático descendente recursivo (`parser.py`): uma função por não-terminal da gramática (`analisa_exp`, `analisa_operador`), produzindo a árvore de sintaxe abstrata.
- Árvore de sintaxe abstrata (`arvore.py`): classes `Const` e `OpBin`, com método `avaliar()` (interpretador tree-walking) e `__str__()` (reconstrói a expressão).
- CLI (`main.py`): lê o arquivo, faz análise léxica + sintática, imprime a árvore e o valor da expressão.
- Suíte de 12 testes: expressões válidas (verificando árvore e valor), erros de sintaxe e erro léxico.

### Reusado
- Analisador léxico da atividade 04 (`lexer.py`, copiado para a pasta da atividade).

## [Atividade 04] — Análise Léxica da EC1 — 2026-05-27

### Adicionado
- Analisador léxico da linguagem EC1 (`lexer.py`): reconhece números, parênteses e os operadores `+ - * /`, ignora whitespace e detecta erros léxicos reportando a posição.
- Suíte de 11 testes (`run_tests.sh` + `tests/`): expressões válidas, whitespace variado (espaços, tabs, múltiplas linhas), erros léxicos e casos extremos (arquivo vazio, erro na primeira posição).
- Documentação de uso no `README.md`.

### Mudado
- Lexer migrado de **C para Python** (decisão do grupo) para simplificar a implementação das próximas atividades. As partes novas (parser, AST, interpretador) ficam mais diretas em Python.

## [Atividade 03] — Congruência de Zeller — 2026-05-20

### Adicionado
- Programa em assembly x86-64 (`zeller.s`) que calcula o dia da semana de qualquer data usando a congruência de Zeller.
- Programa de verificação em Python (`zeller.py`) para validar os resultados do assembly.
- Respostas das perguntas teóricas sobre alocação de registradores na tradução de expressões (`respostas.md`).

## [Atividade 02] — Compilador CI (Constantes Inteiras)

### Adicionado
- Compilador da linguagem CI em C: lê uma constante inteira e gera assembly x86-64 GAS que imprime o valor.
- Tratamento de erro de sintaxe e detecção de overflow.
- Dockerfile, Makefile e conjunto de testes.

## [Atividade 01] — Questionário Inicial

### Adicionado
- Pasta da atividade. Atividade individual feita em sala; as respostas não são versionadas (cada integrante mantém a sua).

## [Estrutura inicial] — 2026-05-17

### Adicionado
- Estrutura do repositório com índice de atividades no `README.md`, `.gitignore` e pasta `docs/` com as transcrições dos enunciados.
