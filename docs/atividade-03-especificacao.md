# Atividade 03 — Congruência de Zeller

> **Metadados do PDF original**
> - **Arquivo:** `CC_-_Atividade_03.pdf`
> - **Autor:** Andrei Formiga (professor)
> - **Data:** 14 de maio de 2026
> - **Páginas:** 5
> - **Disciplina:** Construção de Compiladores (P6 — UFPB)
>
> **Material de apoio:** `slides/Intro-Assembly (1).pdf` (Introdução ao Assembly x86-64)
>
> **Sobre este documento:**
> Transcrição fiel + comentários pedagógicos do PDF da atividade. Onde aparecer **citação textual**, marca como blockquote. Onde aparecer comentário/inferência, marca como **Observação:**.

---

## Sumário

1. [Introdução](#1-introdução-página-3)
2. [Parte 1: Congruência de Zeller](#2-parte-1-congruência-de-zeller-página-4)
3. [Parte 2: Perguntas](#3-parte-2-perguntas-página-5)

E mais (acréscimos meus):

- [Apêndice A — Fórmula formatada e referência rápida](#apêndice-a--fórmula-formatada-e-referência-rápida)
- [Apêndice B — Mapeamento completo de meses](#apêndice-b--mapeamento-completo-de-meses)
- [Apêndice C — Exemplos de cálculo manual](#apêndice-c--exemplos-de-cálculo-manual)
- [Apêndice D — Checklist de entrega](#apêndice-d--checklist-de-entrega)

---

## 1. Introdução (página 3)

> **Citação textual do PDF:**
> *"O objetivo desta atividade é criar um programa em assembly x86-64 para calcular a congruência de Zeller, uma fórmula que permite calcular o dia da semana para qualquer data."*

**Pontos centrais:**

- A atividade é **programar diretamente em assembly x86-64** — diferente da Atividade 02, onde o foco era construir um compilador que gerasse assembly. Aqui não tem compilador no meio: o aluno escreve o assembly à mão.
- A função implementada é a **congruência de Zeller**, fórmula matemática que dado dia/mês/ano calcula o dia da semana correspondente.

**Observação pedagógica:**
Essa atividade é um pivô importante na disciplina — antes de gerar assembly automaticamente (próximas atividades), o aluno precisa entender **a fluência manual da linguagem alvo**. Escrever Zeller à mão treina precedência de operações, uso de registradores, IDIV com CQO, e ordem de avaliação. Tudo o que um compilador de expressões aritméticas vai precisar emitir.

---

## 2. Parte 1: Congruência de Zeller (página 4)

### 2.1. A fórmula

> **Citação textual do PDF:**
> *"A fórmula da congruência de Zeller é:"*
>
> $$h = \left( q + \left\lfloor \frac{13(m+1)}{5} \right\rfloor + k + \left\lfloor \frac{k}{4} \right\rfloor + \left\lfloor \frac{j}{4} \right\rfloor - 2j \right) \bmod 7$$

Em texto plano:

```
h = (q + floor(13*(m+1)/5) + k + floor(k/4) + floor(j/4) - 2*j) mod 7
```

### 2.2. Significado dos símbolos

> **Citação textual:**
> *"Nesta fórmula, ℎ é um número que vai representar o dia da semana, com 0 representando o sábado, 1 o domingo, 2 a segunda-feira, e por aí vai, até 6 que representa a sexta-feira."*

**Tabela de h → dia da semana:**

| `h` | Dia |
|---|---|
| 0 | Sábado |
| 1 | Domingo |
| 2 | Segunda-feira |
| 3 | Terça-feira |
| 4 | Quarta-feira |
| 5 | Quinta-feira |
| 6 | Sexta-feira |

> **Citação textual:**
> *"𝑞 é o dia do mês; 𝑚 é um número que representa o mês, com valor entre 3 e 14: 3 é março, 4 é abril, até 12 que é dezembro, depois 13 para janeiro e 14 para fevereiro."*

**Mapeamento de meses (atenção — não é o mês "normal"):**

| Mês real | Valor de `m` na fórmula |
|---|---|
| Março | 3 |
| Abril | 4 |
| Maio | 5 |
| Junho | 6 |
| Julho | 7 |
| Agosto | 8 |
| Setembro | 9 |
| Outubro | 10 |
| Novembro | 11 |
| Dezembro | 12 |
| **Janeiro** | **13** |
| **Fevereiro** | **14** |

### 2.3. A pegadinha do ano em janeiro/fevereiro

> **Citação textual (importante!):**
> *"𝑘 e 𝑗 juntos representam o ano ajustado, com 𝑘 sendo o ano dentro do século (a unidade e dezena do ano) e 𝑗 sendo a parte do século (centena e milhar do ano). Por exemplo, para datas a partir de março de 2026 o 𝑗 é 20 e o 𝑘 é 26; mas para datas em janeiro e fevereiro (de qualquer ano), o ano é considerado como sendo o ano anterior. Por exemplo, datas em janeiro e fevereiro de 2024 vão ter 𝑗 = 20 e 𝑘 = 23."*

**Resumindo:**

- `j` = século (parte alta do ano) — ex: 20 pra ano 2026, 19 pra 1998
- `k` = ano dentro do século (parte baixa) — ex: 26 pra 2026, 98 pra 1998
- **Janeiro/Fevereiro:** trate como se fosse o **ano anterior**

**Exemplos práticos:**

| Data | Mês real | `m` | Ano real | Ano ajustado | `j` | `k` |
|---|---|---|---|---|---|---|
| 23/abril/2026 | abril | 4 | 2026 | 2026 | 20 | 26 |
| 15/dezembro/2026 | dezembro | 12 | 2026 | 2026 | 20 | 26 |
| 5/janeiro/2026 | janeiro | **13** | 2026 | **2025** | 20 | **25** |
| 14/fevereiro/2024 | fevereiro | **14** | 2024 | **2023** | 20 | **23** |
| 1/janeiro/2000 | janeiro | **13** | 2000 | **1999** | **19** | **99** |

### 2.4. Sobre as divisões (IDIV)

> **Citação textual:**
> *"Como todos os valores usados são positivos, as divisões com a função piso (⌊x/y⌋) são apenas divisões inteiras, que são calculadas facilmente com a instrução IDIV. A função mod calcula o resto da divisão, portanto na fórmula da congruência toda a quantia dentro dos parênteses é calculada e o resultado final é o resto da divisão dessa quantia por 7."*

**Pontos centrais:**

- **Função piso `⌊x/y⌋`** = divisão inteira (truncamento). Como todos os valores aqui são positivos, basta usar IDIV e pegar o quociente.
- **Operação `mod`** = resto da divisão. Em x86-64, IDIV deixa o **quociente em RAX** e o **resto em RDX** automaticamente. Pra `mod 7`, divide o resultado por 7 e pega RDX.

### 2.5. Onde ficam as entradas

> **Citação textual:**
> *"A parte 1 da atividade consiste em escrever um programa em linguagem assembly x86-64 que calcula o valor da congruência de Zeller, considerando o valor de 𝑞 no registrador R8, 𝑚 no registrador R9, 𝑘 em R10 e 𝑗 em R11. Para testar, coloque valores adequados nesses registradores."*

**Convenção de entrada (FIXA — não negociável):**

| Variável | Registrador |
|---|---|
| `q` (dia do mês) | **R8** |
| `m` (mês ajustado) | **R9** |
| `k` (ano dentro do século) | **R10** |
| `j` (século) | **R11** |

**Saída:** o programa deve colocar o resultado `h` em algum registrador (provavelmente RAX, por padrão da disciplina) e ser visível ao final da execução.

### 2.6. Programa de verificação

> **Citação textual:**
> *"Escreva também um pequeno programa em linguagem de alto nível que calcula a congruência, para verificar os resultados obtidos no programa em assembly."*

**Pontos centrais:**

- Linguagem livre — Python, C, Java, JavaScript, etc.
- Propósito: implementar a **mesma fórmula** numa linguagem confiável e comparar com a saída do assembly.
- É uma forma de **validação cruzada** — se Python diz "3" e assembly diz "5", o assembly tá errado.

### 2.7. O que entregar (Parte 1)

> **Citação textual:**
> *"Entrega: o arquivo com o programa assembly que calcula a congruência de Zeller e o arquivo com o programa em linguagem de alto nível usado para verificar os resultados."*

**Checklist Parte 1:**

- [ ] Arquivo `.s` com o programa assembly que calcula Zeller
- [ ] Arquivo na linguagem de alto nível escolhida que faz a mesma coisa (referência de verificação)

---

## 3. Parte 2: Perguntas (página 5)

> **Citação textual:**
> *"Em breve vamos criar compiladores que geram código assembly para expressões aritméticas arbitrárias, e com isso é preciso pensar em quantos registradores são necessários para uma expressão qualquer."*
>
> *"Responda as seguintes questões sobre a tradução de expressões aritméticas para assembly x86-64:"*

### 3.1. Pergunta 1 — Soma de constantes

> **Citação textual:**
>
> *"1. Qual o menor número de registradores necessários para calcular expressão*
>
> $$a_1 + a_2 + \ldots + a_n$$
>
> *em assembly? (Todos os $a_1, a_2, \ldots, a_n$ são inteiros constantes.)"*

### 3.2. Pergunta 2 — Soma de produtos

> **Citação textual:**
>
> *"2. Qual o menor número de registradores necessários para calcular expressão*
>
> $$(a_{11} * a_{12} * \ldots * a_{1n}) + \ldots + (a_{m1} * a_{m2} * \ldots * a_{mn})$$
>
> *em assembly? (Todos os $a_{ij}$ são inteiros constantes.)"*

### 3.3. Pergunta 3 — Limite teórico

> **Citação textual:**
> *"3. Existe alguma forma de calcular expressões aritméticas constantes (com soma, subtração, multiplicação e divisão) de tamanho arbitrário com um número limitado de registradores, ou o número de registradores pode crescer sem limite? Tente justificar sua resposta."*

### 3.4. O que entregar (Parte 2)

> **Citação textual:**
> *"Entrega: as respostas para as três questões acima."*

**Observação pedagógica:**
As 3 perguntas formam uma escada de complexidade: (1) caso simples, (2) caso intermediário com agrupamento, (3) caso geral. A resposta da pergunta 3 é a chave conceitual — ela é o que justifica usar **pilha (stack)** na geração de código pra expressões arbitrárias, técnica que provavelmente vai aparecer na próxima atividade.

---

## Apêndice A — Fórmula formatada e referência rápida

**Fórmula completa em texto:**

```
h = (q + floor(13*(m+1)/5) + k + floor(k/4) + floor(j/4) - 2*j) mod 7
```

**Ordem de avaliação sugerida:**

1. Calcular `tmp1 = 13 * (m+1) / 5` (divisão inteira, piso)
2. Calcular `tmp2 = k / 4`
3. Calcular `tmp3 = j / 4`
4. Somar: `soma = q + tmp1 + k + tmp2 + tmp3 - 2*j`
5. Calcular `h = soma mod 7`

**Tipos de operação envolvidos:**

| Operação | Quantidade | Instruções x86-64 |
|---|---|---|
| Adição | 4 | `add` |
| Subtração | 1 | `sub` |
| Multiplicação | 2 | `imul` |
| Divisão inteira (com piso) | 3 | `idiv` (precedida de `cqo`) |
| Resto (mod) | 1 | `idiv` (resto em RDX) |

---

## Apêndice B — Mapeamento completo de meses

```
Mês real     →  m na fórmula  →  Ano usado
─────────────────────────────────────────────
Janeiro      →  13            →  ano - 1
Fevereiro    →  14            →  ano - 1
Março        →   3            →  ano
Abril        →   4            →  ano
Maio         →   5            →  ano
Junho        →   6            →  ano
Julho        →   7            →  ano
Agosto       →   8            →  ano
Setembro     →   9            →  ano
Outubro      →  10            →  ano
Novembro     →  11            →  ano
Dezembro     →  12            →  ano
```

**Importante:** o ajuste de ano (subtrair 1 em jan/fev) NÃO está dentro da fórmula assembly — é uma preparação que o "programa caller" deve fazer antes de colocar `j` e `k` nos registradores. O programa assembly só recebe os valores já ajustados.

---

## Apêndice C — Exemplos de cálculo manual

### Exemplo 1 — 17 de maio de 2026 (domingo)

- Data: 17/maio/2026
- `q = 17`, `m = 5` (maio), ano = 2026
- Como `m >= 3`, não ajusta ano → `j = 20`, `k = 26`

Cálculo:
```
tmp1 = floor(13 * (5+1) / 5) = floor(13*6/5) = floor(78/5) = 15
tmp2 = floor(26/4) = 6
tmp3 = floor(20/4) = 5
soma = 17 + 15 + 26 + 6 + 5 - 2*20 = 17 + 15 + 26 + 6 + 5 - 40 = 29
h = 29 mod 7 = 1
```
**Resultado: h = 1 = Domingo ✓** (17/maio/2026 é realmente domingo)

### Exemplo 2 — 1 de janeiro de 2024 (segunda)

- Data: 1/jan/2024
- `q = 1`, `m = 13` (janeiro vira 13), ano ajustado = 2023 → `j = 20`, `k = 23`

Cálculo:
```
tmp1 = floor(13 * (13+1) / 5) = floor(13*14/5) = floor(182/5) = 36
tmp2 = floor(23/4) = 5
tmp3 = floor(20/4) = 5
soma = 1 + 36 + 23 + 5 + 5 - 2*20 = 1 + 36 + 23 + 5 + 5 - 40 = 30
h = 30 mod 7 = 2
```
**Resultado: h = 2 = Segunda-feira ✓**

### Exemplo 3 — 25 de dezembro de 2026 (sexta — Natal)

- Data: 25/dez/2026
- `q = 25`, `m = 12`, ano = 2026 → `j = 20`, `k = 26`

Cálculo:
```
tmp1 = floor(13 * (12+1) / 5) = floor(13*13/5) = floor(169/5) = 33
tmp2 = floor(26/4) = 6
tmp3 = floor(20/4) = 5
soma = 25 + 33 + 26 + 6 + 5 - 2*20 = 25 + 33 + 26 + 6 + 5 - 40 = 55
h = 55 mod 7 = 6
```
**Resultado: h = 6 = Sexta-feira ✓** (Natal 2026 é sexta)

---

## Apêndice D — Checklist de entrega

### Parte 1 — Congruência de Zeller

- [ ] Arquivo `.s` com programa assembly funcional
- [ ] Lê `q` de R8, `m` de R9, `k` de R10, `j` de R11
- [ ] Calcula `h = (q + floor(13(m+1)/5) + k + floor(k/4) + floor(j/4) - 2j) mod 7`
- [ ] Resultado fica visível (RAX recomendado)
- [ ] Programa monta com `as --64` sem erros
- [ ] Programa linka com `ld` sem erros
- [ ] Executável roda e produz resultado correto pra entradas conhecidas
- [ ] Programa em linguagem de alto nível (verificação) que produz o mesmo resultado
- [ ] Comparação cruzada entre os dois confirma que assembly tá correto

### Parte 2 — Perguntas teóricas

- [ ] Resposta à pergunta 1 (menor número de registradores pra soma simples)
- [ ] Resposta à pergunta 2 (menor número de registradores pra soma de produtos)
- [ ] Resposta à pergunta 3 (limite teórico + justificativa)

---

**Última atualização deste documento:** 2026-05-20 (durante leitura inicial do PDF).
