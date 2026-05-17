# Construção de Compiladores — UFPB P6 (2026.1)

Repositório das atividades da disciplina **Construção de Compiladores** do curso de Ciência da Computação (UFPB).

**Professor:** Andrei Formiga

---

## Sobre a disciplina

As atividades desta disciplina são **incrementais**: cada uma estende a linguagem implementada na anterior. Começamos com constantes inteiras (Atividade 02), seguimos com expressões aritméticas, variáveis, controle de fluxo, funções, e assim por diante.

Este repositório serve como **base única** para essa evolução. Ao final do semestre, o compilador resultante é o **projeto consolidado da disciplina**, fruto da junção e refinamento das partes desenvolvidas em cada atividade.

---

## Atividades

| # | Tema | Pasta |
|---|---|---|
| 01 | Questionário inicial (compilador vs interpretador, por que estudar compiladores) | [`atv01/`](atv01/) |
| 02 | Compilador CI — Constantes Inteiras (C → assembly x86-64 GAS) | [`atv02/`](atv02/) |

À medida que novas atividades forem lançadas, vão sendo adicionadas como `atv03/`, `atv04/`, etc.

---

## Estrutura do repositório

```
.
├── README.md          # este arquivo
├── .gitignore         # ignora binários, objetos, artefatos de build
├── docs/              # transcrições e referências dos enunciados
└── atvNN/             # uma pasta por atividade — código + README próprio
```

Cada pasta `atvNN/` é independente: tem seu próprio `README.md`, `Makefile` (quando aplicável), código-fonte e testes. Para detalhes de compilação/execução de cada atividade, leia o README dentro da pasta.

---

## Autores

- Johan Carlos
- Luiz Augusto
- Diego de Carvalho
- Gabriel Lizst
