.data

.text
.globl main
main:
    # Allocate stack space
    addi $sp, $sp, -400
    j main_start       # Jump to main function


# Function: grade
func_grade:
    # Save return address and allocate local stack frame
    # Parameter 'score' at offset 0
    sw $a0, 0($sp)     # Store parameter 'score'
    # Declared '__sw0' at offset 4
    lw $t0, 0($sp)     # Load variable 'score'
    move $t1, $t0       # __sw0 = score
    sw $t1, 4($sp)     # Store to '__sw0'
    li $t2, 1         # Load constant 1
    seq $t3, $t1, $t2   # t0 = __sw0 EQ 1
    beqz $t3, L6       # If false, jump to L6
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L0              # Unconditional jump
L6:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 4($sp)     # Load variable '__sw0'
    li $t1, 2         # Load constant 2
    seq $t2, $t0, $t1   # t0 = __sw0 EQ 2
    beqz $t2, L7       # If false, jump to L7
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L1              # Unconditional jump
L7:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 4($sp)     # Load variable '__sw0'
    li $t1, 3         # Load constant 3
    seq $t2, $t0, $t1   # t0 = __sw0 EQ 3
    beqz $t2, L4       # If false, jump to L4
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L2              # Unconditional jump
L4:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L3              # Unconditional jump
L0:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 10         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
L1:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 20         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
L2:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 30         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
L3:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 99         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
L5:                    # Label / merge point
    # Invalidate register state at merge point
    # End of function grade
    # Restore and return
    jr $ra

# Function: main
main_start:
    # Declared 'x' at offset 0
    li $t0, 2         # x = 2 (constant)
    sw $t0, 0($sp)     # Store to 'x'
    # Declared '__sw8' at offset 4
    move $t1, $t0       # __sw8 = x
    sw $t1, 4($sp)     # Store to '__sw8'
    li $t2, 1         # Load constant 1
    seq $t3, $t1, $t2   # t0 = __sw8 EQ 1
    beqz $t3, L14       # If false, jump to L14
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L8              # Unconditional jump
L14:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 4($sp)     # Load variable '__sw8'
    li $t1, 2         # Load constant 2
    seq $t2, $t0, $t1   # t0 = __sw8 EQ 2
    beqz $t2, L15       # If false, jump to L15
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L9              # Unconditional jump
L15:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 4($sp)     # Load variable '__sw8'
    li $t1, 3         # Load constant 3
    seq $t2, $t0, $t1   # t0 = __sw8 EQ 3
    beqz $t2, L12       # If false, jump to L12
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L10              # Unconditional jump
L12:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L11              # Unconditional jump
L8:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 10         # Load constant 10 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L13              # Unconditional jump
L9:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 20         # Load constant 20 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L13              # Unconditional jump
L10:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 30         # Load constant 30 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L13              # Unconditional jump
L11:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L13              # Unconditional jump
L13:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 99         # x = 99 (constant)
    sw $t0, 0($sp)     # Store to 'x'
    # Declared '__sw16' at offset 8
    move $t1, $t0       # __sw16 = x
    sw $t1, 8($sp)     # Store to '__sw16'
    li $t2, 1         # Load constant 1
    seq $t3, $t1, $t2   # t0 = __sw16 EQ 1
    beqz $t3, L21       # If false, jump to L21
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L16              # Unconditional jump
L21:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 8($sp)     # Load variable '__sw16'
    li $t1, 2         # Load constant 2
    seq $t2, $t0, $t1   # t0 = __sw16 EQ 2
    beqz $t2, L19       # If false, jump to L19
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L17              # Unconditional jump
L19:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L18              # Unconditional jump
L16:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 10         # Load constant 10 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L20              # Unconditional jump
L17:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 20         # Load constant 20 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L20              # Unconditional jump
L18:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L20              # Unconditional jump
L20:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 3         # x = 3 (constant)
    sw $t0, 0($sp)     # Store to 'x'
    # Declared '__sw22' at offset 12
    move $t1, $t0       # __sw22 = x
    sw $t1, 12($sp)     # Store to '__sw22'
    li $t2, 3         # Load constant 3
    seq $t3, $t1, $t2   # t0 = __sw22 EQ 3
    beqz $t3, L27       # If false, jump to L27
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L22              # Unconditional jump
L27:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 12($sp)     # Load variable '__sw22'
    li $t1, 4         # Load constant 4
    seq $t2, $t0, $t1   # t0 = __sw22 EQ 4
    beqz $t2, L25       # If false, jump to L25
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L23              # Unconditional jump
L25:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L24              # Unconditional jump
L22:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 30         # Load constant 30 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L26              # Unconditional jump
L23:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 40         # Load constant 40 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L26              # Unconditional jump
L24:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L26              # Unconditional jump
L26:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 4         # x = 4 (constant)
    sw $t0, 0($sp)     # Store to 'x'
    # Declared '__sw28' at offset 16
    move $t1, $t0       # __sw28 = x
    sw $t1, 16($sp)     # Store to '__sw28'
    li $t2, 4         # Load constant 4
    seq $t3, $t1, $t2   # t0 = __sw28 EQ 4
    beqz $t3, L33       # If false, jump to L33
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L28              # Unconditional jump
L33:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 16($sp)     # Load variable '__sw28'
    li $t1, 5         # Load constant 5
    seq $t2, $t0, $t1   # t0 = __sw28 EQ 5
    beqz $t2, L31       # If false, jump to L31
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L29              # Unconditional jump
L31:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L30              # Unconditional jump
L28:                    # Label / merge point
    # Invalidate register state at merge point
L29:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 10         # Load constant 10 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L32              # Unconditional jump
L30:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L32              # Unconditional jump
L32:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 15         # x = 15 (constant)
    sw $t0, 0($sp)     # Store to 'x'
    # Declared 'd' at offset 20
    li $t1, 10         # Load constant 10
    div $t0, $t1      # Division
    mflo $t2           # t0 = x / 10
    move $t0, $t2       # d = t0
    sw $t0, 20($sp)     # Store to 'd'
    # Declared '__sw34' at offset 24
    move $t1, $t0       # __sw34 = d
    sw $t1, 24($sp)     # Store to '__sw34'
    li $t3, 0         # Load constant 0
    seq $t2, $t1, $t3   # t0 = __sw34 EQ 0
    beqz $t2, L40       # If false, jump to L40
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L34              # Unconditional jump
L40:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 24($sp)     # Load variable '__sw34'
    li $t1, 1         # Load constant 1
    seq $t2, $t0, $t1   # t0 = __sw34 EQ 1
    beqz $t2, L41       # If false, jump to L41
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L35              # Unconditional jump
L41:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 24($sp)     # Load variable '__sw34'
    li $t1, 2         # Load constant 2
    seq $t2, $t0, $t1   # t0 = __sw34 EQ 2
    beqz $t2, L38       # If false, jump to L38
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L36              # Unconditional jump
L38:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L37              # Unconditional jump
L34:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L39              # Unconditional jump
L35:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 1         # Load constant 1 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L39              # Unconditional jump
L36:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 2         # Load constant 2 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L39              # Unconditional jump
L37:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 9         # Load constant 9 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L39              # Unconditional jump
L39:                    # Label / merge point
    # Invalidate register state at merge point
    # Declared 'g' at offset 28
    # Argument: 3
    # Call function grade with 1 arguments
    li $a0, 3
    jal func_grade
    move $t0, $v0      # Get return value
    move $t1, $t0       # g = t0
    sw $t1, 28($sp)     # Store to 'g'
    # Declared '__sw42' at offset 32
    move $t2, $t1       # __sw42 = g
    sw $t2, 32($sp)     # Store to '__sw42'
    li $t3, 30         # Load constant 30
    seq $t0, $t2, $t3   # t0 = __sw42 EQ 30
    beqz $t0, L44       # If false, jump to L44
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L42              # Unconditional jump
L44:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L43              # Unconditional jump
L42:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 7         # Load constant 7 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L45              # Unconditional jump
L43:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L45              # Unconditional jump
L45:                    # Label / merge point
    # Invalidate register state at merge point
    # Declared 'outer' at offset 36
    # Declared 'inner' at offset 40
    li $t0, 2         # outer = 2 (constant)
    sw $t0, 36($sp)     # Store to 'outer'
    li $t1, 10         # inner = 10 (constant)
    sw $t1, 40($sp)     # Store to 'inner'
    # Declared '__sw46' at offset 44
    move $t2, $t0       # __sw46 = outer
    sw $t2, 44($sp)     # Store to '__sw46'
    li $t3, 1         # Load constant 1
    seq $t4, $t2, $t3   # t0 = __sw46 EQ 1
    beqz $t4, L51       # If false, jump to L51
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L46              # Unconditional jump
L51:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 44($sp)     # Load variable '__sw46'
    li $t1, 2         # Load constant 2
    seq $t2, $t0, $t1   # t0 = __sw46 EQ 2
    beqz $t2, L49       # If false, jump to L49
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L47              # Unconditional jump
L49:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L48              # Unconditional jump
L46:                    # Label / merge point
    # Invalidate register state at merge point
    # Declared '__sw52' at offset 48
    lw $t0, 40($sp)     # Load variable 'inner'
    move $t1, $t0       # __sw52 = inner
    sw $t1, 48($sp)     # Store to '__sw52'
    li $t2, 10         # Load constant 10
    seq $t3, $t1, $t2   # t0 = __sw52 EQ 10
    beqz $t3, L54       # If false, jump to L54
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L52              # Unconditional jump
L54:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L53              # Unconditional jump
L52:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 100         # Load constant 100 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L55              # Unconditional jump
L53:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L55              # Unconditional jump
L55:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L50              # Unconditional jump
L47:                    # Label / merge point
    # Invalidate register state at merge point
    # Declared '__sw56' at offset 52
    lw $t0, 40($sp)     # Load variable 'inner'
    move $t1, $t0       # __sw56 = inner
    sw $t1, 52($sp)     # Store to '__sw56'
    li $t2, 10         # Load constant 10
    seq $t3, $t1, $t2   # t0 = __sw56 EQ 10
    beqz $t3, L58       # If false, jump to L58
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L56              # Unconditional jump
L58:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L57              # Unconditional jump
L56:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 200         # Load constant 200 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L59              # Unconditional jump
L57:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L59              # Unconditional jump
L59:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L50              # Unconditional jump
L48:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # Load constant 0 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Spill all live registers before branch
    j L50              # Unconditional jump
L50:                    # Label / merge point
    # Invalidate register state at merge point
    # Declared 'i' at offset 56
    li $t0, 0         # i = 0 (constant)
    sw $t0, 56($sp)     # Store to 'i'
    # Declared '__sw60' at offset 60
    move $t1, $t0       # __sw60 = i
    sw $t1, 60($sp)     # Store to '__sw60'
    li $t2, 0         # Load constant 0
    seq $t3, $t1, $t2   # t0 = __sw60 EQ 0
    beqz $t3, L62       # If false, jump to L62
    # Spill all live registers before branch
    # Spill all live registers before branch
    j L60              # Unconditional jump
L62:                    # Label / merge point
    # Invalidate register state at merge point
    # Spill all live registers before branch
    j L61              # Unconditional jump
L60:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 1         # i = 1 (constant)
    sw $t0, 56($sp)     # Store to 'i'
    # Spill all live registers before branch
    j L63              # Unconditional jump
L61:                    # Label / merge point
    # Invalidate register state at merge point
    li $t0, 0         # i = 0 (constant)
    sw $t0, 56($sp)     # Store to 'i'
    # Spill all live registers before branch
    j L63              # Unconditional jump
L63:                    # Label / merge point
    # Invalidate register state at merge point
    lw $t0, 56($sp)     # Load variable 'i' for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t0, 0         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function main

    # Spill any remaining registers

    # Exit program
    addi $sp, $sp, 400
    li $v0, 10
    syscall
