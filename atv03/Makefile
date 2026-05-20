# Makefile do programa Zeller (Atividade 03)
# Construcao de Compiladores - UFPB P6

AS = as
ASFLAGS = --64
LD = ld

# Alvo padrao: monta e linka zeller.s
zeller: zeller.s
	$(AS) $(ASFLAGS) -o zeller.o zeller.s
	$(LD) -o zeller zeller.o

# Roda o assembly e a verificacao em Python lado a lado
test: zeller
	@echo "=== Executando zeller (assembly) ==="
	@./zeller; echo "h = $$?"
	@echo
	@echo "=== Executando zeller.py (verificacao) ==="
	@python3 zeller.py

# Apaga os artefatos gerados
clean:
	rm -f zeller zeller.o
	@echo "Limpeza completa."

.PHONY: test clean
