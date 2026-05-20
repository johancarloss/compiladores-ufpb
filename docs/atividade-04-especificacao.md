# Atividade 04 — Expressões Constantes 1 (Análise Léxica)

> **Metadados do PDF original**
> - **Arquivo:** `CC_-_Atividade_04.pdf`
> - **Autor:** Andrei Formiga (professor)
> - **Data:** 16 de maio de 2026
> - **Páginas:** 9
> - **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Transcrição fiel + comentários pedagógicos do PDF da atividade. Onde aparecer **citação textual**, marca como blockquote. Onde aparecer comentário/inferência, marca como **Observação:**.

---

## Sumário

1. [Introdução](#1-introdução-página-3)
2. [A linguagem EC1](#2-a-linguagem-ec1-expressões-constantes-1-página-4)
3. [Análise léxica e sintática](#3-análise-léxica-e-sintática-página-5)
4. [Análise léxica da linguagem EC1](#4-análise-léxica-da-linguagem-ec1-páginas-6-8)
5. [Artefato para entrega](#5-artefato-para-entrega-página-9)

E mais (acréscimos meus):

- [Apêndice A — Gramática isolada](#apêndice-a--gramática-isolada)
- [Apêndice B — Tabela completa de tokens](#apêndice-b--tabela-completa-de-tokens)
- [Apêndice C — Exemplos comentados](#apêndice-c--exemplos-comentados)
- [Apêndice D — Checklist de entrega](#apêndice-d--checklist-de-entrega)

---

## 1. Introdução (página 3)

> **Citação textual:**
> *"Na Atividade 02 criamos o primeiro compilador da disciplina, um compilador para a linguagem de Constantes Inteiras. Em seguida, na Atividade 03 vimos como traduzir (manualmente) expressões aritméticas contendo apenas constantes para a linguagem assembly x86-64. Agora nosso objetivo é criar um compilador que traduzirá expressões aritméticas com operandos constantes para assembly."*
>
> *"A linguagem EC1 (Expressões Constantes 1) é um pouco mais complicada que a linguagem de Constantes Inteiras, e isso significa que o compilador para EC1 vai precisar fazer análise dos programas para poder gerar o código assembly."*
>
> *"A análise da sintaxe dos programas é normalmente feita em duas etapas: a análise léxica agrupa caracteres isolados em unidades chamadas de tokens que são similares às palavras da língua portuguesa. Em seguida, a análise sintática usa os tokens produzidos pela análise léxica para obter a estrutura sintática do programa de entrada."*
>
> *"Nesta atividade, o objetivo é realizar a análise léxica da linguagem EC1. As próximas atividades continuarão o processo de análise, interpretação e compilação da linguagem EC1."*

**Pontos centrais:**

- A atividade introduz a primeira **fase real** de um compilador: análise léxica.
- A análise sintática completa será dividida em duas etapas:
  1. Léxica (agrupar caracteres em tokens)
  2. Sintática propriamente dita (estrutura gramatical a partir dos tokens)
- Esta atividade implementa **apenas a primeira etapa** (léxica). Sintática vem nas próximas.

**Observação pedagógica:**
Esse é o primeiro projeto da disciplina que cria um artefato reutilizável de compilador real. O lexer que você implementar aqui vai ser **base das próximas atividades** (parser, semântica, codegen). Estrutura limpa agora compensa muito depois.

---

## 2. A linguagem EC1 (Expressões Constantes 1) (página 4)

> **Citação textual:**
> *"Um programa na linguagem EC1 é uma expressão aritmética com operandos constantes e usando as quatro operações. Todas as operações devem ser escritas entre parênteses, então não precisamos nos preocupar com precedência de operadores."*

**Exemplos do PDF (um programa por linha):**

```
333
(6 * 7)
(3 + (4 + (11 + 7)))
(33 + (912 * 11))
((427 / 7) + (11 * (231 + 5)))
```

### Gramática formal (BNF)

```bnf
<programa>   ::= <expressao>
<expressao>  ::= <literal> | '(' <expressao> <operador> <expressao> ')'
<operador>   ::= '+' | '-' | '*' | '/'
<literal>    ::= <digito>+
<digito>     ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
```

**Lendo a gramática:**

- Um `<programa>` é uma `<expressao>`
- Uma `<expressao>` é OU um `<literal>` OU uma expressão entre parênteses com operador no meio
- Um `<operador>` é um dos 4 símbolos: `+`, `-`, `*`, `/`
- Um `<literal>` é uma sequência de 1 ou mais dígitos
- Um `<digito>` é qualquer um dos 10 dígitos decimais

**Observação pedagógica:**
A obrigatoriedade dos parênteses **elimina precedência de operadores**. Isso é uma escolha didática proposital. Em linguagens reais (C, Python), `2 + 3 * 4` é `14` porque `*` tem precedência sobre `+`. Em EC1 isso seria erro de sintaxe — você precisaria escrever `(2 + (3 * 4))`. Tira ambiguidade.

---

## 3. Análise léxica e sintática (página 5)

> **Citação textual:**
> *"O processo de analisar a estrutura de um programa de entrada para ajudar a determinar seu significado (o que o programa faz) é normalmente chamado de análise sintática."*
>
> *"A análise sintática para linguagens computacionais é tradicionalmente dividida em duas etapas:"*
>
> 1. *"a análise léxica, que consiste em agrupar os caracteres individuais em tokens (similares às palavras da linguagem natural) e classificar esses tokens em categorias sintáticas"*
> 2. *"a análise sintática propriamente dita, que verifica a estrutura gramatical da entrada com base na sequência de tokens da análise léxica"*

**Analogia do professor (parafraseada):**
Texto sem separação de palavras é praticamente ilegível:

> *"OfundadordaminhafamíliafoiumcertoDamiãoCubas,quefloresceunaprimeirametadedoséculoXVIII..."*

A análise léxica é o que **separa "palavras"** (tokens) do código antes da análise sintática tentar entender a estrutura. Sem isso, o parser teria que cuidar de cada caractere individual ao mesmo tempo que verifica estrutura — fica muito complicado.

> **Citação textual:**
> *"A base teórica para a análise léxica e análise sintática são as linguagens formais. Usamos as linguagens regulares na análise léxica, e as linguagens livres de contexto na análise sintática."*

**Conexão teórica:**

| Etapa | Tipo de linguagem | Ferramenta de reconhecimento |
|---|---|---|
| Análise léxica | Linguagens regulares | Autômato finito (DFA/NFA) ou regex |
| Análise sintática | Linguagens livres de contexto | Autômato de pilha ou parser recursivo |

---

## 4. Análise léxica da linguagem EC1 (páginas 6-8)

### 4.1. Estrutura de dados do token (página 6)

> **Citação textual:**
> *"As duas informações essenciais para guardar para cada token são o lexema que gerou o token, e a classe ou tipo do token. O lexema é a string da entrada que gerou o token. Por exemplo, a sequência de caracteres `1234` deve gerar um token do tipo número e com lexema `1234`."*

**Estrutura mínima de um token:**

| Campo | Descrição | Exemplo |
|---|---|---|
| `tipo` | Classe léxica | `Numero`, `ParenEsq`, `Soma`, ... |
| `lexema` | String original | `"1234"`, `"("`, `"+"`, ... |
| `posicao` | Onde apareceu no arquivo | `7` (offset em caracteres) |

> **Citação textual:**
> *"Como vimos, a linguagem EC1 tem três tipos de token: números, pontuação e operadores. Para facilitar o uso dos tokens nas etapas posteriores do compilador, podemos criar um tipo separado para cada pontuação e cada operador; assim, ao invés de apenas um tipo pontuação, podemos ter um tipo para 'parêntese esquerdo' e outro para 'parêntese direito'. Da mesma forma, podemos separar os operadores em quatro tipos. Alguns analisadores léxicos também incluem um tipo separado de token para sinalizar o final da entrada, muitas vezes chamado de um token EOF, da siga em inglês End Of File."*

**Tipos sugeridos para EC1:**

| Categoria do PDF | Tipos detalhados sugeridos |
|---|---|
| Número | `Numero` |
| Pontuação | `ParenEsq`, `ParenDir` |
| Operadores | `Soma`, `Sub`, `Mult`, `Div` |
| (opcional) Fim | `EOF` |

> **Citação textual:**
> *"Além do lexema e do tipo do token, é comum guardar em cada um a posição em que ele ocorreu no arquivo de entrada. Isso é muito importante para o tratamento de erros no compilador; quando ocorre um erro no arquivo fonte, é necessário mostrar para o usuário qual o local do arquivo em que o erro foi encontrado."*

**Sobre posição:** o mínimo é o **offset** (índice na string de entrada). Pode estender para linha/coluna se quiser mensagens de erro mais amigáveis. Conversão offset → linha/coluna é fácil quando precisar.

### 4.2. Espaços (página 6-7)

> **Citação textual:**
> *"Uma função importante do analisador léxico (na maioria das linguagens) é eliminar os caracteres que contam como espaço em branco, principalmente:"*
>
> 1. *"espaço (código 32 em ASCII)"*
> 2. *"tabulação (código 9)"*
> 3. *"nova linha (código 10)"*
> 4. *"retorno do carro (código 13)"*

**Whitespace a ignorar em EC1:**

| Caractere | Código ASCII | Como aparece em C |
|---|---|---|
| Espaço | 32 | `' '` |
| Tabulação | 9 | `'\t'` |
| Nova linha | 10 | `'\n'` |
| Retorno do carro | 13 | `'\r'` |

> **Citação textual:**
> *"Na maioria das linguagens, esses espaços entre tokens completos não têm nenhuma influência no significado do programa, então podem ser eliminados sem problema."*

Em EC1, espaços só **separam tokens** — não têm semântica.

### 4.3. Exemplo de análise léxica (página 7)

> **Citação textual:**
>
> *"Para o seguinte programa EC1:"*
>
> ```
> (33 + (912 * 11))
> ```
>
> *"A saída do analisador léxico é a seguinte sequência de tokens, com cada token seguindo o formato `<tipo, lexema, posicao>`:"*
>
> ```
> <ParenEsq, "(", 0>
> <Numero, "33", 1>
> <Soma, "+", 4>
> <ParenEsq, "(", 6>
> <Numero, "912", 7>
> <Mult, "*", 11>
> <Numero, "11", 13>
> <ParenDir, ")", 15>
> <ParenDir, ")", 16>
> ```

**Observação:** este é o formato **canônico de saída** que o professor espera. Nosso programa deve imprimir exatamente nesse formato (`<tipo, "lexema", posicao>` com vírgulas separando, aspas no lexema).

### 4.4. Erros léxicos (página 7)

> **Citação textual:**
> *"O analisador léxico deve gerar a sequência de tokens correspondente ao programa de entrada. O programa de entrada do compilador é fornecido pelo usuário, e esse usuário pode cometer erros. Se o programa de entrada incluir caracteres ou sequências de caracteres que não podem ser reconhecidas como um token da linguagem, isso é um erro léxico."*
>
> *"O analisador léxico pode parar o processo de análise léxica e informar o erro léxico assim que encontrar o primeiro erro léxico, ou pode tratar um erro léxico como um tipo de token específico e tentar continuar a análise. A segunda opção é útil pois pode reportar vários erros ao usuário de uma vez, mas pode ser um pouco mais difícil de implementar."*
>
> *"A posição guardada pelo analisador deve ser usada para reportar o erro, gerando mensagens como `Erro léxico na posição X`."*
>
> *"No caso da linguagem EC1, qualquer caractere fora do conjunto de parênteses, operadores e dígitos vai ser um erro léxico."*

**Decisão livre do grupo:**

| Estratégia | Vantagem | Desvantagem |
|---|---|---|
| Parar no 1º erro | Simples | Usuário só vê um erro por vez |
| Continuar com `Erro` token | Reporta múltiplos erros | Mais complexo |

Pra essa atividade vamos com **parar no 1º erro** (recomendação da nossa discussão).

**Mensagem de erro padrão sugerida:**

```
Erro léxico na posição X: caractere inválido 'Y'
```

### 4.5. Comentários (página 8)

> **Citação textual:**
> *"Uma outra função comum do analisador léxico é remover os comentários da entrada, já que normalmente os comentários não influenciam na semântica do programa (ou seja, o que o programa faz)."*
>
> *"Na linguagem EC1 não temos uma definição de sintaxe para comentários, mas os grupos podem adicionar suporte a comentários (e decidir a sintaxe deles) de forma opcional. Poder escrever comentários será muito útil nas linguagens mais complexas que veremos em atividades futuras."*

**Decisão:** **NÃO implementar** comentários nesta atividade (PDF marca como opcional, foca no básico primeiro).

### 4.6. Uso do analisador léxico (página 8)

> **Citação textual:**
> *"A forma de usar o analisador léxico é geralmente por uma das seguintes funções:"*
>
> 1. *"Uma função para obter o próximo token (por exemplo `proximo_token`) que, quando chamada, retorna o próximo token da entrada; quando não houver mais tokens na entrada, essa função sinaliza o final da entrada por algum erro, exceção, ou retornando um token do tipo EOF"*
> 2. *"Uma função para obter todos os tokens da entrada de uma vez em uma lista ou vetor. Neste caso não é preciso ter um token específico para o final da entrada, já que todos os tokens são colocados em uma lista."*
>
> *"Em compiladores usados em produção, a entrada pode ser muito grande e ter todos os tokens na memória ao mesmo tempo pode criar um problema de desempenho no compilador. Como normalmente a análise sintática pode prosseguir apenas olhando o próximo token, uma função como `proximo_token` é suficiente."*
>
> *"Nos compiladores que faremos nessa disciplina isso não será um problema, portanto qualquer uma das duas interfaces vai funcionar."*

**Decisão:** vamos com **opção 2 (lista de tokens)** — mais simples pra essa atividade.

---

## 5. Artefato para entrega (página 9)

> **Citação textual:**
> *"Cada grupo deve entregar um analisador léxico completo para a linguagem EC1 que recebe um arquivo de entrada (como um argumento na linha de comando) e imprime a sequência de tokens correspondente a esse arquivo de entrada. Além disso, o projeto deve incluir um conjunto de testes que verifique que o analisador funciona corretamente para expressões com diferentes tipos de espaços em branco, e que o analisador detecta e reporta os erros léxicos."*
>
> *"É possível usar a impressão da sequência de tokens como parte dos testes, por exemplo usando uma ferramenta como cram: https://bitheap.org/cram/"*
>
> *"O projeto deve incluir uma documentação sucinta que explica como executar os testes incluídos no projeto, e como executar o analisador léxico para qualquer arquivo de entrada arbitrário."*

**Checklist:**

- [ ] Analisador léxico completo da EC1
- [ ] CLI: recebe arquivo como argumento, imprime tokens
- [ ] Testes com diferentes tipos de whitespace
- [ ] Testes que detectam e reportam erros léxicos
- [ ] Documentação sucinta de como rodar testes
- [ ] Documentação sucinta de como rodar o analisador
- [ ] (sugerido pelo prof, opcional) usar `cram`

---

## Apêndice A — Gramática isolada

```bnf
<programa>   ::= <expressao>
<expressao>  ::= <literal>
              | '(' <expressao> <operador> <expressao> ')'
<operador>   ::= '+' | '-' | '*' | '/'
<literal>    ::= <digito>+
<digito>     ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
```

**Conjunto de caracteres válidos** (qualquer outro é erro léxico):

```
( ) + - * / 0 1 2 3 4 5 6 7 8 9
+ whitespace: espaço, tab, \n, \r
```

---

## Apêndice B — Tabela completa de tokens

| Tipo | Lexema literal | Exemplo de aparição |
|---|---|---|
| `ParenEsq` | `(` | `(33 + 5)` |
| `ParenDir` | `)` | `(33 + 5)` |
| `Soma` | `+` | `(2 + 3)` |
| `Sub` | `-` | `(10 - 4)` |
| `Mult` | `*` | `(6 * 7)` |
| `Div` | `/` | `(20 / 5)` |
| `Numero` | sequência de dígitos | `42`, `912`, `0`, `1234` |

**Whitespace** (ignorado, não vira token):

- Espaço `' '` (ASCII 32)
- Tabulação `'\t'` (ASCII 9)
- Nova linha `'\n'` (ASCII 10)
- Retorno do carro `'\r'` (ASCII 13)

**Qualquer outro caractere** vira erro léxico.

---

## Apêndice C — Exemplos comentados

### Exemplo 1 — `333`

Programa de um único literal.

```
<Numero, "333", 0>
```

### Exemplo 2 — `(6 * 7)`

```
<ParenEsq, "(", 0>
<Numero, "6", 1>
<Mult, "*", 3>
<Numero, "7", 5>
<ParenDir, ")", 6>
```

### Exemplo 3 — `(33 + (912 * 11))` (exemplo do PDF)

```
<ParenEsq, "(", 0>
<Numero, "33", 1>
<Soma, "+", 4>
<ParenEsq, "(", 6>
<Numero, "912", 7>
<Mult, "*", 11>
<Numero, "11", 13>
<ParenDir, ")", 15>
<ParenDir, ")", 16>
```

### Exemplo 4 — Whitespace extra (`  (  33  +  5 )  `)

A saída é a **mesma estrutura de tokens**, só as posições mudam (porque o offset acompanha o whitespace ignorado):

```
<ParenEsq, "(", 2>
<Numero, "33", 5>
<Soma, "+", 9>
<Numero, "5", 12>
<ParenDir, ")", 14>
```

### Exemplo 5 — Erro léxico (`2 # 3`)

```
<Numero, "2", 0>
Erro léxico na posição 2: caractere inválido '#'
```

(O `#` não está no alfabeto da linguagem.)

---

## Apêndice D — Checklist de entrega

### Funcional

- [ ] Programa lê arquivo via argumento de CLI
- [ ] Imprime tokens no formato `<tipo, "lexema", posicao>`
- [ ] Reconhece todos os 7 tipos: `Numero`, `ParenEsq`, `ParenDir`, `Soma`, `Sub`, `Mult`, `Div`
- [ ] Ignora whitespace (espaço, tab, `\n`, `\r`)
- [ ] Detecta erro léxico e reporta com posição
- [ ] Não gera saída de sucesso quando há erro

### Testes

- [ ] Teste com expressão simples sem espaços extras
- [ ] Teste com expressão multilinha (`\n` no meio)
- [ ] Teste com espaços/tabs em volta dos tokens
- [ ] Teste com caractere inválido (deve falhar com erro léxico)
- [ ] Teste com número grande (vários dígitos)
- [ ] Teste de aninhamento profundo

### Documentação

- [ ] README com como compilar o lexer
- [ ] README com como rodar o lexer pra um arquivo qualquer
- [ ] README com como rodar a suíte de testes

---

**Última atualização:** 2026-05-20 (durante leitura inicial do PDF).
