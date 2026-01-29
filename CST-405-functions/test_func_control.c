int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int factorial(int n) {
    int result;
    result = 1;

    while (n > 0) {
        result = result * n;
        n = n - 1;
    }

    return result;
}

int main() {
    int x;
    int y;
    int z;

    x = 10;
    y = 20;
    z = max(x, y);
    print(z);

    x = 5;
    y = factorial(x);
    print(y);

    return 0;
}
