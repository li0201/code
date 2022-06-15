#include <bits/stdc++.h>
int x, y;
int main() {
    y = 0;
    for (int i = 1; i <= 1000000000; ++i) {
        x += y, y = (i & 1);
    }
    printf("%d\n", x);
    return 0;
}