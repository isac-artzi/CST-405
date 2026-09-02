/* Comprehensive While Loop Test File
 * Tests all aspects of while loop functionality:
 * 1. Simple while loops
 * 2. Nested while loops
 * 3. While loops with arrays
 * 4. While loops with function calls
 * 5. Complex conditions
 * 6. Edge cases
 */

/* Helper function for testing */
int isEven(int n) {
    int half;
    half = n / 2;
    return half * 2 == n;
}

/* Function that uses a while loop */
int sumToN(int n) {
    int sum;
    int i;
    sum = 0;
    i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

/* Function to find maximum in array */
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

int main() {
    int i;
    int j;
    int sum;
    int product;
    int count;
    int numbers[10];
    int result;

    /* TEST 1: Simple while loop - count from 1 to 5 */
    print(1111);
    i = 1;
    while (i <= 5) {
        print(i);
        i = i + 1;
    }

    /* TEST 2: While loop with accumulation */
    print(2222);
    sum = 0;
    i = 1;
    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);  /* Should print 55 */

    /* TEST 3: While loop with multiplication */
    print(3333);
    product = 1;
    i = 1;
    while (i <= 5) {
        product = product * 2;
        i = i + 1;
    }
    print(product);  /* Should print 32 (2^5) */

    /* TEST 4: Nested while loops - multiplication table */
    print(4444);
    i = 1;
    while (i <= 3) {
        j = 1;
        while (j <= 3) {
            result = i * j;
            print(result);
            j = j + 1;
        }
        i = i + 1;
    }

    /* TEST 5: While loop with array - fill array */
    print(5555);
    i = 0;
    while (i < 10) {
        numbers[i] = i * 10;
        i = i + 1;
    }

    /* Print array contents */
    i = 0;
    while (i < 10) {
        print(numbers[i]);
        i = i + 1;
    }

    /* TEST 6: While loop with function call */
    print(6666);
    result = sumToN(10);
    print(result);  /* Should print 55 */

    /* TEST 7: While loop with array and function */
    print(7777);
    numbers[0] = 15;
    numbers[1] = 42;
    numbers[2] = 8;
    numbers[3] = 23;
    numbers[4] = 16;
    result = findMax(numbers, 5);
    print(result);  /* Should print 42 */

    /* TEST 8: While loop with complex condition */
    print(8888);
    i = 0;
    sum = 0;
    while (i < 10) {
        if (i > 5) {
            sum = sum + i;
        }
        i = i + 1;
    }
    print(sum);  /* Should print 6+7+8+9 = 30 */

    /* TEST 9: While loop with condition using function */
    print(9999);
    count = 0;
    i = 0;
    while (i < 10) {
        if (isEven(i)) {
            count = count + 1;
        }
        i = i + 1;
    }
    print(count);  /* Should print 5 (0,2,4,6,8) */

    /* TEST 10: Countdown loop */
    print(1000);
    i = 10;
    while (i > 0) {
        print(i);
        i = i - 1;
    }

    /* TEST 11: Triple nested while loops */
    print(1100);
    i = 1;
    while (i <= 2) {
        j = 1;
        while (j <= 2) {
            int k;
            k = 1;
            while (k <= 2) {
                result = i * 100 + j * 10 + k;
                print(result);
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }

    /* TEST 12: While loop that immediately exits (condition false) */
    print(1200);
    i = 10;
    while (i < 5) {
        print(9999);  /* Should never execute */
        i = i + 1;
    }
    print(1201);  /* Should print immediately */

    return 0;
}

