# afruitcenter.py
from mydb import DB

class FruitCenter:
    def __init__(self):
        self.menu_title = '蔬果店'
        self.menu = {
            'a':'蔬果種類',
            'b':'蔬果品項：名稱、數量、單價',
            'c':'購買紀錄查詢',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda db, ft: self.create_fruits(db, ft),
            'b': lambda db, ft: self.list_all_fruit(db, ft),
            'c': lambda db, ft: self.transaction_history(db, ft),
            'd': lambda db, ft: self.customers(db, ft),
        }
        self.divider = '='*20
        

    def show_menu(self):
        """ 主選單
        """
        print(self.divider)
        print(self.menu_title)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def create_fruits(self, db, func_title):
        """ 增修水果
        """
        while True:
            subopt = input('1.增修 2.查詢 3.刪除 4.列表 exit.離開: ')
            if subopt == 'exit':
                break
            else:
                print('水果數:', db.count_fruit())

                if subopt == '4':
                    db.list_all_fruit()
                    continue
                
                if subopt in ('1', '2', '3'):
                    in_fruit = input('水果: ')
                if subopt == '1':
                    number = input('個數: ')
                    if number.isdigit():
                        number = int(number)
                    else:
                        number = '' 
                    price = input('價格:  ')
                    if price.isdigit():
                        price = int(price)
                    else:
                        price = ''
                    db.insert_or_update_fruit(in_fruit, number, price)
                    db.check_fruit_out(in_fruit)
                elif subopt == '2':

                    db.check_fruit_out(in_fruit)
                elif subopt == '3':
                    db.delete_fruit(in_fruit)
                else:
                    db.check_fruit_out(subopt)
        return func_title

    def customers(self, db, func_title):
        """ 顧客列表
        """
        db.list_all_examinees()
        return func_title

    def fruit_list(self, db, func_title):
        """ 個人購買查詢
        """
        while True:
            qaccount = input('請輸入帳號 (exit.離開): ')
            if qaccount == 'exit':
                break
            db.list_scores_by_account(qaccount)
        return func_title
        
# entry point
with DB() as db:
    afruitcenter = FruitCenter()
    while True:
        func_id, func_name = afruitcenter.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            afruitcenter.menu_func[func_id](db, func_name)
        print()
