// Test for loop: sum 1..5
int main() {
    int i;
    int sum;
    sum = 0;
    for (i = 1; i <= 5; i = i + 1) {
        sum = sum + i;
    }
    print(sum);
}
