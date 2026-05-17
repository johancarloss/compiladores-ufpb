# Makefile do compilador CI
# Atividade 02 - Construcao de Compiladores - UFPB P6

# === Variaveis ===
CC = gcc
CFLAGS = -Wall -Wextra -std=c99
AS = as
ASFLAGS = --64
LD = ld

# === Regras principais ===

# Alvo padrao: compila o compilador
compci: compci.c
			$(CC) $(CFLAGS) -o compci compci.c

# Pipeline end-to-end com tests/p1.ci
test: compci runtime.s
			@echo "=== 1. Compilando tests/p1.ci -> tests/p1.s ==="
			./compci tests/p1.ci
			@echo
			@echo "=== 2. Copiando runtime.s pra tests/ ==="
			cp runtime.s tests/
			@echo
			@echo "=== 3. Montando e linkando ==="
			cd tests && $(AS) $(ASFLAGS) -o p1.o p1.s && $(LD) -o p1 p1.o
			@echo
			@echo "=== 4. Executando tests/p1 (deve imprimir 42) ==="
			./tests/p1
			@echo "Exit code: $$?"

# Demonstra erro de sintaxe (esperado falhar)
test-erro: compci
			@echo "=== Testando tests/erro.ci (deve falhar com erro de sintaxe) ==="
			-./compci tests/erro.ci
			@echo "(falhou como esperado)"

# Limpa todos os artefatos gerados
clean:
			rm -f compci
			rm -f tests/*.s tests/*.o
			rm -f tests/p1 tests/erro tests/grande tests/p2
			rm -f tests/runtime.s
			@echo "Limpeza completa."

# Build da imagem Docker
docker-build:
			docker build -t compci .

# Roda o container (executa 'make test' dentro)
docker-run: docker-build
			docker run --rm compci

.PHONY: test test-erro clean docker-build docker-run