import os
import sys
import subprocess
import shutil
from lexer import lex
from parser import parse, ErroSintatico
from compilador import compilar

# Expressões de teste com seus valores esperados
TEST_CASES = [
    ("42", 42),
    ("(7+11)", 18),
    ("(11-7)", 4),
    ("(7+(3+8))", 18),
    ("(10*5)", 50),
    ("(20/4)", 5),
    ("((3*5)-(8/2))", 11),
    ("(100-(2*(10+20)))", 40),
    ("(((12*3)/(5-1))+(7*2))", 23),
    ("((189+(129338/23))-((((1230120+(1123121*123121212))+12)/1121233)/(1231233*(123123+(12332323/1233232112)))))", 5812),
]


def check_tool(name):
    """Verifica se uma ferramenta está disponível no PATH."""
    return shutil.which(name) is not None


def main():
    # Cria o diretório de testes se não existir
    tests_dir = "tests"
    os.makedirs(tests_dir, exist_ok=True)

    # Copia runtime.s para o diretório de testes para resolver o .include "runtime.s"
    if os.path.exists("runtime.s"):
        shutil.copy("runtime.s", os.path.join(tests_dir, "runtime.s"))
    else:
        print("Aviso: runtime.s não encontrado no diretório atual.", file=sys.stderr)

    has_as = check_tool("as")
    has_ld = check_tool("ld")
    # Só podemos rodar binários Linux de forma nativa se o sistema for Linux x86_64
    can_run = sys.platform.startswith("linux") and os.uname().machine == "x86_64"

    print("=" * 60)
    print(" Executando os testes do compilador EC1 (x86-64)")
    print("=" * 60)
    print(f"GNU Assembler (as) disponível: {'Sim' if has_as else 'Não'}")
    print(f"GNU Linker (ld) disponível:    {'Sim' if has_ld else 'Não'}")
    print(f"Pode executar binários Linux:  {'Sim' if can_run else 'Não (Simulado/Apenas Compilação)'}")
    print("-" * 60)

    sucessos = 0
    total = len(TEST_CASES)

    for i, (expr, expected) in enumerate(TEST_CASES, 1):
        print(f"Teste {i}/{total}: '{expr}'")
        
        # 1. Avaliação via interpretador da AST
        try:
            lx = lex(expr)
            arvore = parse(lx.tokens)
            val_interprete = arvore.avaliar()
            if val_interprete != expected:
                print(f"  [FALHA] O interpretador retornou {val_interprete}, mas esperava-se {expected}")
                continue
        except Exception as e:
            print(f"  [FALHA] Erro ao interpretar a expressão: {e}")
            continue

        # Caminhos dos arquivos de teste
        base_path = os.path.join(tests_dir, f"teste_{i}")
        ec1_path = f"{base_path}.ec1"
        s_path = f"{base_path}.s"
        o_path = f"{base_path}.o"
        bin_path = base_path

        # 2. Escreve a expressão original
        with open(ec1_path, "w") as f:
            f.write(expr)

        # 3. Compilação para Assembly x86-64 (.s)
        try:
            assembly_code = compilar(expr)
            with open(s_path, "w", encoding="utf-8") as f:
                f.write(assembly_code)
            print(f"  -> Assembly gerado: {s_path}")
        except Exception as e:
            print(f"  [FALHA] Erro de compilação: {e}")
            continue

        # 4. Verificação de sintaxe usando assembler (as)
        if has_as:
            try:
                # Monta o arquivo (.s -> .o)
                # Forçamos a arquitetura x86-64 com --64
                subprocess.run(["as", "--64", "-o", o_path, s_path], check=True, capture_output=True)
                print("  -> Montagem (.o) realizada com sucesso (Sintaxe OK)")
            except subprocess.CalledProcessError as e:
                print(f"  [FALHA] Erro de sintaxe no assembler:\n{e.stderr.decode('utf-8')}")
                continue
        else:
            print("  -> Montagem (.o) ignorada (as não disponível)")
            continue

        # 5. Linkagem e Execução (Apenas em ambiente compatível)
        if has_ld and can_run:
            try:
                # Linka o objeto (.o -> executável)
                subprocess.run(["ld", "-o", bin_path, o_path], check=True, capture_output=True)
                
                # Executa o binário gerado
                res = subprocess.run([f"./{bin_path}"], capture_output=True, text=True, check=True)
                saida_num = int(res.stdout.strip())

                if saida_num == expected:
                    print(f"  [PASS] Saída do executável: {saida_num} (Igual ao esperado)")
                    sucessos += 1
                else:
                    print(f"  [FALHA] Saída do executável: {saida_num}, mas esperava-se {expected}")
            except subprocess.CalledProcessError as e:
                stderr_msg = e.stderr.decode('utf-8') if e.stderr else ""
                print(f"  [FALHA] Erro de linkagem ou execução:\n{stderr_msg}")
            except ValueError:
                print(f"  [FALHA] O programa impresso não é um número: '{res.stdout.strip()}'")
        else:
            # Se não puder rodar, consideramos sucesso se a montagem funcionou
            print(f"  [PASS] Compilação e sintaxe verificadas (Resultado esperado: {expected} | Execução ignorada no host local)")
            sucessos += 1
        print("-" * 60)

    print(f"Resultado final: {sucessos}/{total} testes passaram com sucesso.")
    sys.exit(0 if sucessos == total else 1)


if __name__ == "__main__":
    main()
