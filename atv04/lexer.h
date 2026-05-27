// Analisador léxico da linguagem EC1.

#ifndef LEXER_H
#define LEXER_H

#include "token.h"

typedef struct {
    Token  *tokens;
    size_t  n;
    int     houve_erro;
    size_t  erro_pos;
    char    erro_char;
} Lexico;

// Tokeniza `fonte`. Em erro léxico, para no primeiro caractere inválido
// e marca houve_erro (os tokens já reconhecidos ficam em .tokens).
Lexico lex(const char *fonte);

void lexico_free(Lexico *lx);

#endif
