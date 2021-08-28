import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance() # api 연결
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)

    def comm_connect(self):
        self.dynamicCall('CommConnect()') # 로그인
        self.login_event_loop = QEventLoop() # 이벤트루프
        self.login_event_loop.exec_() # 이벤트 발생까지 종료되지 않음.

    def _event_connect(self, err_code):
        if err_code == 0: # 에러 없다면,
            print('Connected')
        else: # 에러 있다면
            print('Disconnected')
        
        self.login_event_loop.exit() # 이벤트 발생 후 이벤트루프를 종료시킴

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall('GetCodeListByMarket(QString)',market)
        code_list = code_list.split(';') # ;를 구분자로 종목코드 리스트생성
        return code_list[:-1] # 리스트 마지막은 공백(;구분자로 나눴기 때문)

    def get_master_code_name(self, code):
        code_name = self.dynamicCall('GetMasterCodeName(QString)',code)
        return code_name

if __name__ == '__main__':
    # 앱생성
    app = QApplication(sys.argv)
    kiwoom = Kiwoom() # API 연결
    kiwoom.comm_connect() # 로그인 및 이벤트루프 생성 -> 연결상태 반환(event_connect)
    code_list = kiwoom.get_code_list_by_market('10') # 종목코드 전체
    print('sample code : ', code_list[0])
    code_name = kiwoom.get_master_code_name(code_list[0])
    print('sample code name : ', code_name)