# Changelog

Histórico de evolução do projeto da disciplina de Construção de Compiladores (UFPB — P6 — 2026.1).

Organizado por atividade. Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Não lançado]

### Em progresso
- **Atividade 05** — Análise sintática da EC1: parser descendente recursivo, árvore de sintaxe abstrata (AST) e interpretador tree-walking. Em Python, reusando o analisador léxico da atividade 04.

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
