# Atividade 02 — Compilador CI (Constantes Inteiras)

> **Metadados do PDF original**
> - **Arquivo:** `CC - Atividade 02.pdf`
> - **Autor:** Andrei Formiga (professor)
> - **Data:** 04 de maio de 2026
> - **Páginas:** 9
> - **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Transcrição fiel + comentários pedagógicos do PDF da atividade. Onde aparecer **citação textual** do professor, marca como blockquote. Onde aparecer comentário/inferência, marca como **Observação:**.

---

## Sumário do PDF

1. [Introdução](#1-introdução-página-3)
2. [A linguagem CI (Constantes Inteiras)](#2-a-linguagem-ci-constantes-inteiras-página-4)
3. [O compilador](#3-o-compilador-páginas-5-6)
4. [A estrutura de um compilador](#4-a-estrutura-de-um-compilador-página-7)
5. [O que deve ser entregue](#5-o-que-deve-ser-entregue-página-8)
6. [Próximas Etapas](#6-próximas-etapas-página-9)

E mais (acréscimos meus):

- [Apêndice A — Referência rápida da especificação](#apêndice-a--referência-rápida-da-especificação)
- [Apêndice B — Gramática BNF isolada](#apêndice-b--gramática-bnf-isolada)
- [Apêndice C — Template assembly pronto pra copiar](#apêndice-c--template-assembly-pronto-pra-copiar)
- [Apêndice D — Checklist de entrega](#apêndice-d--checklist-de-entrega)
- [Apêndice E — Glossário de termos do professor](#apêndice-e--glossário-de-termos-do-professor)

---

## 1. Introdução (página 3)

> **Citação textual do PDF:**
> *"Nesta atividade o objetivo é criar um compilador completo para uma linguagem extremamente simples. O propósito é mostrar as etapas de um compilador no contexto mais simples possível. Nas próximas atividades a complexidade da linguagem e do compilador vai aumentar gradualmente."*

**Pontos centrais:**

- O objetivo é **construir um compilador completo** — não um pedaço, não um fragmento. Completo, ponta-a-ponta.
- A linguagem foi escolhida pra ser **extremamente simples** propositalmente.
- A simplicidade é **didática**: serve pra mostrar as etapas sem distração.
- Existe uma promessa explícita: **a complexidade vai crescer gradualmente** em atividades futuras.

**Observação pedagógica:**
O professor está pavimentando expectativa pra a disciplina inteira — o compilador desta atividade é o **esqueleto** que vai engordar nas próximas. Ou seja, o código que você escrever agora vai ser **base de tudo** que vier depois. Capricho aqui economiza retrabalho lá na frente.

---

## 2. A linguagem CI (Constantes Inteiras) (página 4)

> **Citação textual do PDF:**
> *"Um programa na linguagem CI é apenas uma constante inteira, formada por um ou mais dígitos. Uma gramática para essa linguagem pode ser especificada da seguinte forma:"*

**Gramática formal em BNF (Backus-Naur Form):**

```bnf
<programa>        ::= <literal-inteiro>
<literal-inteiro> ::= <digito>+
<digito>          ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

**Como ler essa gramática:**

| Símbolo | Significado |
|---|---|
| `<...>` | "símbolo não-terminal" — uma categoria que se expande em outras coisas |
| `::=` | "é definido como" |
| `\|` | "ou" — alternativas |
| `+` | "um ou mais" — repetição (como em regex) |
| `0`, `1`, ..., `9` | símbolos terminais — caracteres literais |

**Lendo em português:**
- Um `<programa>` é um `<literal-inteiro>`
- Um `<literal-inteiro>` é uma sequência de **um ou mais** `<digito>`
- Um `<digito>` é qualquer um dos 10 dígitos decimais

**Exemplo de programa válido (citação textual):**

```
42
```

**Observação pedagógica:**
A gramática **não permite sinal negativo** (`-42` seria inválido pela gramática). Ela **não permite espaços** entre dígitos. Ela **não permite múltiplos números**. Ela **não permite `0x1A`** ou outras notações. **Só dígitos decimais grudados.**

> **Citação textual sobre a limitação:**
> *"A linguagem CI é extremamente limitada como linguagem de programação; a única capacidade dos programas em CI é imprimir diferentes constantes inteiras na tela. Mesmo assim, já é possível aprender ideias mais gerais sobre compiladores mesmo nessa simplicidade."*

**Pontos centrais:**

- A **única coisa** que um programa CI faz é **imprimir uma constante na tela**.
- Mesmo nessa simplicidade, dá pra extrair lições gerais sobre compiladores.

---

## 3. O compilador (páginas 5-6)

### 3.1. Estrutura geral do pipeline (página 5)

> **Citação textual:**
> *"Os compiladores que veremos na disciplina seguem a mesma estrutura: a partir do código-fonte na entrada, o compilador vai gerar um programa equivalente em linguagem assembly. Este programa em assembly precisa ser montado (por um assembler, ou montador em português) e ligado por um linker para se tornar um executável (Figura 1)."*

**Diagrama da Figura 1 (transcrito em ASCII):**

```
┌──────────────────┐
│   código fonte   │  ← arquivo .ci escrito por você
└──────────────────┘
         │
         ▼
┌──────────────────┐
│   compilador     │  ← O QUE VOCÊ VAI ESCREVER
└──────────────────┘
         │
         ▼
┌──────────────────┐
│     assembly     │  ← arquivo .s gerado pelo compilador
└──────────────────┘
         │
         ▼
┌──────────────────┐
│    assembler     │  ← programa externo (`as` do GNU)
└──────────────────┘
         │
         ▼
┌──────────────────┐
│   código objeto  │  ← arquivo .o
└──────────────────┘
         │
         ▼
┌──────────────────┐
│      linker      │  ← programa externo (`ld` do GNU)
└──────────────────┘
         │
         ▼
┌──────────────────┐
│    executável    │  ← arquivo binário rodável
└──────────────────┘
```

**Pontos centrais:**

- O **compilador** que você escreve é UM bloco no meio do pipeline.
- Os blocos **assembler** (`as`) e **linker** (`ld`) **já existem** — você apenas invoca.
- Cada bloco tem entrada e saída bem definidas (em formato de arquivo).

**Observação pedagógica:**
Não confundir **compilador** (que gera `.s`) com **assembler** (que gera `.o`) com **linker** (que gera o executável). São três ferramentas distintas, com responsabilidades distintas. Em projetos grandes (gcc, rustc), essas três etapas são embaladas num único comando — mas conceitualmente são separadas.

### 3.2. O que o compilador CI especificamente faz (página 6)

> **Citação textual:**
> *"O compilador desta atividade deve ler o programa em um arquivo e gerar um programa assembly na saída que imprime o resultado do programa. A maior parte deste programa vai seguir um modelo que veremos em seguida; o que o compilador CI precisa gerar é apenas uma linha desse programa assembly: uma instrução que coloca o resultado do programa no registrador RAX."*

**Insight crítico:**
O compilador gera **uma única linha** de código novo. O resto é template fixo. Isso muda completamente a complexidade percebida — não é "gerar um programa assembly", é "preencher um buraco num template".

> **Exemplo textual do professor:**
> *"Por exemplo, se o arquivo `p1.ci` contém a constante 42, o compilador deve gerar a seguinte linha de código assembly:"*

```gas
mov $42, %rax
```

**Decomposição dessa instrução (sintaxe AT&T do GAS):**

| Elemento | Significado |
|---|---|
| `mov` | mnemônico — mover/copiar valor |
| `$42` | **imediato** (literal numérico) — sintaxe AT&T usa `$` antes de constantes |
| `%rax` | **registrador** RAX (64-bit) — sintaxe AT&T usa `%` antes de registradores |
| `mov $X, %Y` | ordem AT&T: **fonte primeiro, destino depois** (oposto da sintaxe Intel) |

### 3.3. Arquitetura, sistema operacional e assembler usados

> **Citação textual:**
> *"Os exemplos na disciplina usarão a linguagem assembly para a arquitetura x86-64 e a sintaxe do GNU Assembler (gas), executando em um sistema operacional de kernel Linux. Cada grupo pode escolher gerar código para outras arquiteturas, outros sistemas operacionais, e/ou mudar o assembler utilizado."*

**Padrão da disciplina:**

| Item | Valor |
|---|---|
| Arquitetura | x86-64 |
| Assembler | GAS (GNU Assembler) |
| Sintaxe | AT&T |
| Sistema operacional | Linux |

**Liberdade:** Cada grupo pode mudar qualquer um desses (ARM, MASM/NASM, macOS, etc.). Mas o padrão da disciplina é o conjunto acima.

### 3.4. O modelo (template) do arquivo assembly de saída

> **Citação textual do template:**

```gas
#
# modelo de saida para o compilador
#

.section .text
.globl _start

_start:
    ## saida do compilador deve ser inserida aqui

    call imprime_num
    call sair

.include "runtime.s"
```

**Decomposição do template:**

| Linha | Significado |
|---|---|
| `#...` | comentário em GAS começa com `#` |
| `.section .text` | diretiva: tudo que vier abaixo vai pra **seção de código** (instruções executáveis) |
| `.globl _start` | diretiva: torna o símbolo `_start` **visível para o linker** (entry point do programa) |
| `_start:` | rótulo (label) — onde o programa começa a executar |
| `## saida do compilador deve ser inserida aqui` | **PLACEHOLDER** — aqui vai a linha gerada pelo compilador |
| `call imprime_num` | chama o procedimento que imprime o valor em RAX |
| `call sair` | chama o procedimento que encerra o programa |
| `.include "runtime.s"` | diretiva: cola o conteúdo de `runtime.s` aqui no momento da montagem |

> **Citação textual sobre onde inserir a linha:**
> *"A linha gerada pelo compilador deve ser colocada no local marcado com o comentário, logo após o rótulo `_start`."*

### 3.5. O runtime (procedimentos `imprime_num` e `sair`)

> **Citação textual:**
> *"Podemos ver que esse modelo chama o procedimento `imprime_num` (que imprime na tela o valor do registrador RAX como um inteiro) e depois o procedimento `sair` para sinalizar ao sistema operacional que o programa acabou. O arquivo `runtime.s` que é incluído ao final do modelo contém as definições desses procedimentos."*
>
> *"Por enquanto não é necessário entender o modelo utilizado nem o arquivo `runtime.s`. Faremos uma revisão sobre assembly em breve."*

**Pontos centrais:**

- `imprime_num` — lê o valor em `%rax` e imprime na tela como inteiro decimal.
- `sair` — encerra o programa (provavelmente via syscall `exit`).
- O arquivo `runtime.s` é **fornecido pelo professor** (você não escreve).
- **Não precisa entender agora** como `imprime_num` e `sair` funcionam internamente — vai ver depois.

**Observação pedagógica:**
Esse é um padrão clássico: separar a parte "boring" (printar inteiro, syscalls de exit) numa biblioteca de runtime, e deixar você focar só no que tá aprendendo (gerar `mov $N, %rax`). Em compiladores grandes, runtime é tudo que o programa precisa pra rodar mas não foi gerado pelo compilador (garbage collector, IO básico, etc.).

### 3.6. Comandos para montar e linkar

> **Citação textual:**
> *"O arquivo assembly gerado pelo compilador (contendo a linha de resultado inserida no modelo acima) deve ser montado e linkado. Se o arquivo gerado pelo compilador foi chamado de `p1.s`, os comandos para montar e linkar são:"*

```bash
as --64 -o p1.o p1.s
ld -o p1 p1.o
```

**Decomposição:**

| Comando | Função |
|---|---|
| `as` | invoca o GNU Assembler |
| `--64` | flag pra forçar montagem 64-bit |
| `-o p1.o` | output: arquivo objeto `p1.o` |
| `p1.s` | input: arquivo assembly gerado pelo compilador |
| `ld` | invoca o GNU Linker |
| `-o p1` | output: executável `p1` |
| `p1.o` | input: arquivo objeto |

> **Citação textual:**
> *"Isso gera o executável de nome `p1` que, ao ser executado, vai imprimir a constante inteira que estava no arquivo fonte original na tela."*

**Importante:** O **usuário** roda esses comandos manualmente. O **compilador** não invoca `as` nem `ld`. Ele só gera o `.s` e termina.

---

## 4. A estrutura de um compilador (página 7)

### 4.1. Algoritmo inicial (3 passos)

> **Citação textual:**
> *"Se pensarmos sobre como deve ser o algoritmo do compilador CI, vemos que pelo menos os seguintes passos são necessários:"*
>
> *"1. Ler o arquivo de entrada"*
> *"2. Usar a constante lida no arquivo de entrada e o modelo da saída para gerar o programa assembly resultante"*
> *"3. Escrever o programa de saída no arquivo de saída"*

### 4.2. Tratamento de erros — primeira motivação

> **Citação textual:**
> *"Esse algoritmo não leva em consideração o que acontece caso o programa de entrada tenha um erro de sintaxe; para a linguagem CI, um erro de sintaxe significa que o arquivo de entrada não contém uma constante inteira correta (por exemplo, inclui letras)."*
>
> *"Isso demonstra a necessidade do tratamento de erros. Se o programa na entrada não contém uma constante inteira correta, não será possível gerar o arquivo de saída."*

**Pontos centrais:**

- Erro de sintaxe em CI = arquivo não contém constante inteira válida.
- Exemplos de entradas inválidas: `4a2`, `hello`, `4 2`, `42.0`, `-42` (esse último é discutível mas, pela gramática estrita, é inválido).
- Quando erro de sintaxe acontece, o compilador **não deve gerar** o arquivo `.s`.

### 4.3. Erro opcional — overflow

> **Citação textual entre parênteses:**
> *"(Outro tipo de erro que pode ocorrer é a constante no programa de entrada ser grande demais para caber em um registrador de 64 bits. A verificação desse tipo de erro é um pouco mais difícil e é opcional para esta atividade)."*

**Pontos centrais:**

- Constantes acima de `9_223_372_036_854_775_807` (i64 máximo) ou `18_446_744_073_709_551_615` (u64 máximo) **estouram** o registrador.
- **Detectar overflow é OPCIONAL** nessa atividade.
- Em Rust, isso é "de graça" se você usar `parse::<i64>()` ou `parse::<u64>()` — o parse já retorna erro se não couber.

### 4.4. Algoritmo refinado (4 passos)

> **Citação textual:**
> *"Vamos incluir mais um passo no algoritmo:"*
>
> *"1. Ler o arquivo de entrada"*
> *"2. Verificar se o arquivo de entrada contém uma constante inteira"*
> *"3. Usar a constante lida no arquivo de entrada e o modelo da saída para gerar o programa assembly resultante"*
> *"4. Escrever o programa de saída no arquivo de saída"*

### 4.5. Análise vs Síntese

> **Citação textual (importante — vocabulário recorrente da disciplina):**
> *"Neste compilador muito simples vemos que um compilador pode ser dividido em duas etapas principais: uma etapa de **análise** e outra etapa de **síntese ou geração**. A etapa de análise é responsável por coletar as informações necessárias do programa de entrada, ao mesmo tempo verificando pela presença de erros na entrada. A síntese gera o programa de saída, usando as informações coletadas durante a análise."*
>
> *"A verificação de sintaxe no passo 2 do algoritmo acima é a etapa de análise do compilador CI. O passo 3 é a etapa de síntese ou geração de código."*
>
> *"Todos os compiladores que veremos nesta disciplina seguirão essa estrutura de análise e síntese."*

**Mapeamento dos passos do algoritmo:**

| Passo | Etapa do compilador | Categoria |
|---|---|---|
| 1. Ler arquivo | infraestrutura | (nenhuma das duas) |
| 2. Verificar inteiro | **análise** | análise |
| 3. Gerar assembly | **síntese** (ou geração) | síntese |
| 4. Escrever arquivo | infraestrutura | (nenhuma das duas) |

**Observação pedagógica:**
Esse vocabulário **análise / síntese** é o esqueleto conceitual da disciplina inteira. Em compiladores grandes:

- **Análise** se quebra em: léxica → sintática → semântica.
- **Síntese** se quebra em: geração de IR → otimização → geração de código alvo.

Mas a divisão de 2 estágios continua valendo. Memorize esse vocabulário agora.

---

## 5. O que deve ser entregue (página 8)

### 5.1. Interface de linha de comando

> **Citação textual:**
> *"O compilador deve receber, como argumento na linha de comando, o nome do arquivo que contém o programa a ser compilado. Por exemplo, se o executável do compilador se chamar `compci` e o arquivo de entrada for `p1.ci`, a forma de compilar o arquivo deve ser chamar o compilador na linha de comando da seguinte forma:"*

```bash
compci p1.ci
```

> **Citação textual (restrição importante):**
> *"O programa não deve compilar um arquivo de entrada de nome fixo nem deve receber o nome do arquivo de entrada (ou o programa de entrada) pela leitura do teclado. Isso é importante para facilitar os testes."*

**Restrições:**

- ❌ **NÃO pode** hardcodar nome do arquivo (`open("p1.ci")` direto no código).
- ❌ **NÃO pode** ler do `stdin` (teclado).
- ✅ **DEVE** receber o nome do arquivo como **argumento da linha de comando**.

**Motivação:** facilita execução automatizada de testes (CI/CD, scripts).

### 5.2. Saída esperada

> **Citação textual:**
> *"O compilador deve produzir, na saída, um arquivo assembly que segue o modelo apresentado neste guia, mas que inclui a linha com a instrução `mov` que coloca o valor da constante no registrador RAX. Este arquivo assembly deve poder ser montado e linkado corretamente para gerar um executável que imprime a constante na tela (desde que o arquivo `runtime.s`, fornecido, esteja presente no mesmo diretório."*

**Pontos centrais:**

- A saída é um arquivo `.s`.
- O `.s` deve seguir o **modelo (template)** exato.
- O `.s` deve incluir a **linha gerada** com a constante.
- O `.s` deve poder ser montado/linkado **sem erros**.
- O executável resultante deve **imprimir** a constante.
- Pré-requisito: `runtime.s` deve estar no **mesmo diretório**.

**Observação:** O PDF não especifica o nome exato do arquivo de saída. Convenção implícita do exemplo: `p1.ci` → `p1.s` (mesmo nome base, extensão trocada).

### 5.3. Itens a entregar

> **Citação textual:**
> *"O grupo deve enviar o código-fonte do compilador e, opcionalmente, um Dockerfile que permita executar o compilador em um contêiner. O projeto enviado também deve incluir um arquivo de documentação sucinto que diz claramente como compilar o compilador (se necessário) e como executar o compilador para algum arquivo de entrada. Também é interessante incluir pelo menos dois testes: um com um programa correto e um teste com um erro de sintaxe."*

**Checklist de entrega:**

| Item | Obrigatório? | Detalhes |
|---|---|---|
| Código-fonte do compilador | ✅ Sim | Em qualquer linguagem |
| Dockerfile | ⭐ Opcional | Pra rodar em container |
| Arquivo de documentação | ✅ Sim | **Sucinto** — como compilar e como executar |
| Teste 1: programa correto | ✅ Recomendado | Ex: `42.ci` contendo `42` |
| Teste 2: programa com erro | ✅ Recomendado | Ex: `erro.ci` contendo `4a2` |

---

## 6. Próximas Etapas (página 9)

> **Citação textual:**
> *"Nas próximas etapas, o compilador passará a traduzir uma linguagem de expressões aritméticas. O compilador vai gerar código que calcula o resultado da expressão e coloca esse resultado no registrador RAX. A partir daí, o modelo de código assembly visto neste projeto será usado sem alteração para imprimir o resultado."*

**Pontos centrais:**

- Próxima linguagem: **expressões aritméticas** (provavelmente `+`, `-`, `*`, `/`).
- Mecânica de saída continua a mesma: **resultado em RAX, modelo imprime**.
- O **template assembly desta atividade vai ser reusado SEM ALTERAÇÃO**.
- O esqueleto que você monta agora vai sobreviver.

**Observação pedagógica:**
Isso confirma o que eu disse antes: o que muda nas próximas atividades é o **miolo do compilador** (mais lógica pra calcular expressões). O **template assembly** (call imprime_num; call sair) **fica igual**. Faça código limpo agora, vai te economizar dor depois.

---

## Apêndice A — Referência rápida da especificação

| Item | Valor |
|---|---|
| **Linguagem fonte** | CI (Constantes Inteiras) |
| **Programa válido** | 1 ou mais dígitos decimais (ex: `42`, `0`, `1000`) |
| **Programa inválido** | Qualquer coisa que não case com a gramática (letras, sinais, ponto, espaços) |
| **Linguagem alvo** | Assembly x86-64 GAS (sintaxe AT&T) |
| **Sistema operacional alvo** | Linux |
| **Linguagem do compilador** | Livre (Rust, no nosso caso) |
| **Interface CLI** | `compci arquivo.ci` |
| **Entrada** | Arquivo `.ci` (caminho via argumento de linha de comando) |
| **Saída** | Arquivo `.s` (assembly) |
| **O que o compilador gera** | Template fixo + **1 linha** com a constante |
| **Compilador invoca `as`/`ld`?** | **Não** — usuário invoca manualmente |
| **Erro de sintaxe** | Reportar e **não gerar** o `.s` |
| **Erro de overflow** | **Opcional** |
| **Etapas conceituais** | Análise + Síntese |
| **Runtime (`runtime.s`)** | **Fornecido** pelo professor — não escreve |
| **Testes recomendados** | 1 caso correto + 1 caso de erro |

---

## Apêndice B — Gramática BNF isolada

```bnf
<programa>        ::= <literal-inteiro>
<literal-inteiro> ::= <digito>+
<digito>          ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

**Equivalente em regex:**

```regex
^[0-9]+$
```

---

## Apêndice C — Template assembly pronto pra copiar

**Versão com placeholder:**

```gas
#
# modelo de saida para o compilador
#

.section .text
.globl _start

_start:
    mov ${VALOR}, %rax

    call imprime_num
    call sair

.include "runtime.s"
```

**Versão preenchida com `42`:**

```gas
#
# modelo de saida para o compilador
#

.section .text
.globl _start

_start:
    mov $42, %rax

    call imprime_num
    call sair

.include "runtime.s"
```

**Comando pra montar e linkar:**

```bash
as --64 -o p1.o p1.s
ld -o p1 p1.o
./p1    # imprime 42
```

---

## Apêndice D — Checklist de entrega

Antes de enviar a atividade, verificar:

- [ ] **Compilador funcional** — `compci p1.ci` gera `p1.s` corretamente
- [ ] **CLI correta** — recebe nome do arquivo como argumento (não hardcoded, não stdin)
- [ ] **Saída fiel ao template** — todas as linhas do modelo presentes, na ordem certa
- [ ] **Linha do `mov`** corretamente substituída com o valor lido
- [ ] **Erro de sintaxe** detectado — entrada inválida reporta erro e NÃO gera `.s`
- [ ] **Documentação sucinta** — README com:
  - [ ] Como compilar o compilador
  - [ ] Como executar o compilador
  - [ ] Exemplo de entrada e saída esperada
- [ ] **Teste 1 (válido)** — arquivo `.ci` com constante correta, gera `.s` válido
- [ ] **Teste 2 (inválido)** — arquivo `.ci` com letra/erro, compilador reporta erro
- [ ] **Validação end-to-end** — `.s` gerado pode ser montado/linkado, executável imprime certo
- [ ] (opcional) **Dockerfile** funcional
- [ ] (opcional) **Verificação de overflow** implementada

---

## Apêndice E — Glossário de termos do professor

| Termo | Definição (segundo o PDF) |
|---|---|
| **Compilador** | Programa que gera um equivalente em assembly a partir do código-fonte |
| **Assembler** (montador) | Programa que monta o assembly em código objeto (`.o`) |
| **Linker** | Programa que liga arquivos objeto e produz o executável |
| **Análise** | Etapa do compilador que coleta informações da entrada e verifica erros |
| **Síntese** (ou geração) | Etapa do compilador que produz o código de saída |
| **Modelo** (template) | Arquivo assembly base onde apenas uma linha é substituída pelo compilador |
| **Runtime** (`runtime.s`) | Procedimentos prontos (`imprime_num`, `sair`) fornecidos com a atividade |
| **Erro de sintaxe** | Entrada que não casa com a gramática (em CI: contém algo além de dígitos) |

---

## Observações finais

**Pontos que podem cair em prova futura:**

1. Diferença entre **compilador**, **assembler** e **linker**.
2. Definição de **análise** vs **síntese** (conceitos centrais da disciplina).
3. Gramática BNF — saber ler `+`, `|`, `::=`, `<...>`.
4. Estrutura geral do pipeline de um compilador.
5. Por que CI é tão simples (motivação pedagógica).

**Próximas atividades antecipadas:**

Pelo Apêndice 6 do PDF, a próxima atividade vai tratar **expressões aritméticas**. Provável evolução:

```
Atividade 02: CI            (42)                   ← atual
Atividade 03: CIA           (2 + 3 * 4)           ← próxima
Atividade 04: + variáveis?
Atividade 05: + controle (if/while)?
Atividade 06: + funções?
```

A boa notícia: **o template do `_start:` com `call imprime_num; call sair` não muda**. A `linha de saída do compilador` vai ficar mais complexa (vai gerar várias instruções em vez de uma), mas o entorno é estável.

---

**Última atualização deste documento:** 2026-05-11 (durante leitura inicial do PDF).
