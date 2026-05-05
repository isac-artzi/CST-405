/* Simple while loop test */

int main() {
    int i;
    int sum;

    print(1111);
    sum = 0;
    i = 1;
    while (i <= 5) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);

    return 0;
}
