/* Test while loop optimizations */

int main() {
    int x;

    /* Test 1: Dead loop - while(0) should be optimized away */
    x = 10;
    while (0) {
        x = 99;  /* This should never execute */
    }
    print(x);  /* Should print 10 */

    /* Test 2: Normal loop */
    x = 0;
    while (x < 3) {
        print(x);
        x = x + 1;
    }

    return 0;
}
