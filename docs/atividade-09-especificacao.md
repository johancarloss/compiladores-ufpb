# Atividade 09 — Comandos (linguagem Cmd)

> **Autor do PDF:** Andrei Formiga — 08/07/2026 — 15 páginas
> **Base:** constrói sobre a linguagem EV (atv08). Adiciona `if`, `while` e comparações.
> Transcrição fiel + comentários. Citação textual em blockquote; comentário meu em **Observação:**.

---

## 1. Introdução

> *"Os compiladores que fizemos até agora traduzem linguagens de cálculos com inteiros. Essas linguagens não são propriamente linguagens de programação, pois não possuem capacidade de tomar decisões ou repetição."*
>
> *"Dizemos que uma linguagem que possui os elementos necessários para expressar qualquer algoritmo é uma linguagem **Turing-completa**. Nesta atividade vamos adicionar comandos à linguagem, incluindo um comando condicional e um comando de repetição (loop). Com isso, faremos um compilador para nossa primeira linguagem Turing-completa."*

**Observação:** este é o marco conceitual. Com `if` e `while`, a linguagem passa a poder computar qualquer algoritmo. O nome da nova linguagem é **Cmd** (de comandos).

---

## 2. A Linguagem Cmd

> *"Um programa na linguagem Cmd é composto por zero ou mais declarações (de forma igual às declarações na linguagem EV), seguidas de um corpo contendo zero ou mais comandos e uma expressão de resultado. O corpo é delimitado com chaves e a expressão com o resultado usa a palavra-chave `return`."*

Menor programa (só o corpo com o resultado):
```
{
  return 7 * 6;
}
```

**Comandos possíveis:**
- comando condicional (`if`)
- comando de repetição (`while`)
- comando de atribuição (`x = exp;`) — só altera variável **já declarada** (atribuição NÃO cria variável nova)

**Expressões de controle:**
> *"a linguagem adiciona os operadores `<` (menor que), `>` (maior que) e `==` (igualdade). Os operadores de comparação têm precedência mais baixa que os aritméticos. A linguagem não adiciona um tipo booleano separado; um valor igual a zero é considerado falso, e qualquer valor diferente de zero é considerado verdadeiro."*

**Exemplo — valor absoluto do discriminante (delta):**
```
a = 1;
b = 2;
c = 3;
delta = b * b - 4 * a * c;
{
  if delta < 0 {
    delta = 0 - delta;
  } else {
    delta = delta;
  }
  return delta;
}
```

> *"Note que `return` não é um comando, e portanto não pode ser usado dentro do comando condicional (ou de uma repetição). O comando condicional na linguagem Cmd obrigatoriamente inclui o braço `else`..."*

**Exemplo — soma dos inteiros entre n e m-1 (loop):**
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

> *"O comando de atribuição tem a mesma sintaxe da declaração de uma variável, mas declarações só podem acontecer antes do corpo de comandos, e a atribuição só pode aparecer em lugares que aceitam comandos. A atribuição não pode ser usada para criar novas variáveis, então qualquer variável que será necessária no programa deve ser declarada no começo."*

### 2.1. Gramática

```bnf
<programa> ::= <decl>* '{' <cmd>* 'return' <exp> ';' '}'
<decl>     ::= <var> '=' <exp> ';'
<var>      ::= <letra><letra_digito>*
<cmd>      ::= <if> | <while> | <atrib>
<if>       ::= 'if' <exp> '{' <cmd>* '}' 'else' '{' <cmd>* '}'
<while>    ::= 'while' <exp> '{' <cmd>* '}'
<atrib>    ::= <var> '=' <exp> ';'
<exp>      ::= <exp_a> (('<' | '>' | '==')* <exp_a>)*
<exp_a>    ::= <exp_m> (('+' | '-') <exp_m>)*
<exp_m>    ::= <prim> (('*' | '/') <prim>)*
<prim>     ::= <num> | <var> | '(' <exp> ')'
<num>      ::= <digito><digito>*
```

> *"Note que as chaves nos corpos do `if` e `while` não são opcionais."*
>
> *"Mais uma vez, será necessário fazer alterações em todo o compilador para implementar a nova linguagem."*

**Observação:** a mudança-chave na gramática de expressões é o novo nível `<exp>`, que fica **acima** de `<exp_a>` (aditiva). Ou seja, comparação tem a precedência mais baixa de todas.

---

## 3. Análise léxica

> *"A linguagem Cmd inclui alguns novos tipos de tokens: dois caracteres de pontuação `{` `}`; os operadores `<` `>` e `==`; e as palavras-chave `if`, `else`, `while` e `return`."*

**Pegadinha do `==`:**
> *"O token para teste de igualdade `==` significa que o analisador léxico tem que diferenciar entre este operador e o sinal de igual único usado nas declarações e atribuições. Geralmente isso é resolvido com o analisador léxico olhando o caractere que aparece logo após o primeiro `=`; se o caractere seguinte for outro sinal de igual, o token é o operador de igualdade; caso contrário, o token é o sinal usado nas declarações e atribuições."*

**Palavras-chave:**
> *"As palavras-chave também são um caso interessante, pois elas seguem as regras usadas para identificadores. Uma solução comum é reconhecer identificadores normalmente mas testar, antes de gerar o token, se o lexema identificado é igual a uma das palavras-chave; se for, o token gerado é do tipo palavra-chave, caso contrário é um identificador."*

---

## 4. Análise sintática

> *"A análise do programa começa de forma similar à linguagem EV: reconhecendo zero ou mais declarações. Sempre que o próximo token for um identificador, temos uma declaração. A lista de declarações é terminada por um token `{`."*
>
> *"Dentro do bloco, é preciso reconhecer zero ou mais comandos; um comando inicia com a palavra-chave `if`, a palavra-chave `while`, ou um identificador (no caso da atribuição). A lista de comandos é terminada pela palavra-chave `return`."*
>
> *"A análise das expressões adiciona mais um nível de precedência para as operações de comparação, e é um nível de precedência mais baixo que o das operações de soma e subtração. Isso vai criar a necessidade de mais uma função de análise para esse nível, mas ela vai seguir o mesmo formato das funções de análise usadas para expressões aditivas e multiplicativas."*

**Observação:** o parser da atv08 já tem `analisa_exp_a` (aditiva) e `analisa_exp_m` (multiplicativa). A atv09 adiciona uma `analisa_exp` (comparação) acima delas, no mesmo padrão. E adiciona funções pra comandos.

---

## 5. Análise Semântica

> *"A presença de comandos de atribuição na linguagem cria a necessidade de mais uma verificação na análise semântica: pelas regras da linguagem Cmd, é um erro tentar atribuir um novo valor a uma variável que não foi declarada."*
>
> *"...um comando de atribuição tem dois componentes: a expressão com o novo valor (lado direito), e a variável que vai receber o valor (lado esquerdo). A expressão do lado direito não pode referenciar nenhuma variável que não foi declarada, e o lado esquerdo também deve ser uma variável já declarada. Qualquer variável não declarada no lado direito ou esquerdo deve gerar um erro."*
>
> *"Entretanto, como a atribuição não cria variáveis novas, nada precisa ser incluído na tabela de símbolos ao processar um comando de atribuição."*

---

## 6. Geração de código

> *"A maior diferença na geração de código para a linguagem Cmd são os operadores de comparação, e os comandos condicional e de repetição. A atribuição pode gerar código igual a uma declaração de variável, se as verificações da análise semântica forem bem-sucedidas."*

### 6.1. Condições e sinalizadores (flags)

> *"As condições derivadas de comparações numéricas são implementadas com o uso dos sinalizadores (flags) do processador."* (registrador RFLAGS)

Flags relevantes:
- **Z** (zero): ativado quando o resultado da operação é zero.
- **S** (sinal): ativado quando o resultado é negativo.
- **O** (overflow): ativado quando houve overflow.

> *"Para saber se dois números A e B são iguais, podemos subtrair um do outro (A − B) e verificar os flags. Se Z está ativado, os dois números eram iguais; se S e O têm mesmo valor, A é maior que B; se S e O tem valores diferentes, A é menor que B..."*

**Instrução CMP:**
> *"Usaremos a instrução CMP (compare) que faz a subtração mas não armazena o resultado em nenhum lugar, apenas altera os flags."*

**Instruções SET:**
> *"Vamos utilizar as instruções SETZ (Set if Zero), SETG (Set if Greater) e SETL (Set if Less) para implementar os operadores de comparação. Essas instruções colocam o valor 0 ou 1 em um operando de 8 bits dependendo da condição."*

**Modelo para `A == B`:**
```
<codigo_B>
push %rax
<codigo_A>
pop %rbx
xor %rcx, %rcx
cmp %rbx, %rax
setz %cl
mov %rcx, %rax
```

> *"Como SETZ só aceita um operando de 8-bits, não podemos usar RAX diretamente, então usamos RCX como temporário... O código zera RCX usando XOR, depois faz a comparação com CMP (o operando esquerdo está em RBX e o direito em RAX) e logo em seguida SETZ determina o valor de CL (o sub-registrador de 8 bits de RCX). Nesse ponto, RCX terá valor 1 se os números são iguais, e 0 caso contrário. Para finalizar, o código transfere o valor de RCX para RAX..."*
>
> *"A tradução dos operadores `<` e `>` segue o mesmo modelo, mas trocando SETZ por SETL para `<` e SETG para `>`."*

**Observação:** ordem no `cmp %rbx, %rax` → compara RAX (esquerdo, A) com RBX (direito, B). O `setl` marca se A < B, `setg` se A > B. A ordem de empilhar segue o mesmo esquema da atv06 (direito primeiro).

### 6.2. Saltos e rótulos

> *"Para mudar a execução para continuar com outra instrução que não seja a próxima na ordem, a linguagem de máquina utiliza instruções de salto (jump). Uma instrução de salto sempre recebe o endereço da próxima instrução a executar."*

- **Salto incondicional** `jmp` — sempre pula.
- **Salto condicional** `jz` (Jump if Zero) — pula se o flag Z estiver ativado.

**Rótulos (labels):** nome dado ao endereço de uma instrução, seguido de `:`.

**Exemplo de loop infinito (só ilustrativo):**
```
    mov $1, %rax
    mov $2, %rbx
loop:
    mul %rbx
    jmp loop
```

**Modelo do `if E { C1 } else { C2 }`:**
```
<codigo_E>
cmp $0, %rax
jz Lfalso0
<codigo_C1>
jmp Lfim0
Lfalso0:
<codigo_C2>
Lfim0:
```

> *"...`cmp $0, %rax` testa se o valor de RAX é zero (falso) ou diferente de zero (verdadeiro). Se RAX era zero, o flag Z estará ativado... o código usa JZ para saltar para o rótulo Lfalso0 caso a condição seja falsa. Se a condição era verdadeira... JZ não toma o salto e vai executar `<codigo_C1>`. Ao final da execução de C1, o código precisa saltar para Lfim0 para não executar C2..."*

**Modelo do `while E { C }`:**
```
Linicio0:
<codigo_E>
cmp $0, %rax
jz Lfim0
<codigo_C>
jmp Linicio0
Lfim0:
```

> *"O `<codigo_E>` calcula o resultado da expressão e coloca em RAX; esse resultado é testado e, se a condição for falsa, o código sai do loop saltando para Lfim0. Caso contrário, o código do corpo do laço é executado e depois volta novamente para Linicio0."*

**Rótulos únicos (crucial):**
> *"Naturalmente, cada `if` e `while` gerado deve gerar nomes diferentes para os rótulos. Uma forma de fazer isso é manter um contador de quantos rótulos foram gerados até agora, e sempre concatenar o valor do contador no final do nome do rótulo, gerando por exemplo os rótulos Lfalso0, Lfim1, Linicio2, etc."*

**Observação:** o contador de rótulos é o detalhe que mais gera bug se esquecido — dois `if` gerariam `Lfalso0` iguais e o assembler reclamaria de rótulo duplicado. Manter um contador incremental resolve.

---

## 7. Variações (opcionais, o grupo pode fazer)

- Novos operadores de comparação `<=` e `>=`.
- Operadores booleanos `AND`, `OR`, `NOT` (novo nível de precedência).
- Comando especial para ler número da entrada e atribuir a variável.
- `if` sem `else` (cria ambiguidade na gramática, mas resolvível).
- Remover a limitação da atribuição só a variáveis declaradas (aí a atribuição pode criar variável nova, inserindo símbolo no `.bss`).

---

## 8. Artefato para entrega

> *"Cada grupo deve entregar o compilador para a linguagem Cmd ou alguma variante da linguagem. No caso da linguagem implementada pelo compilador ser diferente... a documentação do projeto deve deixar claras as diferenças em relação ao que está no guia."*
>
> *"O projeto deve incluir programas de teste que incluam comandos condicionais, comandos de repetição e atribuição. A documentação deve descrever, de forma clara e sucinta, como executar o compilador e os testes incluídos."*

**Checklist:**
- [ ] Compilador Cmd completo (léxica → sintática → semântica → geração)
- [ ] `if`, `while`, atribuição, comparações funcionando
- [ ] Testes com condicional, repetição e atribuição
- [ ] Documentação de como executar

---

## 9. Outros exemplos

**Resto da divisão de m por n (subtração sucessiva):**
```
m = 10;
n = 4;
{
  while m + 1 > n {
    m = m - n;
  }
  return m;
}
```
(m=10, n=4 → resultado 2)

**MDC de a e b:**
```
a = 18;
b = 12;
r = 0;
{
  r = a;
  while r+1 > b {
    r = r - b;
  }
  while r > 0 {
    a = b;
    b = r;
    r = a;
    while r+1 > b {
      r = r - b;
    }
  }
  return b;
}
```
(a=18, b=12 → mdc 6)

**Última atualização:** 2026-07-15 (leitura inicial do PDF).
