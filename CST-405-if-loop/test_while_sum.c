/* Test Case 2: Sum Accumulation
 * Tests while loop with accumulation pattern
 * Expected output: 55 (sum of 1 through 10)
 */

int main() {
    int sum;
    int i;

    sum = 0;
    i = 1;

    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }

    print(sum);  // Should print 55
    return 0;
}
