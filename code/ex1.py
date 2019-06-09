"""
題目：奇偶秘差 (APCS-1060304-1)
輸入：任意數 n
處理：產生 n 個數值，範圍 10 的 12~15 次方
(+3) 分別計算奇位數和及偶位數和
(+1) 奇位數和相減偶位數和，取絕對值，即為秘密差
輸出：
(+1) 數字、奇位數和、偶位數和、秘密差
(+2) 最大及最小秘密差的數值
"""

import random

list_n = []
a = 0

n = int(input('n: '))
for i in range(n):
   number = str(random.randint(10**12, 10**15))
   print(number)
   odd_sum = 0
   even_sum = 0
   b = len(number)
   print('len:', b)
   for j in range(b):
       if j % 2 == 0:
           odd_sum += int(number[j])
       else:
           even_sum += int(number[j])
   print('sum of odds: ', odd_sum)
   print('sum of evens: ', even_sum)
   secret_difference = abs(odd_sum - even_sum)

print('numbers: ', number, 'Odd_sum: ', odd_sum, 'Even: ', even_sum, 'secret_difference:,'), secret_difference


    
   





