from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__() # == QAxWidget.__init__()
        print('api connected')

        #_____event loop______#
        self.login_event_loop = QEventLoop() # event loop start - for login
        self.detail_account_info_event_loop = None

        #_____account_rel_____#
        self.account_num = None
        self.deposit = 0 # 예수금
        self.use_money = 0
        self.use_money_percent = 0.5
        self.output_deposit = 0

        #_____screen num______#
        self.screen_my_info="2000"

        #_____initial setting___#
        self.get_ocx_instance() # 1. api를 컨트롤하겠다.
        self.event_slots() # 2. event slot들을 만들어주자.
        self.signal_login_commConnect() # 3. login을 요청한다.
        self.get_account_info() # 4. 계좌번호를 출력한다.
        self.detail_account_info() # 5. 예수금 요청 시그널

    ##___api controller____##
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") #.ocx확장자로 저장된 키움 api를 파이썬으로 컨트롤하겠다.
        
    ##___group of event slots__##
    def event_slots(self): # slot : 이벤트 발생시 slot으로 데이터 회수
        self.OnEventConnect.connect(self.login_slot) # 로그인 요청에 대한 응답이 왔을때 응답을 받도록 연결해둠.
        self.OnReceiveTrData.connect(self.trdata_slot) # 트랜젝션 요청에 대한 응답이 왔을때 응답을 받도록 연결해둠.

    ###___slots__###
    def login_slot(self, err_code):
        print(errors(err_code)[1]) # 로그인 요청에 대한 응답이 오면 에러 코드 출력
        self.login_event_loop.exit() # 에러 코드 출력하고 로그인 이벤트 루프 종료.

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세현황요청':
            deposit = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                     sTrCode, sRQName, 0, '예수금')
        self.deposit = int(deposit)
        use_money = float(self.deposit)*self.use_money_percent
        self.use_money = int(use_money)
        self.use_money = self.use_money/4 # 4종목 이상 매수를 위함
        # 예수금
        output_deposit = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                        sTrCode, sRQName, 0, '예수금')
        self.output_deposit = int(output_deposit)
        print('예수금 : {}'.format(self.output_deposit))
        # 출금가능금액
        can_exit = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                         sTrCode, sRQName, 0, '출금가능금액')
        self.can_exit = int(can_exit)
        print('출금가능금액 : {}'.format(self.can_exit))
        self.stop_screen_cancel(self.screen_my_info)
        self.detail_account_info_event_loop.exit()


    ##_____request_login_____##
    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()") # login request signal
        self.login_event_loop.exec() ## 요청에 대해 응답이 올때까지 대기
    
    ##_____request_account____##
    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO") # request account number signal
        account_num = account_list.split(';')[1] # first account(모의투자 계좌)

        self.account_num = account_num
        print("account : {}".format(account_num))

    def detail_account_info(self, sPrevNext='0'): # 첫 조회 : sPrevNext='0'
        print('예수금 요청중..')
        self.dynamicCall('SetInputValue(QString, QString)','계좌번호', self.account_num)
        self.dynamicCall('SetInputValue(QString, QString)','비밀번호', '0000')
        self.dynamicCall('SetInputValue(QString, QString)','비밀번호입력매체구분','0000')
        self.dynamicCall('SetInputValue(QString, QString)','조회구분','1')
        self.dynamicCall('CommRqData(QString, QString, int, QString)',\
            '예수금상세현황요청','opw00001',sPrevNext, self.screen_my_info)
        self.detail_account_info_event_loop = QEventLoop()
        self.detail_account_info_event_loop.exec_()

    def stop_screen_cancel(self, sScrNo=None):
        self.dynamicCall('DisconnectRealData(QString)',sScrNo)