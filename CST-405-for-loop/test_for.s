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
    # Declared 'sum' at offset 4
    li $t0, 0         # sum = 0 (constant)
    sw $t0, 4($sp)     # Store to 'sum'
    li $t1, 1         # i = 1 (constant)
    sw $t1, 0($sp)     # Store to 'i'
L0:                    # Label
    li $t2, 5         # Load constant 5
    sle $t3, $t1, $t2   # t0 = i LE 5
    beqz $t3, L2       # Jump if false
    lw $t1, 0($sp)     # Load variable 'i'
    add $t2, $t0, $t1   # t0 = sum + i
    move $t0, $t2       # sum = t0
    sw $t0, 4($sp)     # Store to 'sum'
L1:                    # Label
    lw $t1, 0($sp)     # Load variable 'i'
    li $t3, 1         # Load constant 1
    add $t2, $t1, $t3   # t0 = i + 1
    move $t1, $t2       # i = t0
    sw $t1, 0($sp)     # Store to 'i'
    j L0              # Unconditional jump
L2:                    # Label
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # End of function main

    # Spill any remaining registers

    # Exit program
    addi $sp, $sp, 400
    li $v0, 10
    syscall
