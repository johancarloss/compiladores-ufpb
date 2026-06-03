# Dockerfile — Testes do Compilador EC1 (Geração de Código)
# A imagem python:3 é baseada em Debian e já possui gcc, as, ld e make instalados.
FROM python:3

WORKDIR /app

# Copia os arquivos da atv06 para o container
COPY . .

# Comando padrão roda o script de testes que compila, monta, linka e executa os binários
CMD ["python3", "testes.py"]
