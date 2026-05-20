# zeller.s
# Calcula a Congruencia de Zeller para uma data fixa.
# Para testar outras datas, modificar os valores iniciais de R8, R9, R10, R11.
#
# Formula:
#   h = (q + floor(13(m+1)/5) + k + floor(k/4) + floor(j/4) - 2j) mod 7
#
# Entradas (registradores):
#   R8  = q  (dia do mes)
#   R9  = m  (mes ajustado, 3..14)
#   R10 = k  (ano dentro do seculo)
#   R11 = j  (seculo)
#
# Saida:
#   RAX = h  (0=sabado, 1=domingo, 2=segunda, ..., 6=sexta)
#
# Como ler o resultado:
#   ./zeller
#   echo $?       # imprime h
#
# Exemplo: 17/maio/2026 -> q=17, m=5, k=26, j=20 -> h=1 (domingo)

    .section .text
    .globl _start

_start:
    # ===== Carregar valores de teste =====
    # 17/maio/2026 (esperado: h=1, domingo)
    mov $17, %r8                # q  = 17
    mov $5,  %r9                # m  = 5  (maio)
    mov $26, %r10               # k  = 26 (2026 dentro do seculo)
    mov $20, %r11               # j  = 20 (seculo)

    # ===== Passo 1: rbx = floor(13*(m+1) / 5) =====
    mov %r9,  %rax              # rax = m
    add $1,   %rax              # rax = m + 1
    imul $13, %rax              # rax = 13 * (m+1)
    cqo                         # rdx:rax = sign extend de rax (obrigatorio antes de idiv)
    mov $5,   %rcx              # rcx = 5  (divisor)
    idiv %rcx                   # rax = rax / 5
    mov %rax, %rbx              # rbx = tmp1  (vai virar acumulador)

    # ===== Passo 2: rbx += q =====
    add %r8,  %rbx              # rbx = tmp1 + q

    # ===== Passo 3: rbx += k =====
    add %r10, %rbx              # rbx += k

    # ===== Passo 4: rbx += floor(k / 4) =====
    mov %r10, %rax              # rax = k
    cqo                         # sign extend
    mov $4,   %rcx              # rcx = 4
    idiv %rcx                   # rax = k / 4
    add %rax, %rbx              # rbx += floor(k/4)

    # ===== Passo 5: rbx += floor(j / 4) =====
    mov %r11, %rax              # rax = j
    cqo
    mov $4,   %rcx              # rcx = 4
    idiv %rcx                   # rax = j / 4
    add %rax, %rbx              # rbx += floor(j/4)

    # ===== Passo 6: rbx -= 2*j =====
    mov %r11, %rax              # rax = j
    imul $2,  %rax              # rax = 2 * j
    sub %rax, %rbx              # rbx -= 2j

    # ===== Passo 7: h = rbx mod 7 =====
    mov %rbx, %rax              # rax = soma total
    cqo                         # sign extend
    mov $7,   %rcx              # rcx = 7
    idiv %rcx                   # rax = quociente (descartado), rdx = resto = h
    mov %rdx, %rax              # rax = h (resultado final)

    # ===== Sair com h como codigo de saida =====
    mov %rax, %rdi              # rdi = h  (argumento de exit)
    mov $60,  %rax              # rax = 60 (syscall exit)
    syscall
