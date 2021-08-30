from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__() # == QAxWidget.__init__()
        print('api connected')

        #_____event loop______#
        self.login_event_loop = QEventLoop() # event loop start - for login
        self.detail_account_info_event_loop = QEventLoop()

        #_____account_rel_____#
        self.account_stock_dict = {}
        self.not_signed_stock_dict = {}
        self.account_num = None
        self.deposit = 0 # 예수금
        self.use_money = 0
        self.use_money_percent = 0.5
        self.output_deposit = 0
        self.total_profit_loss_money = 0 # 총평가손익금액
        self.total_profit_loss_rate = 0.0 # 총수익률(%)

        #_____screen num______#
        self.screen_my_info="2000"

        #_____initial setting___#
        self.get_ocx_instance() # 1. api를 컨트롤하겠다.
        self.event_slots() # 2. event slot들을 만들어주자.
        self.signal_login_commConnect() # 3. login을 요청한다.
        self.get_account_info() # 4. 계좌번호를 출력한다.
        self.detail_account_info() # 5. 예수금 요청 시그널
        self.detail_account_mystock() # 6. 계좌평가잔고내역을 불러온다.
        QTimer.singleShot(3500, self.not_concluded_account) # 7. 3.5초 뒤 미체결 종목 불러오기.

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
            self.detail_account_info_event_loop.exit()

        elif sRQName == '계좌평가잔고내역요청':
            total_buy_money = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, 0, '총매입금액')
            self.total_buy_money = int(total_buy_money)
            total_profit_loss_money = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                                        sTrCode, sRQName, 0, '총평가손익금액')
            self.total_profit_loss_money = int(total_profit_loss_money)
            total_profit_loss_rate = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                                        sTrCode, sRQName, 0, '총수익률(%)')
            self.total_profit_loss_rate = float(total_profit_loss_rate)
            print('[계좌평가잔고내역요청(싱글)]\n총매입액: {}\n총평가손익:{}\n총수익률(%):{}'.format(\
                self.total_buy_money, self.total_profit_loss_money, self.total_profit_loss_rate ))                                            
            
            # 보유종목 수 가져오기
            rows = self.dynamicCall('GetRepeatCnt(QString, QString)',sTrCode, sRQName) # 최대 20개
            for i in range(rows):
                code = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                        sTrCode, sRQName, i, '종목번호') # 보유 종목의 종목코드를 순서대로 불러온다
                code = code.strip()[1:]
                code_name = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '종목명')
                count_stock = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '보유수량')
                buy_price = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '매입가')
                profit_rate = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '수익률(%)'),
                current_price = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '현재가'),
                total_buy_price = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '매입금액')
                count_can_sell_stock = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                                            sTrCode, sRQName, i, '매매가능수량')
                print('[보유종목정보(멀티)]\n종목번호: {}\n종목명: {}\n보유수량: {}\n매입가: {}\n수익률(%): {}\n현재가: {}\n매입금액: {}\n매매가능수량: {}')
                
                
                if self.not_signed_stock_dict[code]:
                    pass
                else:
                    self.account_stock_dict[code]={}
                    self.account_stock_dict[code].update({
                                                      'name':code_name,
                                                      'count':count_stock,
                                                      'buy_price':buy_price,
                                                      'profit_rate':profit_rate,
                                                      'current_price':current_price,
                                                      'total_buy_price':total_buy_price,
                                                      'count_sell':count_can_sell_stock                
                                                      })
                    print('보유 종목 : {}({})'.format(code_name,code))

            if sPrevNext == '2':
                print('현재 조회한 종목 수 : 20')
                print('다음 페이지를 조회합니다')
                self.detail_account_mystock(sPrevNext='2')
            else:
                print('현재 조회한 종목 수 : {}'.format(rows))
                print('최종페이지입니다.')
                self.detail_account_info_event_loop.exit()

        elif sRQName == '실시간미체결요청':
            rows = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)

            for i in range(rows):
                code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '종목코드')
                code_name = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '종목명')
                order_no = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '주문번호')
                order_status = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '주문상태')
                order_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '주문수량')
                order_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '주문가격')
                order_sector = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '주문구분')
                not_signed_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '미체결수량')
                ok_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, i, '체결량')

                code = code.strip()
                code_name = code_name.strip()
                order_no = order_no.strip()
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                order_sector = order_sector.strip().lstrip('+').lstrip('-')
                not_signed_quantity = int(not_signed_quantity.strip())
                ok_quantity = int(ok_quantity.strip())

                if order_no in self.not_signed_stock_dict:
                    pass
                else:
                    self.not_signed_stock_dict[order_no]={}
                    self.not_signed_stock_dict[order_no].update({
                        'code':code,
                        'code_name':code_name,
                        'order_status':order_status,
                        'order_quantity':order_quantity,
                        'order_price':order_price,
                        'order_sector':order_sector,
                        'not_signed_quantity':not_signed_quantity,
                        'ok_quantity':ok_quantity
                    })
                    print('미체결 종목 : {}(주문번호:{})'.format(code_name, order_no))

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

    def detail_account_mystock(self, sPrevNext='0'): #싱글데이터
        self.dynamicCall('SetInputValue(QString, QString)', '계좌번호', self.account_num)
        self.dynamicCall('SetInputValue(QString, QString)', '비밀번호', '0000') # 모의투자 공통 0000
        self.dynamicCall('SetInputValue(QString, QString)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(QString, QString)', '조회구분', '1') # 1:합산, 2:개별
        self.dynamicCall('CommRqData(QString, QString, int, QString)', '계좌평가잔고내역요청', 'opw00018', sPrevNext, self.screen_my_info)
        self.detail_account_info_event_loop.exec_()

    def not_concluded_account(self, sPrevNext='0'):
        print('미체결 종목 요청중..')
        self.dynamicCall('SetInputValue(QString, QString)', '계좌번호', self.account_num)
        self.dynamicCall('SetInputValue(QString, QString)', '체결구분', '1')
        self.dynamicCall('SetInputValue(QString, QString)', '매매구분', '0')
        self.dynamicCall('CommRqData(QString, QString, int, QString)',
                        '실시간미체결요청','opt10075', sPrevNext, self.screen_my_info)
        self.detail_account_info_event_loop.exec_()