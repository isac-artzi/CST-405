.data

.text
.globl main
main:
    # Allocate stack space
    addi $sp, $sp, -400


# Function: add
add:
    # Save return address and allocate local stack frame
    # Parameter 'a' at offset 0
    # Parameter 'b' at offset 4
    # Declared 'result' at offset 8
    lw $t0, 0($sp)     # Load variable 'a'
    lw $t1, 4($sp)     # Load variable 'b'
    add $t2, $t0, $t1   # t0 = a + b
    move $t0, $t2       # result = t0
    sw $t0, 8($sp)     # Store to 'result'
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function add
    # Restore and return
    jr $ra

# Function: computeConstants
computeConstants:
    # Save return address and allocate local stack frame
    # Declared 'x' at offset 0
    # Declared 'y' at offset 4
    # Declared 'z' at offset 8
    li $t2, 8         # t0 = 8 (constant)
    move $t0, $t2       # x = t0
    sw $t0, 0($sp)     # Store to 'x'
    li $t2, 20         # t0 = 20 (constant)
    move $t1, $t2       # y = t0
    sw $t1, 4($sp)     # Store to 'y'
    add $t2, $t0, $t1   # t0 = x + y
    move $t0, $t2       # z = t0
    sw $t0, 8($sp)     # Store to 'z'
    move $v0, $t0       # Move to return register
    # Return from function
    # End of function computeConstants
    # Restore and return
    jr $ra

# Function: complexCalculation
complexCalculation:
    # Save return address and allocate local stack frame
    # Parameter 'n' at offset 0
    # Declared 'a' at offset 4
    # Declared 'b' at offset 8
    # Declared 'c' at offset 12
    # Declared 'result' at offset 16
    lw $t0, 0($sp)     # Load variable 'n'
    li $t1, 0         # Load constant 0
    add $t2, $t0, $t1   # t0 = n + 0
    move $t0, $t2       # a = t0
    sw $t0, 4($sp)     # Store to 'a'
    li $t2, 6         # t0 = 6 (constant)
    move $t1, $t2       # b = t0
    sw $t1, 8($sp)     # Store to 'b'
    add $t2, $t0, $t1   # t0 = a + b
    move $t0, $t2       # c = t0
    sw $t0, 12($sp)     # Store to 'c'
    move $t1, $t2       # result = t0
    sw $t1, 16($sp)     # Store to 'result'
    move $v0, $t1       # Move to return register
    # Return from function
    # End of function complexCalculation
    # Restore and return
    jr $ra

# Function: main
    # Declared 'x' at offset 0
    # Declared 'y' at offset 4
    # Declared 'z' at offset 8
    # Declared 'w' at offset 12
    # Declared 'result1' at offset 16
    # Declared 'result2' at offset 20
    li $t2, 15         # t0 = 15 (constant)
    move $t1, $t2       # x = t0
    sw $t1, 0($sp)     # Store to 'x'
    li $t2, 12         # t0 = 12 (constant)
    move $t3, $t2       # y = t0
    sw $t3, 4($sp)     # Store to 'y'
    # Argument: x
    # Argument: y
    # Call function add with 2 arguments
    # Return value in $t2 (placeholder)
    move $t4, $t2       # z = t0
    sw $t4, 8($sp)     # Store to 'z'
    li $t2, 12         # t0 = 12 (constant)
    move $t5, $t2       # w = t0
    sw $t5, 12($sp)     # Store to 'w'
    # Call function computeConstants with 0 arguments
    # Return value in $t2 (placeholder)
    move $t6, $t2       # result1 = t0
    sw $t6, 16($sp)     # Store to 'result1'
    # Argument: z
    # Call function complexCalculation with 1 arguments
    # Return value in $t2 (placeholder)
    move $t7, $t2       # result2 = t0
    sw $t7, 20($sp)     # Store to 'result2'
    # Print integer
    move $a0, $t4
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Print integer
    move $a0, $t6
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    # Print integer
    move $a0, $t7
    li $v0, 1
    syscall
    # Print newline
    li $v0, 11
    li $a0, 10
    syscall
    li $t4, 0         # Load return value
    move $v0, $t4       # Move to return register
    # Return from function
    # End of function main

    # Spill any remaining registers

    # Exit program
    addi $sp, $sp, 400
    li $v0, 10
    syscall
