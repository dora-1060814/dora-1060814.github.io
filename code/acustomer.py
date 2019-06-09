# acustomer.py
from mydb import DB

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
            db.list_all_fruit()
            book = input('choose a fruit or quit  ')
            if book.lower() == 'quit':
                break
            book = int(book)
            quantity = int(input('quantity?  '))
            db.book_fruit(self.account, book, quantity)
            db.list_record_fruit(self.account)
            # 個人做完一筆購買之後
            # 要以亂數選取其他顧客，數量 n 亂選：random.sample(顧客list/tuple, random.randint(1, n))
            other_customers = db.other_customers()
            print(other_customers)
            # other_customers = random.sample(other_customers, random.randint(1, len(other_customers)))
            # 每位要買的顧客，都亂選水果及購買數量
            # 動作會很類似 db.book_fruit() 裡面的程式
            # db.book_fruit(selected_customer, rand_fruit, rand_quantity)
            # for customer in other_customers:
            #     # 選取的水果是否還有存量
            #     rand_fruit = ?
            #     rand_quantity = ?
            #     db.book_fruit(customer, rand_fruit, rand_quantity)


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
