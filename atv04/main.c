#include <stdio.h>

int main(int argc, char **argv) {
    FILE *input;
    int ch;

    if (argc != 2) {
        fprintf(stderr, "Uso: %s <arquivo.ec1>\n", argv[0]);
        return 1;
    }

    input = fopen(argv[1], "r");
    if (input == NULL) {
        fprintf(stderr, "Erro: nao foi possivel abrir '%s'\n", argv[1]);
        return 1;
    }

    while ((ch = fgetc(input)) != EOF) {
        (void)ch;
    }

    fclose(input);
    return 0;
}
