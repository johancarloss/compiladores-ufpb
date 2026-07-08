import os
import shutil
import subprocess

from compilador import compilar
from tests.ambiente import can_run_linux_binaries, check_tool, has_gnu_as


GERACAO_TEXTUAL = [
    (
        "resultado constante",
        "= 42",
        [
            ".section .text",
            "mov $42, %rax",
            "call imprime_num",
            "call sair",
        ],
    ),
    (
        "declara variavel na bss e salva valor",
        "x = 10;\n= x",
        [
            ".section .bss",
            ".lcomm x, 8",
            ".section .text",
            "mov $10, %rax",
            "mov %rax, x",
            "mov x, %rax",
        ],
    ),
    (
        "declara duas variaveis e preserva ordem",
        "x = 10;\ny = x + 2;\n= y * 3",
        [
            ".lcomm x, 8",
            ".lcomm y, 8",
            "mov %rax, x",
            "mov x, %rax",
            "mov %rax, y",
            "mov y, %rax",
        ],
    ),
]

GERACAO_EXECUCAO = [
    ("resultado constante", "= 42", 42),
    ("variaveis e expressao final", "x = 10;\ny = x + 2;\n= y * 3", 36),
]


def executar_testes_geracao():
    print("[Geracao]")
    sucessos = 0
    total = len(GERACAO_TEXTUAL)

    for nome, fonte, trechos in GERACAO_TEXTUAL:
        print(f"Geracao textual: {nome}")
        try:
            assembly = compilar(fonte)
            verificar_trechos(assembly, trechos)
        except Exception as e:
            print(f"  [FALHA] {e}")
        else:
            print("  [PASS]")
            sucessos += 1
        print("-" * 60)

    if pode_executar_assembly():
        for nome, fonte, esperado in GERACAO_EXECUCAO:
            total += 1
            print(f"Geracao executavel: {nome}")
            try:
                saida = compilar_montar_e_executar(nome, fonte)
                assert saida == esperado, f"saida {saida}, esperado {esperado}"
            except Exception as e:
                print(f"  [FALHA] {e}")
            else:
                print(f"  [PASS] Saida do executavel: {saida}")
                sucessos += 1
            print("-" * 60)
    else:
        print("Geracao executavel: ignorada (GNU as/ld/Linux x86-64 indisponivel)")
        print("-" * 60)

    print(f"[Geracao] Resultado: {sucessos}/{total}")
    print("-" * 60)
    return sucessos, total


def verificar_trechos(assembly, trechos):
    for trecho in trechos:
        assert trecho in assembly, f"assembly nao contem: {trecho}"


def pode_executar_assembly():
    return has_gnu_as() and check_tool("ld") and can_run_linux_binaries()


def compilar_montar_e_executar(nome, fonte):
    out_dir = os.path.join("tests", "out")
    os.makedirs(out_dir, exist_ok=True)

    if os.path.exists("runtime.s"):
        shutil.copy("runtime.s", os.path.join(out_dir, "runtime.s"))

    base = normalizar_nome(nome)
    ev_path = os.path.join(out_dir, f"{base}.ev")
    s_path = os.path.join(out_dir, f"{base}.s")
    o_path = os.path.join(out_dir, f"{base}.o")
    bin_path = os.path.join(out_dir, base)

    with open(ev_path, "w", encoding="utf-8") as f:
        f.write(fonte)

    assembly = compilar(fonte)
    with open(s_path, "w", encoding="utf-8") as f:
        f.write(assembly)

    subprocess.run(["as", "--64", "-o", o_path, s_path], check=True, capture_output=True)
    subprocess.run(["ld", "-o", bin_path, o_path], check=True, capture_output=True)
    res = subprocess.run([f"./{bin_path}"], check=True, capture_output=True, text=True)
    return int(res.stdout.strip())


def normalizar_nome(nome):
    return nome.replace(" ", "_").replace("-", "_")
