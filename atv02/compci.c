#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

int main(int argc, char const *argv[])
{
  // 1. Verificar que recebeu o argumento
  if (argc < 2) {
    fprintf(stderr, "Uso: %s <arquivo.ci>\n", argv[0]);
    return EXIT_FAILURE;
  }

  const char *arquivo_entrada = argv[1];

  // 2. Abrir o arquivo pra leitura
  FILE *fp_entrada = fopen(arquivo_entrada, "r");
  if (fp_entrada == NULL) {
    fprintf(stderr, "Erro: nao foi possivel abrir '%s'\n", arquivo_entrada);
    return EXIT_FAILURE;
  }

  // 3. Ler o conteudo do arquivo pra um buffer
  char buffer[256];
  size_t bytes_lidos = fread(buffer, 1, sizeof(buffer) - 1, fp_entrada);
  buffer[bytes_lidos] = '\0';
  fclose(fp_entrada);

  while (bytes_lidos > 0 && isspace((unsigned char)buffer[bytes_lidos - 1])) {
    bytes_lidos--;
  }
  buffer[bytes_lidos] = '\0';

  if (bytes_lidos == 0) {
    fprintf(stderr, "Erro de sintaxe: arquivo vazio (esperado um inteiro)\n");
    return EXIT_FAILURE;
  }

  for (size_t i = 0; i < bytes_lidos; i++) {
    if (!isdigit((unsigned char)buffer[i])) {
      fprintf(stderr, "Erro de sintaxe: caractere invalido '%c' na posicao %zu\n", buffer[i], i);
      return EXIT_FAILURE;
    }
  }

  errno = 0;
  strtoull(buffer, NULL, 10);
  if (errno == ERANGE) {
    fprintf(stderr, "Erro de sintaxe: constante '%s' eh muito grande para caber em 64 bits\n", buffer);
    return EXIT_FAILURE;
  }

  const char *ponto = strrchr(arquivo_entrada, '.');
  size_t base_len = (ponto != NULL) ? (size_t)(ponto - arquivo_entrada) : strlen(arquivo_entrada);

  char arquivo_saida[512];
  int n = snprintf(arquivo_saida, sizeof(arquivo_saida), "%.*s.s", (int)base_len, arquivo_entrada);
  if (n < 0 || (size_t)n >= sizeof(arquivo_saida)) {
    fprintf(stderr, "Erro: nome do arquivo de saida muito longo\n");
    return EXIT_FAILURE;
  }

  FILE *fp_saida = fopen(arquivo_saida, "w");
  if (fp_saida == NULL) {
    fprintf(stderr, "Erro: nao foi possivel criar '%s'\n", arquivo_saida);
    return EXIT_FAILURE;
  }

  fprintf(fp_saida,
          "#\n"
          "# model de saída para o compilador\n"
          "#\n"
          "\n"
          ".section .text\n"
          ".globl _start\n"
          "\n"
          "_start:\n"
          "    mov $%s, %%rax\n"
          "\n"
          "    call imprime_num\n"
          "    call sair\n"
          "\n"
          ".include \"runtime.s\"\n",
          buffer);

  fclose(fp_saida);

  printf("Arquivo de saida: %s\n", arquivo_saida);

  return EXIT_SUCCESS;
}