#include "lexer.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static int eh_espaco(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

static char *copia(const char *fonte, size_t inicio, size_t fim) {
    size_t len = fim - inicio;
    char *s = malloc(len + 1);
    memcpy(s, fonte + inicio, len);
    s[len] = '\0';
    return s;
}

Lexico lex(const char *fonte) {
    Lexico lx = {0};
    size_t cap = 16;
    lx.tokens = malloc(cap * sizeof(Token));

    size_t i = 0;
    while (fonte[i] != '\0') {
        char c = fonte[i];

        if (eh_espaco(c)) {
            i++;
            continue;
        }

        if (lx.n == cap) {
            cap *= 2;
            lx.tokens = realloc(lx.tokens, cap * sizeof(Token));
        }

        Token tok;
        tok.posicao = i;

        if (isdigit((unsigned char)c)) {
            size_t inicio = i;
            while (isdigit((unsigned char)fonte[i])) i++;
            tok.tipo = TK_NUMERO;
            tok.lexema = copia(fonte, inicio, i);
            lx.tokens[lx.n++] = tok;
            continue;
        }

        TokenTipo tipo;
        switch (c) {
            case '(': tipo = TK_PAREN_ESQ; break;
            case ')': tipo = TK_PAREN_DIR; break;
            case '+': tipo = TK_SOMA;      break;
            case '-': tipo = TK_SUB;       break;
            case '*': tipo = TK_MULT;      break;
            case '/': tipo = TK_DIV;       break;
            default:
                lx.houve_erro = 1;
                lx.erro_pos = i;
                lx.erro_char = c;
                return lx;
        }

        tok.tipo = tipo;
        tok.lexema = copia(fonte, i, i + 1);
        lx.tokens[lx.n++] = tok;
        i++;
    }

    return lx;
}

void lexico_free(Lexico *lx) {
    if (!lx || !lx->tokens) return;
    for (size_t k = 0; k < lx->n; k++)
        token_free(&lx->tokens[k]);
    free(lx->tokens);
    lx->tokens = NULL;
    lx->n = 0;
}
