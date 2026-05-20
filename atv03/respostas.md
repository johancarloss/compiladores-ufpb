# Atividade 03 — Parte 2: Perguntas

## 1. Menor número de registradores para calcular $a_1 + a_2 + \ldots + a_n$

**Resposta: 1 registrador.**

Como todos os $a_i$ são constantes inteiras, dá pra usar a forma da instrução `add` que aceita um operando imediato (constante carregada direto na instrução). Ou seja, basta começar carregando $a_1$ num registrador (tipo RAX) e ir somando cada constante seguinte com `add imediato, %rax`. Não precisa de um segundo registrador pra "segurar" o valor sendo somado, porque ele já está na própria instrução.

O código fica assim:

```gas
mov $a1, %rax
add $a2, %rax
add $a3, %rax
...
add $an, %rax
```

No fim, RAX tem a soma total. Independente de quantos termos $n$ sejam, 1 registrador resolve.

(Observação: a instrução `add` em x86-64 tem o imediato limitado a 32 bits. Se as constantes fossem maiores que isso, precisaria de 1 registrador extra pra carregar via `movabs` antes de somar. Pra inteiros no tamanho usual da disciplina, 1 registrador é suficiente.)

---

## 2. Menor número de registradores para calcular $(a_{11} * \ldots * a_{1n}) + \ldots + (a_{m1} * \ldots * a_{mn})$

**Resposta: 2 registradores.**

A ideia é dividir o cálculo em duas funções: um registrador (RAX) vai calculando o produto atual de cada parêntese, e outro registrador (RBX) vai acumulando a soma desses produtos.

Pra cada parêntese, começa carregando a primeira constante em RAX e usa `imul imediato, %rax` pra multiplicar pelas constantes seguintes. Quando o produto termina, soma o valor de RAX em RBX. Depois recomeça RAX com a primeira constante do próximo parêntese.

O código fica assim:

```gas
# Primeiro produto: rax = a11 * a12 * ... * a1n
mov $a11, %rax
imul $a12, %rax
imul $a13, %rax
...
mov %rax, %rbx          # rbx começa com o primeiro produto

# Segundo produto:
mov $a21, %rax
imul $a22, %rax
...
add %rax, %rbx          # rbx += segundo produto

# Continua até o m-ésimo produto.
```

No fim RBX tem a soma de todos os produtos. 2 registradores bastam pra qualquer $m$ e $n$.

---

## 3. É possível calcular expressões aritméticas arbitrárias com número limitado de registradores?

**Resposta: Sim, é possível.** O número de registradores não precisa crescer sem limite, desde que possamos usar memória externa (especificamente a pilha) pra guardar resultados intermediários.

A justificativa é a seguinte: se a gente insistir em manter tudo só em registradores, conforme a expressão fica mais aninhada (por exemplo, `((a+b) * (c+d)) + ((e+f) * (g+h))`), o número de valores intermediários que precisam estar "vivos" ao mesmo tempo cresce com a profundidade da árvore de expressão. Cada sub-expressão calculada precisa esperar a outra terminar pra ser combinada, então no caso geral o número de registradores necessários cresce com o tamanho da expressão.

Mas se a gente usa a pilha (stack) pra armazenar esses resultados intermediários, a história muda. Quando uma sub-expressão termina, dá pra fazer `push` do resultado pra pilha, liberando o registrador pra calcular outra coisa. Quando o valor for necessário de novo, dá pra fazer `pop` e trazer de volta. Assim, em qualquer momento da execução, só precisa ter alguns poucos registradores "ativos" (no limite, dá pra fazer com 1 ou 2), e a pilha cuida do resto.

Essa abordagem é conhecida como **stack machine** (máquina de pilha), e é o modelo clássico que compiladores usam pra avaliar expressões aritméticas arbitrárias. O algoritmo é uma travessia pós-ordem (postorder) da árvore de expressão: avalia o filho esquerdo, faz push do resultado, avalia o filho direito, faz pop do esquerdo, e aplica o operador.

No final, é uma troca: gasta mais memória (pilha), mas economiza em registradores. A pilha tem capacidade muito maior que o conjunto de registradores (limitada só pelo tamanho total da memória do processo), então essa troca é vantajosa pra expressões grandes.
