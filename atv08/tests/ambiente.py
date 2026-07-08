import os
import shutil
import subprocess
import sys


def check_tool(name):
    return shutil.which(name) is not None


def running_in_docker():
    return os.path.exists("/.dockerenv")


def has_gnu_as():
    if not check_tool("as"):
        return False
    try:
        res = subprocess.run(["as", "--version"], capture_output=True, text=True)
    except OSError:
        return False
    saida = (res.stdout + res.stderr).lower()
    return "gnu assembler" in saida


def can_run_linux_binaries():
    return sys.platform.startswith("linux") and os.uname().machine == "x86_64"


def run_with_docker():
    if not check_tool("docker"):
        print("Docker nao encontrado.")
        return 1

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
