class Kiwoom():
    def __init__(self):
        self.stock = {
            'naver':3000,
            'apple':6000,
            'daum':1500,
            'netflix':5000,
            'google':10000
        }

class Condition():
    def __init__(self):
        pass

    def sell_filtering(self, stock):
        stock_li = []
        for key in stock.keys():
            if stock[key]<=5000:
                stock_li.append(stock[key])
        return stock_li


kiwoom = Kiwoom()
print(kiwoom.stock)

condition = Condition()
stock_list = condition.sell_filtering(kiwoom.stock)
print(stock_list)