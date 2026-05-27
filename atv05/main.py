import sys
from lexer import lex
from parser import parse, ErroSintatico
from arvore import desenhar_arvore


def main():
    args = sys.argv[1:]
    mostrar_visual = "--arvore" in args
    args = [a for a in args if a != "--arvore"]

    if len(args) != 1:
        print(f"Uso: {sys.argv[0]} [--arvore] <arquivo.ec1>", file=sys.stderr)
        return 1

    caminho = args[0]
    try:
        with open(caminho, "r") as f:
            fonte = f.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir '{caminho}'", file=sys.stderr)
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
    if mostrar_visual:
        print("Arvore (visual):")
        print(desenhar_arvore(arvore))
    print(f"Valor: {arvore.avaliar()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
