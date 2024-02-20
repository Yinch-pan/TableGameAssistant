import sys
import os
import math as mth
from collections import Counter, deque, defaultdict
from heapq import nsmallest, nlargest, heapify, heappop, heappush
from io import BytesIO, IOBase
import bisect

# sys.setrecursionlimit(10**6)
BUFSIZE = 4096
MOD = 10 ** 9 + 7
MODD = 998244353
inf = float('inf')


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


from types import GeneratorType


def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack: return f(*args, **kwargs)
        to = f(*args, **kwargs)
        while True:
            if type(to) is GeneratorType:
                stack.append(to)
                to = next(to)
            else:
                stack.pop()
                if not stack: break
                to = stack[-1].send(to)
        return to

    return wrappedfunc


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

input = lambda: sys.stdin.readline().rstrip("\r\n")
I = lambda: input()
II = lambda: int(input())
MI = lambda: map(str, input().split())
MII = lambda: map(int, input().split())
LI = lambda: list(input().split())
LII = lambda: list(map(int, input().split()))
ZLI = lambda: [0] + list(map(int, input().split()))


def solve():
    g = defaultdict(list)
    n = II()
    a = [0, 0] + LII()
    res = [[0] * 2 for i in range(n + 1)]
    s = ' ' + I()
    for i in range(2, n + 1):
        g[i].append(a[i])
        g[a[i]].append(i)

    # print(g)
    @bootstrap
    def dfs(u, pa):
        if s[u] == 'P':
            for v in g[u]:
                if v == pa: continue
                yield dfs(v, u)
                if s[v] == 'P':
                    res[u][0] += res[v][0]
                if s[v] == 'S':
                    res[u][0] += res[v][1] + 1
                if s[v] == 'C':
                    res[u][0] += min(res[v][0], res[v][1] + 1)

        if s[u] == 'S':
            for v in g[u]:
                if v == pa: continue
                yield dfs(v, u)
                if s[v] == 'P':
                    res[u][1] += res[v][0] + 1
                if s[v] == 'S':
                    res[u][1] += res[v][1]
                if s[v] == 'C':
                    res[u][1] += min(res[v][0] + 1, res[v][1])
        if s[u] == 'C':
            for v in g[u]:
                if v == pa: continue
                yield dfs(v, u)
                if s[v] == 'P':
                    res[u][0] += res[v][0]
                    res[u][1] += res[v][0] + 1

                if s[v] == 'S':
                    res[u][0] += res[v][1] + 1
                    res[u][1] += res[v][1]

                if s[v] == 'C':
                    res[u][0] += min(res[v][0], res[v][1] + 1)
                    res[u][1] += min(res[v][0] + 1, res[v][1])
        yield None

    dfs(1, -1)

    if s[1]=='P':
        print(res[1][0])
    if s[1]=='S':
        print(res[1][1])
    if s[1]=='C':
        print(min(res[1]))


for case in range(II()):
    solve()
