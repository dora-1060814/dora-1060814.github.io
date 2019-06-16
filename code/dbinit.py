import os
try:
    os.unlink('fruit.db')
except:
    print('首次建檔')

import sqlite3
conn = sqlite3.connect('fruit.db')
cur = conn.cursor()

def show_all_rows(all_rows):
    for row in all_rows:
        print(row)
    print()

# 水果表
cur.execute('''CREATE TABLE FRUIT
    (ID integer, FRUIT text, QUANTITY integer, PRICE integer)''')
# 水果表初始資料
cur.execute("INSERT INTO FRUIT VALUES (1, '蘋果', 500, 15)")
cur.execute("INSERT INTO FRUIT VALUES (2, '香蕉', 500, 10)")
cur.execute("INSERT INTO FRUIT VALUES (3, '鳳梨', 500, 35)")
cur.execute("INSERT INTO FRUIT VALUES (4, '橘子', 500, 7)")
conn.commit()
 
# 查詢水果
cur.execute("SELECT * FROM FRUIT")
show_all_rows(cur.fetchall())

# 設定表
cur.execute('''CREATE TABLE SETTINGS
    (ID integer, TYPE text, NUM_OF_QUESTIONS integer, OPTION integer)''')
# 設定表初始資料
cur.execute("INSERT INTO SETTINGS VALUES (1, 'multiple_choice', 10, 4)")
cur.execute("INSERT INTO SETTINGS VALUES (2, 'fill_in_the_blank', 10, 1)")
conn.commit()
# 查詢設定表
cur.execute("SELECT * FROM SETTINGS")
show_all_rows(cur.fetchall())

#交易紀錄表
cur.execute('''CREATE TABLE RECORD
    (ID integer, ACCOUNT text, FRUIT text, PRICE integer, QUANTITY integer, DATETIME text)''')
cur.execute("INSERT INTO RECORD VALUES (1, 'chris1980', '蘋果', 15, 50, '2019-04-14 10:20:30') " )
cur.execute("INSERT INTO RECORD VALUEs (2, 'gal1985', '香蕉', 10, 50, '2019-04-15 10:20:30') ")
show_all_rows(cur.fetchall())

# 顧客表
cur.execute('''CREATE TABLE CUSTOMERS
    (ID integer, ACCOUNT text, NAME text, GENDER integer, BIRTH_YEAR integer)''')
# 顧客表初始資料
cur.execute("INSERT INTO CUSTOMERS VALUES (1, 'dora', 'Dora ya', 1, 2001)")
cur.execute("INSERT INTO CUSTOMERS VALUES (2, 'chris', 'Chris evan', 1, 1980)")
cur.execute("INSERT INTO CUSTOMERS VALUES (3, 'diego', 'diego go', 1, 1999)")
cur.execute("INSERT INTO CUSTOMERS VALUES (4, 'elizabeth', 'elizabeth olsen', 0, 1975)")
cur.execute("INSERT INTO CUSTOMERS VALUES (5, 'peter', 'peter parker', 1, 1985)")
cur.execute("INSERT INTO CUSTOMERS VALUES (6, 'doctor', 'doctor strange', 1, 1989)")
cur.execute("INSERT INTO CUSTOMERS VALUES (7, 'hank', 'hank pym', 1, 1995)")
cur.execute("INSERT INTO CUSTOMERS VALUES (8, 'barry', 'barry allen', 0, 1988)")
cur.execute("INSERT INTO CUSTOMERS VALUES (9, 'robert', 'robert downeyjr ', 1, 1990)")
conn.commit()
# 查詢顧客
cur.execute("SELECT * FROM CUSTOMERS")
show_all_rows(cur.fetchall())



conn.close()
