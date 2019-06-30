# acustomer.py
from mydb import DB
import random

class Customer:
    def __init__(self):
        self.menu_title = '顧客'
        self.account = ''
        self.menu = {
            'a':'登入．註冊',
            'b':'訂購蔬果',
            'c':'個人購買紀錄',
            'd':'退貨處理',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda db, ft: self.login_or_signup(db, ft),
            'b': lambda db, ft: self.book_fruit(db, ft),
            'c': lambda db, ft: self.test_fill_in_the_blank(db, ft),
            'd': lambda db, ft: self.customer_list(db, ft),
        }
        self.divider = '='*20

    def show_menu(self, account=''):
        """ 主選單
        """
        print(self.divider)
        if self.account == '':
            print(self.menu_title, '尚未登入')
        else:
            print(self.menu_title, self.account)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def login_or_signup(self, db, func_title):
        """ 登入．註冊
        """
        account_input = input('請輸入帳號: ')
        if db.check_if_examinee_existed(account_input):
            self.account = account_input
            print(db.get_customer_info(self.account))
        else:
            if db.insert_or_update_examinee(account_input, 'insert'):
                print('註冊成功，可立即購買蔬果')

    def customer_list(self, db, func_title):
        """ 個人購買查詢 
        """
        db.list_scores_by_account(self.account)
        return func_title

    def profile(self, db, func_title):
        """ 個人資料修改
        """
        print(db.get_customer_info(self.account))
        if db.insert_or_update_customer(self.account, 'update'):
            print(db.get_customer_info(self.account))
            print('資料已更新')
        else:
            print('資料未更新')
        return func_title

    def book_fruit(self, db, func_title):
        """ 訂購蔬果
        """
        
        while True:
            all_fruit = db.list_all_fruit()
           # all_fruit[0][2] # 1. apple
           # all_fruit[1][2] # 2. banana
            book = input('choose a fruit or quit  ')
            if book.lower() == 'quit':
                break
            book = int(book)
            quantity = int(input('quantity?  '))
            # 當存量為0或小於 quantity，不允許購買
            # 存量已經為0，可以考慮不顯示選項，但也要避免誤選而發生錯誤
            if all_fruit[book-1][2] == 0:
                print('賣完了')
                continue
            elif all_fruit[book-1][2] < quantity:
                print('數量不足')
                continue
                
            db.book_fruit(self.account, book, quantity)
            db.list_record_fruit(self.account)
            # 個人做完一筆購買之後
            # 要以亂數選取其他顧客，數量 n 亂選：random.sample(顧客list/tuple, random.randint(1, n))
            other_customers = db.other_customers()
            # print(other_customers)
            other_customers = random.sample(other_customers, random.randint(1, len(other_customers)))
            
            # 每位要買的顧客，都亂選水果及購買數量
            # 動作會很類似 db.book_fruit() 裡面的程式
            for customer in other_customers:
                print(customer[0])
                rand_fruit = random.sample(db.list_all_fruit(), 1)
                rand_quantity = random.randint(1, rand_fruit[0][2])
                print(rand_fruit[0][2])
                # 模擬顧客購買完之後，應該是要顯示類似個人購買的明細列表，而不要顯示全部存量
                db.book_fruit(customer[0], rand_fruit[0][0], rand_quantity)
                print()



# entry point
with DB() as db:
    acustomer = Customer()
    while True:
        func_id, func_name = acustomer.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            if acustomer.account == '':
                func_id = 'a'
                print('請先登入或註冊')
            acustomer.menu_func[func_id](db, func_name)
        print()
