# Atividade 08 — Expressões com Variáveis

> **Metadados do PDF original**
>
> * **Arquivo:** `CC_-_Atividade_08.pdf`
> * **Título:** Atividade 08 - Expressões com Variáveis
> * **Autor:** Andrei Formiga (professor)
> * **Data do documento:** 30 de junho de 2026
> * **Data de criação do PDF:** 7 de julho de 2026
> * **Páginas:** 13
> * **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Sobre este documento:**
> Resumo da especificação oficial acompanhado de comentários sobre os pontos de implementação esperados. A atividade estende a linguagem EC2 para uma nova linguagem, chamada **EV**, com declarações e uso de variáveis.

---

# Sumário

1. Introdução
2. A linguagem EV
3. Alterações léxicas
4. Alterações sintáticas
5. Análise semântica
6. Tabela de símbolos
7. Geração de código
8. Variações sintáticas
9. Artefato para entrega
10. Plano de implementação sugerido

---

# 1. Introdução

A Atividade 08 parte do compilador completo de expressões constantes desenvolvido nas atividades anteriores e adiciona suporte a **variáveis**.

Com isso, o compilador deixa de processar apenas uma expressão aritmética isolada e passa a aceitar programas formados por:

* zero ou mais declarações de variáveis;
* uma expressão final obrigatória;
* uso de variáveis previamente declaradas dentro de expressões.

Essa mudança afeta todos os principais estágios do compilador:

* análise léxica;
* análise sintática;
* análise semântica;
* geração de código.

A grande novidade conceitual é a introdução de uma etapa entre a análise sintática e a geração de código: a **análise semântica**, também chamada de análise contextual.

Fluxo atualizado do compilador:

```text
código-fonte
      |
      v
 análise léxica
      |
      v
    tokens
      |
      v
 análise sintática
      |
      v
     AST
      |
      v
 análise semântica
      |
      v
     AST
      |
      v
 geração de código
      |
      v
código assembly
```

---

# 2. A linguagem EV

A nova linguagem se chama **EV**: Expressões com Variáveis.

Um programa EV é composto por uma sequência de declarações, seguida por uma expressão final cujo valor será o resultado do programa.

Exemplo:

```ev
l = 30;
c = 40;
= l + l + c + c
```

Esse programa calcula o perímetro de um retângulo com largura `30` e comprimento `40`.

## Gramática

```bnf
<programa> ::= <decl>* <result>

<decl> ::= <ident> '=' <exp> ';'

<ident> ::= <letra><letra_digito>*

<result> ::= '=' <exp>

<exp> ::= <exp_m> (('+' | '-') <exp_m>)*

<exp_m> ::= <prim> (('*' | '/') <prim>)*

<prim> ::= <num>
         | <ident>
         | '(' <exp> ')'

<num> ::= <digito><digito>*
```

Onde:

* `<letra>` representa uma letra maiúscula ou minúscula;
* `<digito>` representa um dígito de `0` a `9`;
* `<letra_digito>` representa uma letra ou um dígito.

## Declarações

Cada declaração começa com um identificador, seguido por `=`, uma expressão e `;`.

Exemplo:

```ev
x = (7 + 4) * 12;
```

O valor da expressão do lado direito deve ser calculado e atribuído à variável do lado esquerdo.

## Expressão final

A expressão final começa com `=` e não termina com ponto-e-vírgula.

Exemplo completo:

```ev
x = (7 + 4) * 12;
y = x * 3 + 11;
= (x * y) + (x * 11) + (y * 13)
```

Nesse programa:

* `x` é declarado primeiro;
* `y` pode usar `x`, pois `x` já foi declarado;
* a expressão final pode usar `x` e `y`;
* o resultado esperado é `60467`.

---

# 3. Alterações léxicas

A linguagem EV adiciona três elementos ao analisador léxico:

* ponto-e-vírgula (`;`);
* sinal de igual (`=`);
* identificadores.

Um identificador é uma sequência que:

* começa com uma letra maiúscula ou minúscula;
* pode continuar com zero ou mais letras ou dígitos;
* termina quando aparece um caractere que não é letra nem dígito.

Exemplos válidos:

```text
x
y
largura
altura2
abc123
```

Exemplos inválidos:

```text
237axy
9valor
```

Sequências que começam com dígito e depois contêm letras continuam sendo erro léxico.

---

# 4. Alterações sintáticas

A parte de expressões reaproveita a linguagem EC2, que já possui precedência e associatividade para operadores aritméticos.

A principal diferença é que agora uma expressão primária também pode ser uma variável:

```bnf
<prim> ::= <num>
         | <ident>
         | '(' <exp> ')'
```

O parser deve iniciar pelo não-terminal `<programa>`, e não mais diretamente por uma expressão.

Um programa é reconhecido assim:

1. Enquanto o próximo token for um identificador, reconhecer uma declaração.
2. Ao encontrar `=`, reconhecer a expressão final.
3. Construir um nó raiz `Programa`.

Pseudo-código da análise de programa:

```text
programa():
    tok = olhar_proximo_token()
    declaracoes = []

    while tok.tipo == Identificador:
        dec = decl()
        declaracoes.adicionar(dec)
        tok = olhar_proximo_token()

    if tok != '=':
        erro

    exp_final = result()
    return Programa(declaracoes, exp_final)
```

## Nó de programa

O nó `Programa` deve armazenar:

* a lista de declarações;
* a expressão final.

## Nó de declaração

Cada declaração deve armazenar:

* o nome da variável;
* a expressão que calcula seu valor.

## Nó de variável

Além de constantes e operações binárias, a AST passa a precisar de um nó para representar referências a variáveis.

Uma estrutura possível:

```text
Programa(declaracoes, resultado)
Decl(nome, exp)
Var(nome)
Const(valor)
OpBin(op, esq, dir)
```

---

# 5. Análise semântica

Com variáveis, surgem programas que são sintaticamente corretos, mas semanticamente inválidos.

Exemplo:

```ev
x = 7 + y;
y = x * 11;
= x * y + z
```

Esse programa tem dois problemas:

* `y` é usado na declaração de `x` antes de ter sido declarado;
* `z` é usado na expressão final sem ter sido declarado.

Esses erros não são detectáveis apenas pela gramática, porque a sintaxe não diferencia uma variável declarada de uma variável não declarada.

Por isso, o compilador deve incluir uma etapa de análise semântica após construir a AST.

## Regra principal

Uma variável só pode ser usada depois de já ter sido declarada.

A análise deve processar as declarações na ordem em que aparecem no arquivo.

Para cada declaração:

1. Verificar se todas as variáveis usadas na expressão já foram declaradas.
2. Se houver variável não declarada, reportar erro e interromper a compilação.
3. Se a expressão estiver correta, adicionar a variável declarada à tabela de símbolos.

Depois de analisar todas as declarações, o compilador deve verificar a expressão final usando a tabela de símbolos resultante.

---

# 6. Tabela de símbolos

A tabela de símbolos é a estrutura usada para registrar nomes conhecidos pelo compilador.

Na linguagem EV, ela precisa guardar apenas quais variáveis já foram declaradas.

Implementações possíveis:

* um `set` com os nomes declarados;
* um dicionário associando nomes a valores booleanos;
* uma estrutura global ou um objeto compartilhado pela análise semântica.

Exemplo:

```ev
x = 7 * 8;
y = x * 11 - 17;
= x * y + 33
```

Processamento semântico:

1. A expressão `7 * 8` não usa variáveis, então `x` pode ser inserido na tabela.
2. A declaração de `y` usa `x`, que já está na tabela, então `y` pode ser inserido.
3. A expressão final usa `x` e `y`, ambos já declarados.

O programa é semanticamente válido.

---

# 7. Geração de código

Após a análise sintática e a análise semântica, o compilador pode gerar código assembly.

Uma variável pode ser tratada como uma região de memória reservada para armazenar um inteiro de 64 bits.

## Seção BSS

As variáveis devem ser declaradas na seção `.bss`, usada para dados não inicializados.

Exemplo:

```assembly
.section .bss
.lcomm x, 8
.lcomm y, 8
```

Cada variável ocupa `8` bytes.

## Escrita em variável

Depois de gerar o código da expressão do lado direito de uma declaração, o resultado estará em `%rax`.

Para armazenar esse valor na variável:

```assembly
mov %rax, x
```

## Leitura de variável

Para carregar o valor de uma variável em `%rax`:

```assembly
mov x, %rax
```

## Processo de geração

O PDF descreve o seguinte processo:

1. Percorrer as declarações da AST para descobrir quais variáveis precisam aparecer na seção `.bss`.
2. Gerar uma diretiva `.lcomm` para cada variável.
3. Percorrer as declarações novamente, gerando o código da expressão de cada uma.
4. Ao final de cada declaração, mover `%rax` para a variável correspondente.
5. Gerar o código da expressão final.
6. Chamar as rotinas de impressão e saída.

Modelo geral do assembly:

```assembly
.section .bss
# diretivas das variaveis

.section .text
.globl _start
_start:
# codigo das declaracoes
# codigo da expressao final
call imprime_num
call sair

.include "runtime.s"
```

## Exemplo completo

Programa-fonte:

```ev
x = 11 * 7;
y = x * 3 + 5;
= x * y
```

Assembly esperado em alto nível:

```assembly
.section .bss
.lcomm x, 8
.lcomm y, 8

.section .text
.globl _start
_start:
# x = 11 * 7;
mov $11, %rax
push %rax
mov $7, %rax
pop %rbx
mul %rbx
mov %rax, x

# y = x * 3 + 5;
mov x, %rax
push %rax
mov $3, %rax
pop %rbx
mul %rbx
push %rax
mov $5, %rax
pop %rbx
add %rbx, %rax
mov %rax, y

# = x * y
mov x, %rax
push %rax
mov y, %rax
pop %rbx
mul %rbx

call imprime_num
call sair

.include "runtime.s"
```

---

# 8. Variações sintáticas

O PDF permite que o grupo implemente a linguagem EV original ou uma variação sintática equivalente.

A sintaxe base usa `=` para a expressão final:

```ev
x = (7 + 4) * 12;
y = x * 3 + 11;
= (x * y) + (x * 11) + (y * 13)
```

Uma variação possível é trocar a expressão final por `return`:

```ev
x = (7 + 4) * 12;
y = x * 3 + 11;
return (x * y) + (x * 11) + (y * 13)
```

Outras variações podem se inspirar em Pascal ou C, desde que preservem os componentes fundamentais:

* declarações;
* expressões;
* referências a variáveis;
* expressão ou comando final de resultado;
* mesma AST conceitual.

Caso o grupo escolha uma variação sintática, a documentação do projeto deve declarar explicitamente a gramática adotada.

---

# 9. Artefato para entrega

O grupo deve entregar um compilador para a linguagem EV ou para uma variação sintática documentada.

O projeto deve incluir:

* suporte a declarações de variáveis;
* suporte ao uso de variáveis em expressões;
* verificação de variáveis não declaradas;
* geração de código assembly para variáveis usando `.bss`;
* testes com programas válidos que usam variáveis;
* testes que demonstrem erro para variáveis não declaradas;
* documentação concisa explicando como usar o compilador;
* documentação explicando como executar os testes.

---
