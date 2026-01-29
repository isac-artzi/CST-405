/* OPTIMIZATION TEST FILE
 * This file demonstrates multiple levels of optimization opportunities:
 * 1. Constant folding in expressions
 * 2. Constant propagation through assignments
 * 3. Dead code elimination (constants that simplify)
 * 4. Arithmetic simplification
 */

int add(int a, int b) {
    int result;

    /* Simple addition - will use parameters as-is */
    result = a + b;

    return result;
}

int computeConstants() {
    int x;
    int y;
    int z;

    /* OPTIMIZATION OPPORTUNITY 1: Constant folding in assignment */
    x = 5 + 3;        /* Should fold to: x = 8 */

    /* OPTIMIZATION OPPORTUNITY 2: Multiple constant operations */
    y = 10 * 2;       /* Should fold to: y = 20 */

    /* OPTIMIZATION OPPORTUNITY 3: Constant arithmetic chain */
    z = x + y;        /* After folding: z = 8 + 20 = 28 */

    return z;
}

int complexCalculation(int n) {
    int a;
    int b;
    int c;
    int result;

    /* OPTIMIZATION OPPORTUNITY 4: Mix of constants and variables */
    a = n + 0;        /* Should simplify to: a = n */

    /* OPTIMIZATION OPPORTUNITY 5: Constant in subexpression */
    b = 2 * 3;        /* Should fold to: b = 6 */

    /* OPTIMIZATION OPPORTUNITY 6: Use folded constant */
    c = a + b;        /* Uses simplified values */

    /* OPTIMIZATION OPPORTUNITY 7: Multiply by constant */
    result = c * 1;   /* Should simplify to: result = c */

    return result;
}

int main() {
    int x;
    int y;
    int z;
    int w;
    int result1;
    int result2;

    /* Test 1: Direct constant folding */
    x = 10 + 5;       /* OPTIMIZE: x = 15 */
    y = 20 - 8;       /* OPTIMIZE: y = 12 */

    /* Test 2: Use optimized constants */
    z = add(x, y);    /* add(15, 12) */

    /* Test 3: More constant folding */
    w = 3 * 4;        /* OPTIMIZE: w = 12 */

    /* Test 4: Function with constant folding */
    result1 = computeConstants();  /* Should return 28 */

    /* Test 5: Function with variable */
    result2 = complexCalculation(z);

    /* Print results */
    print(z);
    print(result1);
    print(result2);

    return 0;
}
