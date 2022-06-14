#include <bits/stdc++.h>
int x, y;
const int N = 1e9;

int main() {
    y = 0;
    for (int i = 1; i <= N; ++i) {
        x += y, y = (i & 1);
    }
    printf("%d\n", x);
    return 0;
}











