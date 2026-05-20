# Atividade 03 — Congruência de Zeller

Programa assembly x86-64 que calcula o **dia da semana** para qualquer data, usando a **congruência de Zeller**.

Diferente das atividades anteriores, esta não envolve um compilador — o programa assembly é escrito **diretamente à mão**.

**Disciplina:** Construção de Compiladores (UFPB — P6 — 2026.1)
**Professor:** Andrei Formiga
**Atividade:** 03

---

## Estrutura

```
zeller.s        # programa assembly x86-64 (Parte 1)
zeller.py       # programa de verificação em Python (Parte 1)
respostas.md    # respostas das 3 perguntas teóricas (Parte 2)
Makefile        # automação de build/teste
README.md       # este arquivo
```

## Como compilar e executar (Parte 1)

```bash
make            # monta e linka zeller.s
make test       # roda zeller (assembly) e zeller.py (referência) e compara
make clean      # limpa artefatos
```

## A fórmula

```
h = (q + floor(13(m+1)/5) + k + floor(k/4) + floor(j/4) - 2j) mod 7
```

| Variável | Significado | Registrador |
|---|---|---|
| `q` | Dia do mês | R8 |
| `m` | Mês (3=março, ..., 12=dez, 13=jan, 14=fev) | R9 |
| `k` | Ano dentro do século (ex: 26 pra 2026) | R10 |
| `j` | Século (ex: 20 pra 2026) | R11 |
| `h` | Resultado: 0=sáb, 1=dom, ..., 6=sex | RAX |

**Atenção:** janeiro/fevereiro devem usar `m = 13/14` E o ano deve ser tratado como o anterior (ex: jan/fev 2024 → `j=20, k=23`).

Especificação completa: [`../docs/atividade-03-especificacao.md`](../docs/atividade-03-especificacao.md).

## Parte 2 — Perguntas teóricas

Respostas em [`respostas.md`](respostas.md).

## Autores

- Johan Carlos
- Luiz Augusto
- Diego de Carvalho
- Gabriel Lizst
