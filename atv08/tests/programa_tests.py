import os
import subprocess

from compilador import compilar
from lexer import lex
from parser import parse


PROGRAM_CASES = [
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
    ("7+5*3", 22),
    ("10-8-2", 0),
    ("100/2/2", 25),
    ("10*5+20/4", 55),
    ("100-2*10+20", 100),
    ("3+4*2/(1-5)", 1),
]


def executar_testes_programa(tests_dir, has_as, has_ld, can_run):
    print("[Programa]")
    sucessos = 0
    total = len(PROGRAM_CASES)

    for i, (expr, expected) in enumerate(PROGRAM_CASES, 1):
        print(f"Programa {i}/{total}: '{expr}'")

        try:
            lx = lex(expr)
            arvore = parse(lx.tokens)
            val_interprete = arvore.avaliar()
            if val_interprete != expected:
                print(f"  [FALHA] O interpretador retornou {val_interprete}, mas esperava-se {expected}")
                print("-" * 60)
                continue
        except Exception as e:
            print(f"  [FALHA] Erro ao interpretar a expressao: {e}")
            print("-" * 60)
            continue

        base_path = os.path.join(tests_dir, f"teste_{i}")
        ev_path = f"{base_path}.ev"
        s_path = f"{base_path}.s"
        o_path = f"{base_path}.o"
        bin_path = base_path

        with open(ev_path, "w") as f:
            f.write(expr)

        try:
            assembly_code = compilar(expr)
            with open(s_path, "w", encoding="utf-8") as f:
                f.write(assembly_code)
            print(f"  -> Assembly gerado: {s_path}")
        except Exception as e:
            print(f"  [FALHA] Erro de compilacao: {e}")
            print("-" * 60)
            continue

        if has_as:
            try:
                subprocess.run(["as", "--64", "-o", o_path, s_path], check=True, capture_output=True)
                print("  -> Montagem (.o) realizada com sucesso (Sintaxe OK)")
            except subprocess.CalledProcessError as e:
                print(f"  [FALHA] Erro de sintaxe no assembler:\n{e.stderr.decode('utf-8')}")
                print("-" * 60)
                continue
        else:
            print("  [FALHA] GNU as nao disponivel")
            print("-" * 60)
            continue

        if has_ld and can_run:
            try:
                subprocess.run(["ld", "-o", bin_path, o_path], check=True, capture_output=True)
                res = subprocess.run([f"./{bin_path}"], capture_output=True, text=True, check=True)
                saida_num = int(res.stdout.strip())

                if saida_num == expected:
                    print(f"  [PASS] Saida do executavel: {saida_num} (Igual ao esperado)")
                    sucessos += 1
                else:
                    print(f"  [FALHA] Saida do executavel: {saida_num}, mas esperava-se {expected}")
            except subprocess.CalledProcessError as e:
                stderr_msg = e.stderr.decode("utf-8") if e.stderr else ""
                print(f"  [FALHA] Erro de linkagem ou execucao:\n{stderr_msg}")
            except ValueError:
                print(f"  [FALHA] O programa impresso nao e um numero: '{res.stdout.strip()}'")
        else:
            print(f"  [PASS] Compilacao e sintaxe verificadas (Resultado esperado: {expected})")
            sucessos += 1
        print("-" * 60)

    print(f"[Programa] Resultado: {sucessos}/{total}")
    print("-" * 60)
    return sucessos, total
