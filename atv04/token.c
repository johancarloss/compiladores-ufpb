#include "token.h"
#include <stdio.h>
#include <stdlib.h>

const char *token_tipo_str(TokenTipo tipo) {
    switch (tipo) {
        case TK_NUMERO:    return "Numero";
        case TK_PAREN_ESQ: return "ParenEsq";
        case TK_PAREN_DIR: return "ParenDir";
        case TK_SOMA:      return "Soma";
        case TK_SUB:       return "Sub";
        case TK_MULT:      return "Mult";
        case TK_DIV:       return "Div";
        case TK_EOF:       return "EOF";
        default:           return "Desconhecido";
    }
}

void token_print(const Token *t) {
    printf("<%s, \"%s\", %zu>\n",
           token_tipo_str(t->tipo),
           t->lexema ? t->lexema : "",
           t->posicao);
}

void token_free(Token *t) {
    if (!t) return;
    free(t->lexema);
    t->lexema = NULL;
}
