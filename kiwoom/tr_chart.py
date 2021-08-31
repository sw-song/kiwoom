from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errCode import *
from config.slack import *

class GetChartInfo(QAxWidget):
    def __init__(self):
        super().__init__()
        print('class: GetCharInfo -- api[kiwoom] connected')

        self.screen_calculate_stock = '4000'
    
        self.calculator_fnc() #종목분석

    def get_code_list_by_market(self, market_code):
        '''
        전체 종목 코드 반환
        '''
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market_code)
        print(code_list)
        code_list = code_list.split(';')[:-1]
        return code_list

    def calculator_fnc(self):
        '''
        종목 분석
        '''
        code_list = self.get_code_list_by_market('10') #코스닥 전체 종목 조회
        print('코스닥 종목 수 : {}'.format(len(code_list)))


    def day_kiwoom_db(self, code=None, date=None, sPrevNext='0'):
        self.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)
        self.dynamicCall('SetInputValue(QString, QString)', '수정주가구분', '1')

        if date != None:
            self.dynamicCall('SetInputValue(QString, QString)', '기준일자', date)
        
        self.dynamicCall('CommRqData(QString, QString, int, QString)',\
             '주식일봉차트조회', 'opt10081', sPrevNext, self.screen_calculate_stock)
