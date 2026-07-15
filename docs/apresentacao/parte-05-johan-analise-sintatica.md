# Vídeo Marco 1 — Análise Sintática (Atividade 05)

**Apresentador:** Johan Carlos
**Duração alvo:** ~2 min 30 s a 3 min
**Posição no vídeo:** depois da Análise Léxica (Atividade 04) e antes da Geração de Código (Atividade 06)

**Antes de gravar:** abrir o terminal e estar na pasta base:
```bash
cd ~/ufpb/P6/construcao-de-compiladores
```

---

## Roteiro de fala

> Marcações: **[TELA]** indica o que mostrar. **[DIGITAR]** são os comandos pra eu rodar ao vivo (já estão prontos pra copiar/digitar). O resto é o texto que eu falo, pode adaptar com naturalidade.

### 1. Abertura — ~20 s

Oi, meu nome é Johan, e nessa parte eu vou falar da Atividade 05, que é a análise sintática do nosso compilador.

Pra contextualizar: na Atividade 04, a análise léxica, a gente viu como o compilador pega o texto do programa e quebra ele em tokens, que são tipo as "palavras" da linguagem. Mas até aqui esses tokens são só uma sequência solta, um do lado do outro. O compilador ainda não sabe a **estrutura** da expressão, quem opera com quem. E é exatamente isso que a análise sintática resolve: ela pega essa lista de tokens e descobre a estrutura por trás dela, montando uma árvore.

### 2. O que a análise sintática faz — ~30 s

**[TELA: mostrar a expressão `(33 + (912 * 11))` num editor ou no slide]**

Vou usar essa expressão como exemplo. Olhando ela, a gente entende naturalmente que primeiro tem que fazer o `912 * 11`, e só depois somar com 33. Essa ordem está implícita nos parênteses.

A análise sintática deixa essa estrutura **explícita**, construindo o que a gente chama de árvore de sintaxe abstrata, ou AST. Nessa árvore, a soma fica na raiz, com o 33 de um lado e a multiplicação do outro. A estrutura da árvore captura exatamente a estrutura da expressão.

### 3. Como a árvore é representada — ~30 s

**[TELA: abrir o `arvore.py` e mostrar as classes Const e OpBin]**

**[DIGITAR]**
```bash
cd projeto-compiladores/atv05
```

Pra representar essa árvore a gente usou duas classes. A `Const`, que é uma folha da árvore, guarda só um número. E a `OpBin`, que é uma operação binária, guarda o operador e dois filhos: o operando da esquerda e o da direita. E esses filhos também são expressões, o que é justamente o que permite o aninhamento.

### 4. Como construímos a árvore: descida recursiva — ~45 s

**[TELA: abrir o `parser.py` e mostrar as funções `analisa_exp` e `analisa_operador`]**

A técnica que a gente usou pra montar a árvore chama análise descendente recursiva. A ideia é simples: criar uma função para cada regra da gramática.

A função principal é a `analisa_exp`. Ela olha o próximo token e decide o que fazer. Se o próximo token é um número, ela cria uma constante. Se é um abre-parêntese, ela sabe que é uma operação binária, então ela analisa a expressão da esquerda, identifica o operador, analisa a expressão da direita, e verifica se fecha o parêntese no final.

O detalhe importante é que, pra analisar os operandos, a `analisa_exp` chama **ela mesma**. Por isso o nome recursiva. É essa recursão que faz o aninhamento funcionar sozinho, sem nenhum esforço extra.

### 5. Demo — ~45 s

**[TELA: terminal]**

Agora deixa eu mostrar rodando. Vou criar um arquivo com aquela expressão e passar pro nosso programa.

**[DIGITAR]**
```bash
echo '(33 + (912 * 11))' > exemplo.ec1
python3 main.py --arvore exemplo.ec1
```

**[TELA: deixar a saída na tela enquanto explica]**

Rodando, o programa mostra três coisas. Primeiro, a árvore reconstruída, que bate com a entrada original, o que já prova que a estrutura foi entendida certo. Depois, a mesma árvore num formato visual, onde dá pra ver a soma na raiz e a multiplicação como filho da direita. E por último, o valor da expressão, que é 10065.

Esse valor vem de um interpretador que a gente também implementou: ele percorre a árvore, calcula os filhos primeiro e depois aplica o operador.

E a gente também trata erro de sintaxe. Se a expressão estiver malformada, tipo faltando um operando, o analisador identifica e reporta em vez de quebrar:

**[DIGITAR]**
```bash
echo '(1 + )' > erro.ec1
python3 main.py erro.ec1
```

**[TELA: mostrar a mensagem de erro]**

Aqui ele acusa um token inesperado, que é o parêntese fechando sem o segundo operando.

### 6. Transição pra Atividade 06 — ~15 s

Então, no fim da minha parte, a gente saiu de uma lista de tokens e chegou nessa árvore, que já tem toda a estrutura da expressão organizada. A partir daqui, na Atividade 06, a geração de código, a gente vai ver como pegar essa árvore e transformar ela em código assembly de verdade.

---

## Todos os comandos da demo (já partindo da pasta base)

Estando em `~/ufpb/P6/construcao-de-compiladores`:

```bash
# entra na pasta da atividade 05
cd projeto-compiladores/atv05

# demo principal: arvore + visual + valor
echo '(33 + (912 * 11))' > exemplo.ec1
python3 main.py --arvore exemplo.ec1

# demo de erro de sintaxe
echo '(1 + )' > erro.ec1
python3 main.py erro.ec1
```

Saída esperada da demo principal:

```
Arvore: (33 + (912 * 11))
Arvore (visual):
+
├── 33
└── *
    ├── 912
    └── 11
Valor: 10065
```

Saída esperada da demo de erro:

```
Erro sintático: token inesperado: ')'
```

---

## Checklist do que não esquecer

- [ ] Abrir falando o nome e dizendo que é a Atividade 05 (análise sintática)
- [ ] Contextualizar a partir da Atividade 04 (tokens são uma lista, falta a estrutura)
- [ ] Explicar a AST com a ideia de "estrutura explícita"
- [ ] Citar as duas classes: `Const` (folha) e `OpBin` (operação + dois filhos)
- [ ] Explicar "uma função por regra da gramática" (descida recursiva)
- [ ] Destacar a recursão que resolve o aninhamento
- [ ] Demo: árvore linear + visual + valor (interpretador)
- [ ] Mostrar o erro de sintaxe sendo tratado
- [ ] Passar a bola pra Atividade 06 (a árvore vai virar assembly)

## Dicas de gravação

- Deixar o terminal já na pasta base (`~/ufpb/P6/construcao-de-compiladores`) antes de começar.
- Aumentar a fonte do terminal pra ficar legível no vídeo.
- A árvore visual é o ponto mais "bonito" de mostrar, vale dar um tempinho nela.
- Falar com calma na parte da recursão, que é o conceito central.
- Se quiser, já deixar os arquivos `exemplo.ec1` e `erro.ec1` criados antes e só rodar os `python3` na hora, pra não digitar muito.
