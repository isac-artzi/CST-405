.data

.text
.globl main
main:
    # Allocate stack space
    addi $sp, $sp, -400
    j main_start       # Jump to main function


# Function: main
main_start:
    # Declared 'i' at offset 0
    # Declared 'j' at offset 4
    # Declared 'product' at offset 8
    li $t0, 1         # i = 1 (constant)
    sw $t0, 0($sp)     # Store to 'i'
L0:                    # Label
    li $t1, 3         # Load constant 3
    sle $t2, $t0, $t1   # t0 = i LE 3
    beqz $t2, L2       # Jump if false
    li $t0, 1         # j = 1 (constant)
    sw $t0, 4($sp)     # Store to 'j'
L3:                    # Label
    li $t1, 3         # Load constant 3
    sle $t2, $t0, $t1   # t0 = j LE 3
    beqz $t2, L5       # Jump if false
    lw $t0, 0($sp)     # Load variable 'i'
    lw $t1, 4($sp)     # Load variable 'j'
    mul $t2, $t0, $t1   # t0 = i MUL j
    move $t0, $t2       # product = t0
    sw $t0, 8($sp)     # Store to 'product'
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
L4:                    # Label
    lw $t0, 4($sp)     # Load variable 'j'
    li $t1, 1         # Load constant 1
    add $t2, $t0, $t1   # t0 = j + 1
    move $t0, $t2       # j = t0
    sw $t0, 4($sp)     # Store to 'j'
    j L3              # Unconditional jump
L5:                    # Label
L1:                    # Label
    lw $t1, 0($sp)     # Load variable 'i'
    li $t3, 1         # Load constant 1
    add $t2, $t1, $t3   # t0 = i + 1
    move $t1, $t2       # i = t0
    sw $t1, 0($sp)     # Store to 'i'
    j L0              # Unconditional jump
L2:                    # Label
    # End of function main

    # Spill any remaining registers

    # Exit program
    addi $sp, $sp, 400
    li $v0, 10
    syscall
