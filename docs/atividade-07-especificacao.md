# Atividade 07 — Expressões Constantes 2 (Precedência de Operadores)

> **Metadados do PDF original**
>
> * **Arquivo:** `CC - Atividade 07.pdf`
> * **Autor:** Andrei Formiga (professor)
> * **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Resumo da especificação oficial acompanhado de comentários sobre a implementação adotada pelo grupo. Citações da especificação aparecem destacadas; comentários e decisões de implementação são marcados como **Observação**.

---

# Sumário

1. Introdução
2. A linguagem EC2
3. Precedência e associatividade
4. Nova gramática
5. Implementação do analisador sintático
6. Interface com o restante do compilador
7. Artefato para entrega
8. Plano de implementação adotado

---

# 1. Introdução

> *"Até a atividade anterior construímos um compilador completo para a linguagem EC1. Nesta atividade, vamos modificar a linguagem para remover a obrigatoriedade dos parênteses em todas as operações, introduzindo precedência e associatividade dos operadores."*

A Atividade 07 marca a transição da linguagem **EC1** para **EC2**.

Até a Atividade 06, toda operação precisava estar obrigatoriamente entre parênteses.

Por exemplo:

```text
(7 + (5 * 3))
```

Agora, a linguagem passa a aceitar expressões escritas naturalmente:

```text
7 + 5 * 3
```

Para isso, o analisador sintático precisa respeitar automaticamente a precedência entre operadores.

---

# 2. A linguagem EC2

A principal diferença entre EC1 e EC2 é que os parênteses deixam de ser obrigatórios.

Exemplos válidos:

```text
42

7 + 5

7 + 5 * 3

100 - 2 * 10 + 20

3 + 4 * 2 / (1 - 5)

(7 + 5) * 3
```

Os operadores continuam sendo:

* soma (`+`)
* subtração (`-`)
* multiplicação (`*`)
* divisão (`/`)

Parênteses continuam existindo, porém agora apenas para alterar a ordem natural de avaliação.

---

# 3. Precedência e associatividade

Na EC2, o compilador deve obedecer às mesmas regras encontradas na maioria das linguagens de programação.

## Precedência

Os operadores de multiplicação e divisão possuem precedência maior que soma e subtração.

Exemplo:

```text
7 + 5 * 3
```

A expressão é interpretada como:

```text
7 + (5 * 3)
```

e não

```text
(7 + 5) * 3
```

---

## Associatividade

Operadores de mesma precedência são avaliados da esquerda para a direita.

Por exemplo:

```text
10 - 8 - 2
```

é interpretado como

```text
(10 - 8) - 2
```

e não

```text
10 - (8 - 2)
```

O mesmo vale para divisões:

```text
100 / 2 / 2
```

equivale a

```text
(100 / 2) / 2
```

---

# 4. Nova gramática

A gramática da EC2 passa a ser dividida em três níveis.

```bnf
exp_a ::= exp_m (('+' | '-') exp_m)*

exp_m ::= prim (('*' | '/') prim)*

prim ::= numero
       | '(' exp_a ')'
```

Cada produção representa um nível de precedência.

* `exp_a` reconhece operações de soma e subtração.
* `exp_m` reconhece multiplicação e divisão.
* `prim` reconhece constantes e expressões entre parênteses.

Essa separação elimina ambiguidades e garante automaticamente a ordem correta das operações.

---

# 5. Implementação do analisador sintático

O analisador sintático foi reorganizado para seguir diretamente a nova gramática.

Foram implementadas três funções principais:

```text
analisa_exp_a()
analisa_exp_m()
analisa_prim()
```

## analisa_exp_a()

Responsável por reconhecer operações de soma e subtração.

Inicialmente é analisada uma expressão multiplicativa.

Enquanto o próximo token for um operador `+` ou `-`, o parser continua construindo novos nós da árvore sintática.

Esse comportamento implementa naturalmente a associatividade à esquerda.

---

## analisa_exp_m()

Responsável por reconhecer multiplicações e divisões.

Seu funcionamento é idêntico ao de `analisa_exp_a()`, porém considerando apenas os operadores `*` e `/`.

Como `analisa_exp_a()` sempre chama `analisa_exp_m()`, multiplicações e divisões são processadas antes das operações aditivas, implementando corretamente a precedência.

---

## analisa_prim()

Reconhece os elementos básicos da linguagem.

Caso o próximo token seja um número, é criado um nó `Const`.

Caso seja um parêntese de abertura, uma nova expressão aditiva é analisada recursivamente até encontrar o parêntese de fechamento correspondente.

---

## Consulta do próximo token

Foi utilizada a função

```text
olhar_token()
```

para consultar o próximo token sem consumi-lo.

Essa função permite que o parser descubra se existe um operador de mesma precedência antes de decidir continuar a análise da expressão.

---

# 6. Interface com o restante do compilador

A mudança desta atividade ficou restrita ao analisador sintático.

Não foi necessário alterar:

* analisador léxico;
* estrutura da AST;
* geração de código Assembly.

A árvore sintática continua sendo composta pelos nós:

```text
Const
OpBin
```

Como consequência, o gerador de código desenvolvido na Atividade 06 continua funcionando sem modificações.

A única diferença é que agora a árvore construída pelo parser respeita automaticamente as regras de precedência e associatividade da linguagem EC2.

---

# 7. Artefato para entrega

O compilador deve:

* aceitar expressões sem parênteses obrigatórios;
* respeitar precedência entre operadores;
* respeitar associatividade à esquerda;
* continuar gerando assembly correto;
* incluir testes demonstrando o funcionamento da nova gramática;
* incluir documentação de utilização.

Durante o desenvolvimento foram adicionados testes cobrindo:

```text
7+5*3
10-8-2
100/2/2
10*5+20/4
100-2*10+20
3+4*2/(1-5)
```

Esses testes verificam corretamente precedência, associatividade e uso de parênteses.

---

# 8. Plano de implementação adotado

Estrutura do projeto:

```text
lexer.py
parser.py
arvore.py
compilador.py
runtime.s
testes.py
Makefile
tests/
```

Fluxo do compilador:

```text
arquivo.ec2
      |
      v
    lexer
      |
      v
    tokens
      |
      v
 parser EC2
      |
      v
     AST
      |
      v
 gerador de código
      |
      v
 assembly x86-64
```

A principal modificação desta atividade foi a reorganização do parser para utilizar três níveis de análise (`analisa_exp_a`, `analisa_exp_m` e `analisa_prim`), permitindo reconhecer expressões sem parênteses obrigatórios e respeitando automaticamente a precedência e a associatividade dos operadores.

---

**Última atualização:** 2026-07-05
