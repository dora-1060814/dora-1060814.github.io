class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.title_side = '-'*12

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """ 開啟資料庫連線
        """
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('fruit.db')
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """ 關閉資料庫連線
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def count_fruit(self):
        """ 計算蔬果品項
        """
        self.cur.execute("SELECT COUNT(*) FROM FRUIT")
        return self.cur.fetchone()[0]

    def get_max_id(self, arg_table):
        """ 取得資料最新編號
        """
        self.cur.execute("SELECT MAX(ID) FROM {}".format(arg_table))
        return self.cur.fetchone()[0] + 1

    def list_all_fruit(self):
        """ 蔬果列表
        """
        self.cur.execute("SELECT * FROM FRUIT")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print('{} {} {} {}'.format(*row))
        print()
        return all_rows

    def insert_or_update_fruit(self, arg_fruit, number, price):
        """ 增修蔬果
        (*)維護時的列表，要出現價格
        (*)若是修改，應該允許不用輸入數量或價格，例如不輸入直接按 Enter 表示不修改
        (*)水果資料的名稱可分設中英文，以英文輸入管理，中文顯示 (可暫時不用處理)
        """
        fruit_max_id = self.get_max_id('fruit')
        self.cur.execute("SELECT COUNT(*) FROM FRUIT WHERE FRUIT=?", (arg_fruit,))
        count_result = self.cur.fetchone()[0]
        if count_result == 0:
            if number == '' or price == '':
                print('錯誤：必須輸入數量及價格')
                return False
            self.cur.execute("INSERT INTO FRUIT VALUES (?, ?, ?, ?)", 
                (fruit_max_id, arg_fruit, number, price))
        elif count_result > 0:
            if number != '':
                self.cur.execute("UPDATE FRUIT SET NUMBER=? WHERE FRUIT=?", (number, arg_fruit))
            if price != '':
                self.cur.execute("UPDATE FRUIT SET PRICE=? WHERE FRUIT=?", (price, arg_fruit))
        return self.conn.commit()

    def check_fruit_out(self, arg_fruit):
        """ 查詢水果
        """
        arg_fruit = '%'+arg_fruit+'%'
        self.cur.execute("SELECT * FROM FRUIT WHERE FRUIT LIKE ?", (arg_fruit,))
        print(self.cur.fetchone())

    def delete_fruit(self, arg_fruit):
        """ 刪除水果
        """         
        self.cur.execute("DELETE FROM FRUIT WHERE FRUIT=?", (arg_fruit,))
        return self.conn.commit()

    def list_all_customers(self):
        """ 顧客列表
        """
        self.cur.execute("SELECT * FROM CUSTOMERS")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def check_if_examinee_existed(self, arg_account):
        """ 檢查顧客是否註冊
        """
        self.cur.execute("SELECT COUNT(*) FROM CUSTOMERS WHERE ACCOUNT=?", (arg_account,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def insert_or_update_examinee(self, account_id, action):
        """ 增修顧客
        """
        data_ok = True
        full_name = input('全名: ')
        if full_name == 'q':
            return False

        gender = input('性別(F.女性 M.男性): ').upper()
        if gender == 'F':
            gender = 0
        elif gender == 'M':
            gender = 1
        else:
            data_ok = False

        birth_year = input('出生年: ')
        if birth_year.isdigit():
            birth_year = int(birth_year)
            if birth_year not in range(1950, 2007):
                data_ok = False
        else:
            data_ok = False

        # 資料無誤，准許註冊            
        if data_ok:
            if action == 'insert':
                customers_max_id = self.get_max_id('CUSTOMERS')
                self.cur.execute("INSERT INTO  CUSTOMERS VALUES (?, ?, ?, ?, ?)", 
                    (customers_max_id, account_id, full_name, gender, birth_year))
            elif action == 'update':
                self.cur.execute("UPDATE CUSTOMERS SET NAME=?, GENDER=?, BIRTH_YEAR=? WHERE ACCOUNT=?", 
                    (full_name, gender, birth_year, account_id))
            self.conn.commit()
            return True
        else:
            return False
                        
    def get_customer_info(self, account):
        """ 查詢顧客資訊
        """
        self.cur.execute("SELECT * FROM CUSTOMERS WHERE ACCOUNT=?", (account,))
        customers_info = self.cur.fetchone()
        return customers_info

    def insert_fruit(self, account, ex_type, ex_fruit):
        """ 增修蔬果
        """
        fruit_max_id = self.get_max_id('fruit')
        self.cur.execute("INSERT INTO FRUIT VALUES (?, ?, ?, ?, ? date('now'))", 
            (fruit_max_id, account, ex_type, ex_fruit, price))
        self.conn.commit()
        return True


    def list_fruit_by_account(self, account):
        """ 個人購買紀錄查詢
        """
        account_like = ''.join(('%', account, '%'))
        self.cur.execute("SELECT * FROM FRUIT WHERE ACCOUNT LIKE ?", (account_like,))
        all_rows = self.cur.fetchall()
        if len(all_rows) > 0:
            for row in all_rows:
                print(row)
        else:
            print(account, '查無任何購買紀錄')

    
    def book_fruit(self, account, fruit_id, quantity):
        """ 訂購蔬果
        """
        # INSERT 時，應該考慮寫入水果名稱
        # 依編號查詢水果名稱
        max_id = self.get_max_id('record')
        self.cur.execute("SELECT FRUIT, PRICE FROM FRUIT WHERE ID=?", (fruit_id,))
        # 一次查詢兩個欄位，值同時指定給兩個變數
        # 下面這行的作用，等於其後的兩行(已註解)
        fruit, price = self.cur.fetchone()
        # fruit = self.cur.fetchone()[0]
        # price = self.cur.fetchone()[1]
        # ID integer, ACCOUNT text, FRUIT text, PRICE integer, QUANTITY integer, DATETIME text
        self.cur.execute("INSERT INTO RECORD VALUES(?, ?, ?, ?, ?, ?) ",
        (max_id, account, fruit, quantity, price, self.get_datetime()))
        # 更新數量時應比對 fruit_id
        self.cur.execute("UPDATE FRUIT SET QUANTITY=QUANTITY-? WHERE ID=?", (quantity, fruit_id,))
        self.conn.commit()
        return quantity * price

    def get_datetime(self):
        """日期時間
        """
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_today(self):
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y-%m-%d")

    def list_record_fruit(self,account):
        """ # 1. 每採購一筆，就顯示當日購買的明細
            # 2. 列出 RECORD，SELECT 的 WHERE 條件要比對帳號及日期
            # 3. TOTAL 可以用計算欄位的方式設定在 SELECT
            # 4. SELECT 查詢欄位至少應該設定如下：
            #    蔬果列表
        """
        # 前後加 % 符號是為了可以模糊查詢，模糊查詢要用 LIKE 運算子，不是 =
        today = '%'+self.get_today()+'%'
        print(account, today)
        self.cur.execute("""SELECT ID, FRUIT, PRICE, QUANTITY, 
            PRICE*QUANTITY AS TOTAL, DATETIME FROM RECORD 
            WHERE ACCOUNT=? AND DATETIME LIKE ?""", (account, today))
        all_rows = self.cur.fetchall()
        print('{:7} {:2} {:2} {:3} {}'.format('水果', '數量', '單價',
         '總金額', '日期時間'))
        print('-'*50)
        for row in all_rows:
            print('{:2} {:4} {:4} {:4} {:6} {}'.format(*row))
        print()

    def other_customers(self):
        self.cur.execute("SELECT ACCOUNT FROM CUSTOMERS WHERE ID>1")
        other_customers = self.cur.fetchall()
        return other_customers



if __name__ == '__main__':
    print('This is the DB class.')
