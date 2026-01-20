/*
 * Comprehensive C-Minus Test File
 * CST-405 Compiler Design
 *
 * This file tests ALL features of the C-Minus language:
 * - Global and local variables
 * - Scalar and array variables
 * - All arithmetic operators (+, -, *, /)
 * - All relational operators (<, <=, >, >=, ==, !=)
 * - If-else statements (simple and nested)
 * - While loops (simple and nested)
 * - Function declarations and calls
 * - Parameters (scalar and array)
 * - Return statements
 * - Recursion
 * - Array indexing
 * - Complex expressions
 * - Operator precedence
 * - Built-in functions: input() and output()
 */

/* ========================================
   GLOBAL VARIABLE DECLARATIONS
   ======================================== */

int globalCounter;
int globalArray[20];
int globalResult;

/* ========================================
   ARITHMETIC OPERATIONS TESTING
   ======================================== */

int testArithmetic(int a, int b) {
    int sum;
    int diff;
    int prod;
    int quot;
    int complex;

    /* Test all four basic operations */
    sum = a + b;
    diff = a - b;
    prod = a * b;
    quot = a / b;

    /* Test operator precedence: should be 2 + (3 * 4) = 14 */
    complex = 2 + 3 * 4;

    /* Test with parentheses: should be (2 + 3) * 4 = 20 */
    complex = (2 + 3) * 4;

    /* Complex expression */
    complex = a * b + a / b - a + b;

    return sum + diff + prod + quot;
}

/* ========================================
   RELATIONAL OPERATIONS TESTING
   ======================================== */

int testRelational(int x, int y) {
    int result;

    result = 0;

    /* Test less than */
    if (x < y) {
        result = result + 1;
    }

    /* Test less than or equal */
    if (x <= y) {
        result = result + 10;
    }

    /* Test greater than */
    if (x > y) {
        result = result + 100;
    }

    /* Test greater than or equal */
    if (x >= y) {
        result = result + 1000;
    }

    /* Test equality */
    if (x == y) {
        result = result + 10000;
    }

    /* Test inequality */
    if (x != y) {
        result = result + 100000;
    }

    return result;
}

/* ========================================
   IF-ELSE STATEMENT TESTING
   ======================================== */

int testIfElse(int value) {
    int result;

    /* Simple if statement */
    if (value > 0) {
        result = 1;
    }

    /* If-else statement */
    if (value < 0) {
        result = -1;
    } else {
        result = 0;
    }

    /* Nested if-else */
    if (value > 100) {
        if (value > 200) {
            result = 200;
        } else {
            result = 100;
        }
    } else {
        if (value > 50) {
            result = 50;
        } else {
            result = 0;
        }
    }

    return result;
}

/* ========================================
   WHILE LOOP TESTING
   ======================================== */

int testWhileLoop(int n) {
    int sum;
    int i;

    sum = 0;
    i = 1;

    /* Simple while loop - sum from 1 to n */
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }

    return sum;
}

/* ========================================
   NESTED LOOPS TESTING
   ======================================== */

int testNestedLoops(int rows, int cols) {
    int total;
    int i;
    int j;

    total = 0;
    i = 0;

    /* Nested while loops */
    while (i < rows) {
        j = 0;
        while (j < cols) {
            total = total + 1;
            j = j + 1;
        }
        i = i + 1;
    }

    return total;
}

/* ========================================
   ARRAY OPERATIONS TESTING
   ======================================== */

void testArrayOperations(int arr[], int size) {
    int i;

    /* Initialize array */
    i = 0;
    while (i < size) {
        arr[i] = i * 2;
        i = i + 1;
    }

    /* Modify array elements */
    i = 0;
    while (i < size) {
        arr[i] = arr[i] + 1;
        i = i + 1;
    }
}

int sumArray(int arr[], int size) {
    int sum;
    int i;

    sum = 0;
    i = 0;

    while (i < size) {
        sum = sum + arr[i];
        i = i + 1;
    }

    return sum;
}

/* ========================================
   RECURSION TESTING
   ======================================== */

int factorial(int n) {
    int result;

    if (n <= 1) {
        result = 1;
    } else {
        result = n * factorial(n - 1);
    }

    return result;
}

int fibonacci(int n) {
    int result;

    if (n <= 1) {
        result = n;
    } else {
        result = fibonacci(n - 1) + fibonacci(n - 2);
    }

    return result;
}

int power(int base, int exp) {
    int result;

    if (exp == 0) {
        result = 1;
    } else {
        result = base * power(base, exp - 1);
    }

    return result;
}

/* ========================================
   GCD ALGORITHM (Euclidean)
   ======================================== */

int gcd(int a, int b) {
    int remainder;

    while (b != 0) {
        remainder = a - (a / b) * b;  /* Modulo operation */
        a = b;
        b = remainder;
    }

    return a;
}

/* ========================================
   ARRAY SEARCHING
   ======================================== */

int linearSearch(int arr[], int size, int target) {
    int i;
    int found;

    i = 0;
    found = -1;

    while (i < size) {
        if (arr[i] == target) {
            found = i;
            i = size;  /* Exit loop */
        } else {
            i = i + 1;
        }
    }

    return found;
}

/* ========================================
   ARRAY SORTING (Bubble Sort)
   ======================================== */

void bubbleSort(int arr[], int size) {
    int i;
    int j;
    int temp;

    i = 0;
    while (i < size - 1) {
        j = 0;
        while (j < size - i - 1) {
            if (arr[j] > arr[j + 1]) {
                /* Swap elements */
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

/* ========================================
   FINDING MAXIMUM AND MINIMUM
   ======================================== */

int findMax(int arr[], int size) {
    int max;
    int i;

    max = arr[0];
    i = 1;

    while (i < size) {
        if (arr[i] > max) {
            max = arr[i];
        }
        i = i + 1;
    }

    return max;
}

int findMin(int arr[], int size) {
    int min;
    int i;

    min = arr[0];
    i = 1;

    while (i < size) {
        if (arr[i] < min) {
            min = arr[i];
        }
        i = i + 1;
    }

    return min;
}

/* ========================================
   PRIME NUMBER CHECKING
   ======================================== */

int isPrime(int n) {
    int i;
    int result;

    if (n <= 1) {
        result = 0;
    } else {
        result = 1;
        i = 2;

        while (i < n) {
            if (n / i * i == n) {  /* Check if i divides n */
                result = 0;
                i = n;  /* Exit loop */
            } else {
                i = i + 1;
            }
        }
    }

    return result;
}

/* ========================================
   COUNT PRIMES UP TO N
   ======================================== */

int countPrimes(int limit) {
    int count;
    int i;

    count = 0;
    i = 2;

    while (i <= limit) {
        if (isPrime(i) == 1) {
            count = count + 1;
        }
        i = i + 1;
    }

    return count;
}

/* ========================================
   REVERSE ARRAY
   ======================================== */

void reverseArray(int arr[], int size) {
    int left;
    int right;
    int temp;

    left = 0;
    right = size - 1;

    while (left < right) {
        temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;

        left = left + 1;
        right = right - 1;
    }
}

/* ========================================
   COMPLEX EXPRESSION TESTING
   ======================================== */

int testComplexExpressions(int a, int b, int c) {
    int result;

    /* Multiple operations with precedence */
    result = a + b * c - a / b;

    /* Nested parentheses */
    result = ((a + b) * (c - a)) / (b + 1);

    /* Long expression */
    result = a * b + c * a - b / c + a - b + c;

    return result;
}

/* ========================================
   VOID FUNCTION TESTING
   ======================================== */

void testVoidFunction(int x) {
    int y;

    y = x * 2;
    output(y);
}

void printArray(int arr[], int size) {
    int i;

    i = 0;
    while (i < size) {
        output(arr[i]);
        i = i + 1;
    }
}

/* ========================================
   MULTIPLE PARAMETERS TESTING
   ======================================== */

int multiply3(int a, int b, int c) {
    return a * b * c;
}

int add4(int a, int b, int c, int d) {
    return a + b + c + d;
}

int max3(int a, int b, int c) {
    int max;

    max = a;

    if (b > max) {
        max = b;
    }

    if (c > max) {
        max = c;
    }

    return max;
}

/* ========================================
   ARRAY MANIPULATION FUNCTIONS
   ======================================== */

void fillArray(int arr[], int size, int value) {
    int i;

    i = 0;
    while (i < size) {
        arr[i] = value;
        i = i + 1;
    }
}

void copyArray(int source[], int dest[], int size) {
    int i;

    i = 0;
    while (i < size) {
        dest[i] = source[i];
        i = i + 1;
    }
}

int arrayEqual(int arr1[], int arr2[], int size) {
    int i;
    int equal;

    equal = 1;
    i = 0;

    while (i < size) {
        if (arr1[i] != arr2[i]) {
            equal = 0;
            i = size;  /* Exit loop */
        } else {
            i = i + 1;
        }
    }

    return equal;
}

/* ========================================
   MATHEMATICAL FUNCTIONS
   ======================================== */

int absoluteValue(int x) {
    int result;

    if (x < 0) {
        result = 0 - x;
    } else {
        result = x;
    }

    return result;
}

int sign(int x) {
    int result;

    if (x < 0) {
        result = -1;
    } else {
        if (x > 0) {
            result = 1;
        } else {
            result = 0;
        }
    }

    return result;
}

/* ========================================
   COUNTING AND ACCUMULATION
   ======================================== */

int sumOfSquares(int n) {
    int sum;
    int i;

    sum = 0;
    i = 1;

    while (i <= n) {
        sum = sum + i * i;
        i = i + 1;
    }

    return sum;
}

int sumOfCubes(int n) {
    int sum;
    int i;

    sum = 0;
    i = 1;

    while (i <= n) {
        sum = sum + i * i * i;
        i = i + 1;
    }

    return sum;
}

/* ========================================
   ARRAY STATISTICS
   ======================================== */

int calculateMean(int arr[], int size) {
    int sum;
    int i;

    sum = 0;
    i = 0;

    while (i < size) {
        sum = sum + arr[i];
        i = i + 1;
    }

    return sum / size;
}

int countOccurrences(int arr[], int size, int value) {
    int count;
    int i;

    count = 0;
    i = 0;

    while (i < size) {
        if (arr[i] == value) {
            count = count + 1;
        }
        i = i + 1;
    }

    return count;
}

/* ========================================
   BINARY OPERATIONS
   ======================================== */

int leftShift(int n, int bits) {
    int result;
    int i;

    result = n;
    i = 0;

    while (i < bits) {
        result = result * 2;
        i = i + 1;
    }

    return result;
}

int rightShift(int n, int bits) {
    int result;
    int i;

    result = n;
    i = 0;

    while (i < bits) {
        result = result / 2;
        i = i + 1;
    }

    return result;
}

/* ========================================
   STRING-LIKE OPERATIONS (using int arrays)
   ======================================== */

int arrayLength(int arr[], int maxSize) {
    int length;

    length = 0;

    while (length < maxSize) {
        if (arr[length] == 0) {
            length = maxSize;  /* Exit loop */
        } else {
            length = length + 1;
        }
    }

    return length;
}

/* ========================================
   MAIN FUNCTION - COMPREHENSIVE TESTING
   ======================================== */

void main(void) {
    int testArray[10];
    int testArray2[10];
    int i;
    int result;
    int a;
    int b;
    int choice;

    /* Initialize global variable */
    globalCounter = 0;

    /* Test 1: Arithmetic Operations */
    output(1);  /* Test marker */
    result = testArithmetic(10, 5);
    output(result);

    /* Test 2: Relational Operations */
    output(2);
    result = testRelational(5, 10);
    output(result);

    /* Test 3: If-Else Statements */
    output(3);
    result = testIfElse(75);
    output(result);

    /* Test 4: While Loops */
    output(4);
    result = testWhileLoop(10);
    output(result);

    /* Test 5: Nested Loops */
    output(5);
    result = testNestedLoops(5, 5);
    output(result);

    /* Test 6: Array Operations */
    output(6);
    testArrayOperations(testArray, 10);
    result = sumArray(testArray, 10);
    output(result);

    /* Test 7: Factorial (Recursion) */
    output(7);
    result = factorial(5);
    output(result);

    /* Test 8: Fibonacci */
    output(8);
    result = fibonacci(7);
    output(result);

    /* Test 9: Power Function */
    output(9);
    result = power(2, 5);
    output(result);

    /* Test 10: GCD */
    output(10);
    result = gcd(48, 18);
    output(result);

    /* Test 11: Array Search */
    output(11);
    i = 0;
    while (i < 10) {
        testArray[i] = i * 3;
        i = i + 1;
    }
    result = linearSearch(testArray, 10, 15);
    output(result);

    /* Test 12: Bubble Sort */
    output(12);
    testArray[0] = 5;
    testArray[1] = 2;
    testArray[2] = 8;
    testArray[3] = 1;
    testArray[4] = 9;
    bubbleSort(testArray, 5);
    printArray(testArray, 5);

    /* Test 13: Find Max and Min */
    output(13);
    result = findMax(testArray, 5);
    output(result);
    result = findMin(testArray, 5);
    output(result);

    /* Test 14: Prime Number Testing */
    output(14);
    result = isPrime(17);
    output(result);
    result = isPrime(18);
    output(result);

    /* Test 15: Count Primes */
    output(15);
    result = countPrimes(20);
    output(result);

    /* Test 16: Reverse Array */
    output(16);
    i = 0;
    while (i < 5) {
        testArray[i] = i + 1;
        i = i + 1;
    }
    reverseArray(testArray, 5);
    printArray(testArray, 5);

    /* Test 17: Multiple Parameters */
    output(17);
    result = multiply3(2, 3, 4);
    output(result);
    result = add4(1, 2, 3, 4);
    output(result);
    result = max3(5, 9, 3);
    output(result);

    /* Test 18: Array Fill and Copy */
    output(18);
    fillArray(testArray, 10, 7);
    copyArray(testArray, testArray2, 10);
    result = arrayEqual(testArray, testArray2, 10);
    output(result);

    /* Test 19: Absolute Value and Sign */
    output(19);
    result = absoluteValue(-15);
    output(result);
    result = sign(-5);
    output(result);
    result = sign(5);
    output(result);
    result = sign(0);
    output(result);

    /* Test 20: Sum of Squares and Cubes */
    output(20);
    result = sumOfSquares(5);
    output(result);
    result = sumOfCubes(5);
    output(result);

    /* Test 21: Array Statistics */
    output(21);
    i = 0;
    while (i < 5) {
        testArray[i] = (i + 1) * 2;
        i = i + 1;
    }
    result = calculateMean(testArray, 5);
    output(result);
    testArray[0] = 5;
    testArray[1] = 5;
    testArray[2] = 3;
    testArray[3] = 5;
    testArray[4] = 7;
    result = countOccurrences(testArray, 5, 5);
    output(result);

    /* Test 22: Bit Shift Operations */
    output(22);
    result = leftShift(3, 2);
    output(result);
    result = rightShift(16, 2);
    output(result);

    /* Test 23: Complex Expressions */
    output(23);
    result = testComplexExpressions(10, 5, 3);
    output(result);

    /* Test 24: Global Variables */
    output(24);
    globalCounter = 100;
    globalArray[0] = 10;
    globalArray[1] = 20;
    globalArray[2] = 30;
    output(globalCounter);
    output(globalArray[0] + globalArray[1] + globalArray[2]);

    /* Test 25: Void Functions */
    output(25);
    testVoidFunction(5);

    /* All tests complete */
    output(999);
}
