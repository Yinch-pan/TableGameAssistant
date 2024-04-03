n, K = 6, 6
a = [0] + [1, 1, 1, 2, 3, 4]
b = [0]
for i in range(1, n + 1):
    b.append(b[-1] ^ a[i])
f = [[[0] * (n + 5) for i in range(K + 5)] for j in range(n + 5)]

for i in range(n):
    for j in range(1, K + 1):
        for k in range(1, n + 1):
            f[i + 1][j + 1][i + 1] = max(f[i][j][k] + a[i + 1], f[i + 1][j + 1][i + 1])
            f[i + 1][j][k] = max(f[i][j][k] - (b[i] - b[k - 1]) + (b[i + 1] - b[k - 1]), f[i + 1][j][k])
# for l in f:
#     print(l)
print(max(f[n][K]))
