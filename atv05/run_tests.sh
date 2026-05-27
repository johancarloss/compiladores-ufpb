#!/bin/sh

set -u

PROG="main.py"
TEST_DIR="tests"
TMP_DIR="${TMPDIR:-/tmp}/atv05-tests.$$"
FAILURES=0
TOTAL=0

mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT HUP INT TERM

if [ ! -d "$TEST_DIR" ]; then
    echo "Diretorio de testes nao encontrado: $TEST_DIR"
    exit 1
fi

for input in "$TEST_DIR"/*.ec1; do
    [ -e "$input" ] || continue

    TOTAL=$((TOTAL + 1))
    base=${input%.ec1}
    name=${base##*/}
    expected="$base.out"
    actual="$TMP_DIR/$name.actual"

    echo "== $name =="
    echo "input: $input"
    echo "expected: $expected"

    if [ ! -f "$expected" ]; then
        echo "FAIL"
        echo "  arquivo esperado nao encontrado: $expected"
        echo
        FAILURES=$((FAILURES + 1))
        continue
    fi

    python3 "$PROG" "$input" > "$actual"

    if cmp -s "$expected" "$actual"; then
        echo "PASS"
    else
        echo "FAIL"
        FAILURES=$((FAILURES + 1))
    fi

    echo
done

if [ "$TOTAL" -eq 0 ]; then
    echo "Nenhum teste encontrado em $TEST_DIR"
    exit 1
fi

echo
echo "$TOTAL teste(s), $FAILURES falha(s)"

[ "$FAILURES" -eq 0 ]
