# Dockerfile — Compilador CI
# Imagem base: gcc:13 ja vem com gcc, make, binutils (as, ld) preinstalados.

FROM gcc:13

# Diretorio de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto pra dentro da imagem
COPY compci.c runtime.s Makefile ./
COPY tests/ ./tests/

# Compila o compilador durante o build da imagem
RUN make

# Comando padrao: roda o pipeline completo (compci -> as -> ld -> executa)
CMD ["make", "test"]