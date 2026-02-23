/* Test Case 1: Simple Counter Loop
 * Tests basic while loop functionality
 * Expected output: 1, 2, 3, 4, 5
 */

int main() {
    int i;
    i = 1;

    while (i <= 5) {
        print(i);
        i = i + 1;
    }

    return 0;
}
