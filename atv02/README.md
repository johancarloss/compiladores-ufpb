# Compilador CI (Constantes Inteiras)

Compilador para a linguagem CI (uma constante inteira de um ou mais dígitos), gerando código assembly x86-64 GAS para Linux.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 02

---

## Requisitos

- Linux x86-64
- `gcc`, GNU `as`, GNU `ld`, `make`
- (opcional) `docker` para execução em contêiner

Instalação em Ubuntu/Debian:

```bash
sudo apt install build-essential
```

## Estrutura

```
compci.c        # código-fonte do compilador (C)
runtime.s       # runtime fornecido (procedimentos imprime_num e sair)
Makefile        # build e testes (nativo e Docker)
Dockerfile      # build da imagem Docker (opcional)
.dockerignore   # arquivos ignorados no contexto Docker
README.md       # este arquivo
.gitignore
tests/
├── p1.ci       # teste válido (conteúdo: 42)
└── erro.ci     # teste com erro de sintaxe (conteúdo: 4a2)
```

## Como compilar o compilador

```bash
make
```

Equivalente a:

```bash
gcc -Wall -Wextra -std=c99 -o compci compci.c
```

## Como executar

```bash
./compci <arquivo.ci>
```

O compilador lê o arquivo `.ci`, valida que o conteúdo é uma constante inteira (apenas dígitos decimais), e gera um arquivo `.s` no mesmo diretório (substituindo a
extensão).

Para obter o executável final, é necessário montar e linkar o `.s` com o `runtime.s` no mesmo diretório:

```bash
cp runtime.s tests/
cd tests
as --64 -o p1.o p1.s
ld -o p1 p1.o
./p1            # imprime o conteúdo do arquivo original (ex: 42)
```

## Como testar (nativo)

```bash
make test       # pipeline end-to-end com tests/p1.ci (deve imprimir 42)
make test-erro  # demonstra detecção de erro de sintaxe
make clean      # remove todos os artefatos gerados
```

## Como testar (Docker)

Permite rodar o pipeline completo sem instalar nada localmente além do Docker:

```bash
make docker-build  # constrói a imagem (usa cache local se disponível)
make docker-run    # executa o container — equivale a 'make test' isolado
```

Equivalente a:

```bash
docker build --pull=false -t compci .
docker run --rm compci
```

A imagem usa `gcc:13` como base, já com `gcc`, `make` e `binutils` preinstalados.

## Erros detectados

| Mensagem | Causa |
|---|---|
| `Uso: ./compci <arquivo.ci>` | Argumento ausente na linha de comando |
| `Erro: nao foi possivel abrir 'X'` | Arquivo de entrada inexistente ou sem permissão |
| `Erro de sintaxe: arquivo vazio (esperado um inteiro)` | Arquivo sem conteúdo ou apenas whitespace |
| `Erro de sintaxe: caractere invalido 'X' na posicao N` | Caractere não-dígito encontrado |
| `Erro de sintaxe: constante 'X' eh muito grande para caber em 64 bits` | Constante numérica acima de `ULLONG_MAX` (overflow) |

Em qualquer caso de erro, o compilador escreve a mensagem em `stderr`, **não gera o arquivo `.s`**, e retorna código de saída `1`.

## Limitações

- O código gerado é específico para x86-64 Linux. Outras arquiteturas exigiriam adaptar o template em `compci.c` e o `runtime.s`.

## Autores

- Johan Carlos
- Luiz Augusto
- Diego de Carvalho
- Gabriel Lizst