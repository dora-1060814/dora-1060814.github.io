輸入：任意數 n
處理：產生 n 組數值資料，每組 3 個數值，存至 a, b, c
(+2) a 和 b 的數值不是 0 就是 1~9 之間的整數，c 只會是 0 或 1
(+1) 判斷 a 和 b 的 AND 運算結果是否等於 c
(+1) 判斷 a 和 b 的 OR 運算結果是否等於 c
(+1) 判斷 a 和 b 的 XOR 運算結果是否等於 c
輸出：
(+2) 每組數值，以及可能的運算結果
"""

import random

n = int(input('n: '))
a = []
b = []
c = []
for i in range(n):  
    for i in range(3):
        q = random.randint(0, 9)
        w = random.randint(0, 9)
        e = random,randint(0, 1)
        a.append(q)
        b.append(w)
        c.append(e)
print(a)
print(b)
print(c)
