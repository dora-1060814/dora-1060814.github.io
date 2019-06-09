a = ('12', 'a15', '18', '21', '24')
b = ('16', '20', '24b', '28', '32')
c = ('25', '30', '35', '4c0', '45')
# progression 是1個tuple，內層有3個tuple
progression = (a, b, c)
numbers = '0123456789'

# 第一層讀 tuple 中的 tuple
for p in progression:
    int_sum = 0
    # 第二層讀 tuple 中的 string
    for i in p:
        print(i)
        # 假設 i 是可以加總的數值
        is_num = True
        # 第三層讀 string 中的 string(char 字元)
        for j in i:
            # print('   ', j)
            # 只要出現非數字，將 is_num 改成 False
            if numbers.find(j) == -1:
                is_num = False
                break
        # 判斷 is_num 是否為 True
        if is_num:
            int_sum += int(i)
    print('Sum:', int_sum)    

