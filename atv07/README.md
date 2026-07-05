# Atividade 06 — Geração de Código para a Linguagem EC1

Este projeto implementa a etapa final (Geração de Código) do compilador para a linguagem **EC1** (Expressões Constantes 1). O compilador lê arquivos com expressões aritméticas de operandos constantes usando as quatro operações básicas (Soma, Subtração, Multiplicação e Divisão) sempre encapsuladas por parênteses, analisa-os e gera código assembly **x86-64** para Linux, utilizando a pilha do sistema para o cálculo das subexpressões.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)  
**Professor:** Andrei Formiga  
**Atividade:** 06  

---

## Estrutura dos Arquivos em `atv06/`

```
├── arvore.py       # Definição das classes da AST (herdado da atv05)
├── lexer.py        # Analisador léxico para extração de tokens (herdado da atv05)
├── parser.py       # Analisador sintático que gera a AST (herdado da atv05)
├── runtime.s       # Runtime com funções de suporte para entrada/saída em assembly (de atv02)
├── compilador.py   # Gerador de código recursivo que produz arquivos assembly .s
├── testes.py       # Script de testes automatizados com verificação de resultados
├── Makefile        # Atalhos rápidos de execução para testes e limpeza
└── README.md       # Este arquivo com documentação e nota teórica de otimização
```

---

## Regras de Tradução de Código Assembly

O compilador gera código para arquitetura **x86-64** seguindo estritamente as diretrizes abaixo:

1. **Destino do resultado**: O resultado de qualquer expressão ou subexpressão é colocado no registrador `%rax`.
2. **Constantes**: Para traduzir um operando constante, gera-se: `mov $VALOR, %rax`.
3. **Pilha para operações binárias**: As subexpressões intermediárias são salvas utilizando a pilha do sistema com as instruções `push` e `pop`.
4. **Ordem de Tradução (Crucial para Subtrações e Divisões)**:
   - Passo 1: Executa a geração recursiva de código para o **operando direito** (o resultado vai para `%rax`).
   - Passo 2: Salva esse valor empilhando-o com `push %rax`.
   - Passo 3: Executa a geração recursiva de código para o **operando esquerdo** (o resultado vai para `%rax`).
   - Passo 4: Desempilha o operando direito no registrador `%rbx` usando `pop %rbx`.
   - Passo 5: Executa a instrução correspondente ao operador em `%rax` usando `%rbx`:
     - Soma (`+`): `add %rbx, %rax` (faz `%rax = %rax + %rbx` -> `esquerdo + direito`)
     - Subtração (`-`): `sub %rbx, %rax` (faz `%rax = %rax - %rbx` -> `esquerdo - direito`)
     - Multiplicação (`*`): `imul %rbx, %rax` (faz `%rax = %rax * %rbx` -> `esquerdo * direito`)
     - Divisão (`/`): `cqto` (extende o sinal de `%rax` para `%rdx:%rax`) e `idiv %rbx` (divide `%rdx:%rax` por `%rbx`, guardando o quociente em `%rax`)

---

## Como Executar o Compilador

Para compilar uma expressão EC1 para assembly x86-64, execute o `compilador.py` passando o arquivo de entrada contendo a expressão e o arquivo `.s` onde o assembly será salvo:

```bash
python3 compilador.py <arquivo.ec1> <saida.s>
```

### Exemplo
Seja o arquivo `expressao.ec1` com o conteúdo `(7+11)`. Rodando:
```bash
python3 compilador.py expressao.ec1 expressao.s
```

O arquivo `expressao.s` gerado conterá:
```assembly
.section .text
.globl _start
_start:
    # --- Início do Código Gerado ---
    # Operação: (7 + 11)
    # Passo 1: operando direito
    # Constante 11
    mov $11, %rax
    # Passo 2: push %rax
    push %rax
    # Passo 3: operando esquerdo
    # Constante 7
    mov $7, %rax
    # Passo 4: pop %rbx
    pop %rbx
    # Passo 5: aplicar operador +
    add %rbx, %rax
    # --- Fim do Código Gerado ---

    call imprime_num
    call sair
    .include "runtime.s"
```

---

## Como Rodar os Testes

Os testes automatizados podem ser executados usando o script `testes.py` ou o atalho do `Makefile`:

```bash
make test
```
*(ou `python3 testes.py`)*

### Funcionamento dos Testes:
1. O script gera os arquivos `.ec1` e `.s` de teste dentro de uma pasta chamada `tests/` para vários casos, incluindo as expressões exigidas: `(7+11)`, `(11-7)` e `(7+(3+8))`.
2. Para cada teste, ele avalia a expressão diretamente com o interpretador embutido para descobrir o resultado esperado.
3. Se o script for executado em um ambiente **Linux x86-64** que possua o assembler `as` e linker `ld`, ele automaticamente:
   - Monta o arquivo assembly: `as --64 -o tests/teste_x.o tests/teste_x.s`
   - Linka o objeto gerado: `ld -o tests/teste_x tests/teste_x.o`
   - Executa o binário resultante e lê a saída impressa no terminal.
   - Compara o valor obtido da execução real com o valor esperado pelo interpretador, atestando a corretude de ponta a ponta.
4. Se o script rodar em um host **Windows ou outra plataforma**, ele realizará a compilação estática do arquivo `.s` e executará o `as` (se disponível) para validar a correção da sintaxe do assembly gerado, ignorando a linkagem e a execução nativa.

Para limpar os arquivos intermediários criados pelos testes:
```bash
make clean
```

### Executando com validação completa via Docker (Recomendado no Windows)

Como você está em um host Windows e o assembly gerado é direcionado para Linux x86-64, a execução dos binários é ignorada localmente por padrão (embora a montagem seja verificada). Para compilar, linkar e **executar** todos os testes na arquitetura real usando Docker, basta rodar:

```bash
make docker-test
```

Isso irá:
1. Construir uma imagem Docker (`atv06-comp`) baseada no Linux (Debian/Python) contendo a toolchain de desenvolvimento (`as`, `ld`).
2. Copiar os fontes e rodar o script de testes dentro de um contêiner.
3. Exibir a saída da execução real dos binários com os resultados correspondentes (ex: `[PASS] Saída do executável: 18 (Igual ao esperado)`).

---

