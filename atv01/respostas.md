# Construção de Compiladores — Atividade 1
## Questionário Inicial

**Aluno:** Johan Carlos Pereira Fernandes

---

### 1. O que é um compilador?

Um compilador é um programa que pega um código escrito em uma linguagem (a chamada "linguagem fonte") e traduz pra outra linguagem (a "linguagem alvo"), normalmente de um nível mais alto pra um nível mais baixo, tipo de C pra assembly. Mas no caso ele não faz isso de uma vez só, é um pipeline com várias etapas — análise léxica, sintática, semântica, geração de código intermediário, otimização e geração do código final. Cada etapa pega o código numa representação diferente e transforma na próxima, até chegar no resultado.

Outra coisa importante é que compilador não é só pra "virar assembly". TypeScript pra JavaScript é compilação, SQL virando plano de execução no Postgres é compilação, Python virando bytecode `.pyc` também é. O conceito é mais amplo do que parece.

---

### 2. Qual a diferença entre um compilador e um interpretador?

A diferença mais comum que se fala é "compilador traduz tudo antes, interpretador executa linha por linha". Isso não tá errado, mas é uma resposta meio rasa, porque na prática quase todas as linguagens hoje misturam os dois.

A diferença real, no caso, é em duas coisas:

1. **Se sobra um artefato** — o compilador gera um arquivo (executável, bytecode, etc.) que persiste depois da tradução. O interpretador não, ele executa e descarta.
2. **Quando a tradução acontece** — compilador faz antes (AOT, "ahead of time"), interpretador faz durante a execução.

Por exemplo, o Python parece interpretado, mas no fundo ele é híbrido: quando você roda `python script.py`, o CPython compila o código pra bytecode (gera o `.pyc` em `__pycache__`), e ai uma VM interpreta esse bytecode. Tem etapa de compilação ali no meio. O Java é parecido, mas vai além — compila pra bytecode `.class` e depois o JIT da JVM ainda compila partes pra código nativo em runtime.

Então não é uma divisão rígida, é mais um espectro: tem coisa que é puro compilador (gcc), tem coisa que é puro interpretador (bash), e tem muita coisa híbrida no meio.

---

### 3. Por quê estudar compiladores?

Acho que tem alguns motivos que valem a pena listar:

**Primeiro**, técnicas de compilador aparecem em um monte de lugar que a gente usa todo dia sem perceber. `JSON.parse`, regex, `EXPLAIN ANALYZE` no Postgres, validação do Pydantic, ESLint, template engine — tudo isso usa lexer, parser e análise por trás. Saber a teoria ajuda a entender essas ferramentas e até contribuir com elas.

**Segundo**, o pipeline de fases de um compilador (léxica → sintática → semântica → IR → otimização → geração) é um dos exemplos mais limpos de separação de responsabilidades em software. Cada fase tem entrada e saída bem definidas e zero conhecimento das outras. Esse mesmo padrão arquitetural reaparece em ETL, processamento de requests no FastAPI, pipelines de agentes LLM, e por ai vai.

**Terceiro**, em algum momento da carreira, é bem possível ter que desenhar uma DSL — pra config, pra automação, pra regras de negócio. Sem saber compiladores, a gente acaba reinventando parser ad-hoc com regex, e o resultado fica frágil. Saber a teoria dá ferramentas pra fazer direitinho.

**Por último**, no dia-a-dia de debug, entender as fases muda como você raciocina sobre erros. Erro de sintaxe estranho? Suspeita do parser. Variável não encontrada? Análise semântica. Performance ruim? Pensa em otimização. Vira um nível a mais de entendimento que ajuda em qualquer linguagem que você usa.
