"""
Verificacao da Congruencia de Zeller.

Calcula o dia da semana usando a formula:
    h = (q + floor(13(m+1)/5) + k + floor(k/4) + floor(j/4) - 2j) mod 7

Variaveis:
    q = dia do mes
    m = mes ajustado (3=marco, ..., 12=dez, 13=jan, 14=fev)
    k = ano dentro do seculo
    j = seculo
    h = 0=sabado, 1=domingo, 2=segunda, ..., 6=sexta

Este programa serve como referencia para validar o resultado do
programa assembly zeller.s.
"""


def zeller(q: int, m: int, k: int, j: int) -> int:
    """
    Implementa a formula direta da congruencia de Zeller.
    Recebe os valores ja ajustados (mesmo formato dos registradores
    R8, R9, R10, R11 do programa assembly).
    """
    return (q + (13 * (m + 1)) // 5 + k + k // 4 + j // 4 - 2 * j) % 7


def dia_da_semana(dia: int, mes: int, ano: int) -> int:
    """
    Wrapper que aceita uma data normal (dia/mes/ano) e faz o
    ajuste padrao de janeiro/fevereiro antes de chamar zeller().

    Janeiro e fevereiro contam como meses 13 e 14 do ano anterior.
    """
    if mes < 3:
        mes += 12
        ano -= 1
    q = dia
    m = mes
    k = ano % 100
    j = ano // 100
    return zeller(q, m, k, j)


DIAS = ["sabado", "domingo", "segunda", "terca",
        "quarta", "quinta", "sexta"]


def main() -> None:
    # Casos de teste: (descricao, dia, mes, ano, h esperado)
    testes = [
        ("17/maio/2026",      17,  5, 2026, 1),  # domingo
        ("01/janeiro/2024",    1,  1, 2024, 2),  # segunda
        ("25/dezembro/2026",  25, 12, 2026, 6),  # sexta (Natal)
        ("14/fevereiro/2024", 14,  2, 2024, 4),  # quarta
        ("23/abril/2026",     23,  4, 2026, 5),  # quinta
        ("29/fevereiro/2024", 29,  2, 2024, 5),  # quinta (ano bissexto)
        ("01/janeiro/2000",    1,  1, 2000, 0),  # sabado
    ]

    print(f"{'Data':<22} {'h':>2}  {'Dia':<10} {'Esperado':<10} {'Status'}")
    print("-" * 65)

    todos_ok = True
    for descricao, d, mes, ano, esperado in testes:
        h = dia_da_semana(d, mes, ano)
        ok = (h == esperado)
        status = "OK" if ok else "FALHOU"
        if not ok:
            todos_ok = False
        print(f"{descricao:<22} {h:>2}  {DIAS[h]:<10} "
              f"{esperado} ({DIAS[esperado]:<7}) {status}")

    print()
    if todos_ok:
        print("Todos os testes passaram.")
    else:
        print("Algum teste falhou — verificar formula.")


if __name__ == "__main__":
    main()
