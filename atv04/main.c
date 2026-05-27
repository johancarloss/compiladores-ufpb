#include "token.h"
#include "lexer.h"
#include <stdio.h>
#include <stdlib.h>

static char *le_arquivo(const char *caminho) {
    FILE *f = fopen(caminho, "rb");
    if (!f) return NULL;

    fseek(f, 0, SEEK_END);
    long tam = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *buf = malloc(tam + 1);
    if (!buf) { fclose(f); return NULL; }

    fread(buf, 1, tam, f);
    buf[tam] = '\0';
    fclose(f);
    return buf;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <arquivo.ec1>\n", argv[0]);
        return 1;
    }

    char *fonte = le_arquivo(argv[1]);
    if (!fonte) {
        fprintf(stderr, "Erro: nao foi possivel abrir '%s'\n", argv[1]);
        return 1;
    }

    Lexico lx = lex(fonte);

    for (size_t i = 0; i < lx.n; i++)
        token_print(&lx.tokens[i]);

    int status = 0;
    if (lx.houve_erro) {
        printf("Erro léxico na posição %zu: caractere inválido '%c'\n",
               lx.erro_pos, lx.erro_char);
        status = 1;
    }

    lexico_free(&lx);
    free(fonte);
    return status;
}
