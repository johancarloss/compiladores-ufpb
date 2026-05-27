// Tokens da linguagem EC1.

#ifndef TOKEN_H
#define TOKEN_H

#include <stddef.h>

typedef enum {
    TK_NUMERO,
    TK_PAREN_ESQ,
    TK_PAREN_DIR,
    TK_SOMA,
    TK_SUB,
    TK_MULT,
    TK_DIV,
    TK_EOF
} TokenTipo;

typedef struct {
    TokenTipo tipo;
    char     *lexema;   // alocado com strdup; liberar com token_free
    size_t    posicao;  // offset em caracteres na entrada
} Token;

const char *token_tipo_str(TokenTipo tipo);
void        token_print(const Token *t);
void        token_free(Token *t);

#endif
