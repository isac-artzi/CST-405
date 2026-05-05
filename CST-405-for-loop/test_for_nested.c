// Nested for loops: print products
int main() {
    int i;
    int j;
    int product;
    for (i = 1; i <= 3; i = i + 1) {
        for (j = 1; j <= 3; j = j + 1) {
            product = i * j;
            print(product);
        }
    }
}
