import os
import shutil
import subprocess
import sys


def check_tool(name):
    """Verifica se uma ferramenta esta disponivel no PATH."""
    return shutil.which(name) is not None


def has_gnu_as():
    """Retorna True quando o assembler disponivel aceita opcoes GNU."""
    if not check_tool("as"):
        return False
    try:
        res = subprocess.run(["as", "--version"], capture_output=True, text=True)
    except OSError:
        return False
    saida = (res.stdout + res.stderr).lower()
    return "gnu assembler" in saida


def running_in_docker():
    return os.path.exists("/.dockerenv")


def can_run_linux_binaries():
    return sys.platform.startswith("linux") and os.uname().machine == "x86_64"


def run_with_docker():
    if not check_tool("docker"):
        print("GNU as nao disponivel localmente e Docker nao encontrado.", file=sys.stderr)
        return 1

    print("GNU as nao disponivel localmente. Executando testes via Docker.", flush=True)
    try:
        subprocess.run(
            ["docker", "build", "--platform", "linux/amd64", "-t", "atv08-comp", "."],
            check=True,
        )
        subprocess.run(
            ["docker", "run", "--rm", "--platform", "linux/amd64", "atv08-comp"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0


def preparar_diretorio_testes():
    tests_dir = os.path.join("tests", "out")
    os.makedirs(tests_dir, exist_ok=True)

    if os.path.exists("runtime.s"):
        shutil.copy("runtime.s", os.path.join(tests_dir, "runtime.s"))
    else:
        print("Aviso: runtime.s nao encontrado no diretorio atual.", file=sys.stderr)

    return tests_dir
