/* Test Case 3: Nested While Loops
 * Tests nested loop control flow
 * Expected output: 3x3 multiplication table
 * (1, 2, 3, 2, 4, 6, 3, 6, 9)
 */

int main() {
    int i;
    int j;

    i = 1;
    while (i <= 3) {
        j = 1;
        while (j <= 3) {
            print(i * j);
            j = j + 1;
        }
        i = i + 1;
    }

    return 0;
}
