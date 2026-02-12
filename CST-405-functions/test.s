.data

.text
.globl main
main:
    # Allocate stack space
    addi $sp, $sp, -400
    j main_start       # Jump to main function

    # Declared 'globalA' at offset 0
    # Declared 'globalB' at offset 4
    # Declared 'globalC' at offset 8
    # Declared array 'sharedArray[10]' at offset 12 (40 bytes)

# Function: fillNumbers
func_fillNumbers:
    # Save return address and allocate local stack frame
    # Parameter 'output' at offset 0
    sw $a0, 0($sp)     # Store parameter 'output'
    li $t0, 0         # Load index
    li $t1, 100         # Load value
    sll $t2, $t0, 2     # offset = index * 4
    addi $t3, $sp, 0    # addr = sp + base
    add $t3, $t3, $t2  # addr = base + offset
    sw $t1, 0($t3)      # Store to array element
    li $t0, 1         # Load index
    li $t1, 200         # Load value
    sll $t2, $t0, 2     # offset = index * 4
    addi $t3, $sp, 0    # addr = sp + base
    add $t3, $t3, $t2  # addr = base + offset
    sw $t1, 0($t3)      # Store to array element
    li $t0, 2         # Load index
    li $t1, 300         # Load value
    sll $t2, $t0, 2     # offset = index * 4
    addi $t3, $sp, 0    # addr = sp + base
    add $t3, $t3, $t2  # addr = base + offset
    sw $t1, 0($t3)      # Store to array element
    li $t0, 3         # Load return value
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function fillNumbers
    # Restore and return
    jr $ra

# Function: readArray
func_readArray:
    # Save return address and allocate local stack frame
    # Parameter 'input' at offset 0
    sw $a0, 0($sp)     # Store parameter 'input'
    # Declared 'val' at offset 4
    li $t0, 0         # Load index
    sll $t1, $t0, 2
    addi $t2, $sp, 0
    add $t2, $t2, $t1
    lw $t3, 0($t2)
    move $t0, $t3       # val = t0
    sw $t0, 4($sp)     # Store to 'val'
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function readArray
    # Restore and return
    jr $ra

# Function: sumFive
func_sumFive:
    # Save return address and allocate local stack frame
    # Parameter 'a' at offset 0
    sw $a0, 0($sp)     # Store parameter 'a'
    # Parameter 'b' at offset 4
    sw $a1, 4($sp)     # Store parameter 'b'
    # Parameter 'c' at offset 8
    sw $a2, 8($sp)     # Store parameter 'c'
    # Parameter 'd' at offset 12
    sw $a3, 12($sp)     # Store parameter 'd'
    # Parameter 'e' at offset 16
    # Declared 'x' at offset 20
    # Declared 'y' at offset 24
    # Declared 'result' at offset 28
    lw $t0, 0($sp)     # Load variable 'a'
    lw $t1, 4($sp)     # Load variable 'b'
    add $t3, $t0, $t1   # t0 = a + b
    lw $t0, 8($sp)     # Load variable 'c'
    add $t1, $t3, $t0   # t1 = t0 + c
    move $t0, $t1       # x = t1
    sw $t0, 20($sp)     # Store to 'x'
    lw $t2, 12($sp)     # Load variable 'd'
    lw $t3, 16($sp)     # Load variable 'e'
    add $t1, $t2, $t3   # t1 = d + e
    move $t2, $t1       # y = t1
    sw $t2, 24($sp)     # Store to 'y'
    add $t1, $t0, $t2   # t1 = x + y
    move $t0, $t1       # result = t1
    sw $t0, 28($sp)     # Store to 'result'
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function sumFive
    # Restore and return
    jr $ra

# Function: square
func_square:
    # Save return address and allocate local stack frame
    # Parameter 'n' at offset 0
    sw $a0, 0($sp)     # Store parameter 'n'
    # Declared 'result' at offset 4
    move $t0, $t1       # result = t1
    sw $t0, 4($sp)     # Store to 'result'
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function square
    # Restore and return
    jr $ra

# Function: cube
func_cube:
    # Save return address and allocate local stack frame
    # Parameter 'n' at offset 0
    sw $a0, 0($sp)     # Store parameter 'n'
    # Declared 'sq' at offset 4
    # Declared 'result' at offset 8
    # Argument: n
    # Call function square with 1 arguments
    lw $a0, 0($sp)     # Load argument 'n'
    jal func_square
    move $t1, $v0      # Get return value
    move $t0, $t1       # sq = t1
    sw $t0, 4($sp)     # Store to 'sq'
    move $t2, $t1       # result = t1
    sw $t2, 8($sp)     # Store to 'result'
    move $v0, $t2       # Move to return register
    # Return from function
    # End of function cube
    # Restore and return
    jr $ra

# Function: main
main_start:
    # Declared array 'localArray[8]' at offset 0 (32 bytes)
    # Declared array 'resultArray[5]' at offset 32 (20 bytes)
    # Declared 'a' at offset 52
    # Declared 'b' at offset 56
    # Declared 'c' at offset 60
    # Declared 'd' at offset 64
    # Declared 'e' at offset 68
    # Declared 'result' at offset 72
    li $t2, 111         # Load constant 111 for print
    # Print integer
    move $a0, $t2
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t2, 0         # Load index
    li $t3, 10         # Load value
    sll $t4, $t2, 2     # offset = index * 4
    addi $t5, $sp, 0    # addr = sp + base
    add $t5, $t5, $t4  # addr = base + offset
    sw $t3, 0($t5)      # Store to array element
    li $t2, 1         # Load index
    li $t3, 20         # Load value
    sll $t4, $t2, 2     # offset = index * 4
    addi $t5, $sp, 0    # addr = sp + base
    add $t5, $t5, $t4  # addr = base + offset
    sw $t3, 0($t5)      # Store to array element
    li $t2, 2         # Load index
    li $t3, 30         # Load value
    sll $t4, $t2, 2     # offset = index * 4
    addi $t5, $sp, 0    # addr = sp + base
    add $t5, $t5, $t4  # addr = base + offset
    sw $t3, 0($t5)      # Store to array element
    li $t2, 3         # Load index
    li $t3, 40         # Load value
    sll $t4, $t2, 2     # offset = index * 4
    addi $t5, $sp, 0    # addr = sp + base
    add $t5, $t5, $t4  # addr = base + offset
    sw $t3, 0($t5)      # Store to array element
    li $t2, 4         # Load index
    li $t3, 50         # Load value
    sll $t4, $t2, 2     # offset = index * 4
    addi $t5, $sp, 0    # addr = sp + base
    add $t5, $t5, $t4  # addr = base + offset
    sw $t3, 0($t5)      # Store to array element
    li $t2, 0         # Load index
    sll $t3, $t2, 2
    addi $t4, $sp, 0
    add $t4, $t4, $t3
    lw $t1, 0($t4)
    # Print integer
    move $a0, $t1
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 2         # Load index
    sll $t2, $t1, 2
    addi $t3, $sp, 0
    add $t3, $t3, $t2
    lw $t4, 0($t3)
    # Print integer
    move $a0, $t4
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 4         # Load index
    sll $t2, $t1, 2
    addi $t3, $sp, 0
    add $t3, $t3, $t2
    lw $t4, 0($t3)
    # Print integer
    move $a0, $t4
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 222         # Load constant 222 for print
    # Print integer
    move $a0, $t1
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 3         # t1 = 3 (constant)
    li $t2, 3         # Load constant 3
    add $t3, $t1, $t2   # t0 = t1 + 3
    li $t1, 4         # Load constant 4
    add $t2, $t3, $t1   # t1 = t0 + 4
    li $t1, 5         # Load constant 5
    add $t3, $t2, $t1   # t0 = t1 + 5
    move $t1, $t3       # result = t0
    sw $t1, 72($sp)     # Store to 'result'
    # Print integer
    move $a0, $t1
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 333         # Load constant 333 for print
    # Print integer
    move $a0, $t1
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 10         # a = 10 (constant)
    sw $t1, 52($sp)     # Store to 'a'
    li $t2, 20         # b = 20 (constant)
    sw $t2, 56($sp)     # Store to 'b'
    li $t4, 30         # c = 30 (constant)
    sw $t4, 60($sp)     # Store to 'c'
    li $t5, 40         # d = 40 (constant)
    sw $t5, 64($sp)     # Store to 'd'
    li $t6, 50         # e = 50 (constant)
    sw $t6, 68($sp)     # Store to 'e'
    # Argument: a
    # Argument: b
    # Argument: c
    # Argument: d
    # Argument: e
    # Call function sumFive with 5 arguments
    move $a0, $t1      # Pass argument 'a'
    move $a1, $t2      # Pass argument 'b'
    move $a2, $t4      # Pass argument 'c'
    move $a3, $t5      # Pass argument 'd'
    jal func_sumFive
    move $t3, $v0      # Get return value
    move $t7, $t3       # result = t0
    sw $t7, 72($sp)     # Store to 'result'
    # Print integer
    move $a0, $t7
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t7, 444         # Load constant 444 for print
    # Print integer
    move $a0, $t7
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Argument: resultArray
    # Call function fillNumbers with 1 arguments
    lw $a0, 32($sp)     # Load argument 'resultArray'
    jal func_fillNumbers
    move $t3, $v0      # Get return value
    li $t7, 0         # Load index
    sll $t8, $t7, 2
    addi $t9, $sp, 32
    add $t9, $t9, $t8
    lw $t0, 0($t9)
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t0, 1         # Load index
    sll $t7, $t0, 2
    addi $t8, $sp, 32
    add $t8, $t8, $t7
    lw $t9, 0($t8)
    # Print integer
    move $a0, $t9
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t0, 2         # Load index
    sll $t7, $t0, 2
    addi $t8, $sp, 32
    add $t8, $t8, $t7
    lw $t9, 0($t8)
    # Print integer
    move $a0, $t9
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t0, 555         # Load constant 555 for print
    # Print integer
    move $a0, $t0
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Argument: localArray
    # Call function readArray with 1 arguments
    lw $a0, 0($sp)     # Load argument 'localArray'
    jal func_readArray
    move $t0, $v0      # Get return value
    move $t7, $t0       # result = t1
    sw $t7, 72($sp)     # Store to 'result'
    # Print integer
    move $a0, $t7
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t7, 666         # Load constant 666 for print
    # Print integer
    move $a0, $t7
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Argument: 5
    # Call function square with 1 arguments
    li $a0, 5
    jal func_square
    move $t0, $v0      # Get return value
    move $t1, $t0       # a = t1
    sw $t1, 52($sp)     # Store to 'a'
    # Print integer
    move $a0, $t1
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Argument: 3
    # Call function cube with 1 arguments
    li $a0, 3
    jal func_cube
    move $t0, $v0      # Get return value
    move $t2, $t0       # b = t1
    sw $t2, 56($sp)     # Store to 'b'
    # Print integer
    move $a0, $t2
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t1, 0         # Load return value
    move $v0, $t1       # Move to return register
    # Return from function
    # End of function main

    # Spill any remaining registers

    # Exit program
    addi $sp, $sp, 400
    li $v0, 10
    syscall
