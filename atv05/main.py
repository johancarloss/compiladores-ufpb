import sys
from lexer import lex
from parser import parse, ErroSintatico


def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <arquivo.ec1>", file=sys.stderr)
        return 1

    try:
        with open(sys.argv[1], "r") as f:
            fonte = f.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir '{sys.argv[1]}'", file=sys.stderr)
        return 1

    lx = lex(fonte)
    if lx.houve_erro:
        print(f"Erro léxico na posição {lx.erro_pos}: "
              f"caractere inválido '{lx.erro_char}'")
        return 1

    try:
        arvore = parse(lx.tokens)
    except ErroSintatico as e:
        print(f"Erro sintático: {e}")
        return 1

    print(f"Arvore: {arvore}")
    print(f"Valor: {arvore.avaliar()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
