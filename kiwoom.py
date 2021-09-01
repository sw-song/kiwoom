from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from config.slack import Slack

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self._slack = Slack()

###############################
#__init__ 호출
    def _create_kiwoom_instance(self): # api controller
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        print('api connected')

    def _set_signal_slots(self): # slot : get api's response 
        self.OnEventConnect.connect(self._event_connect)
        # 조건검색
        self.OnReceiveConditionVer.connect(self._receive_condition_ver)
        self.OnReceiveTrCondition.connect(self._receive_tr_condition)
        self.OnReceiveRealCondition.connect(self._receive_real_condition)
        
#_set_signal_slots 호출
    def _event_connect(self, err_code):
        """
        :err_code::int: 반환된 에러코드 (0-에러 없음)
        """
        if not err_code: # == not 0 == 에러 없음
            print('login success')
        else:
            print('login failed')
        
        self.login_event_loop.exit() # [로그인 이벤트 루프] 해제


    def _receive_condition_ver(self, result, msg):
        """
        :result::int: 응답결과 (1-성공) 
        :msg::str: 메세지(사용x)
        """
        try:
            if not result: # 응답 받지 못함
                print('cannot get response <- getConditionLoad()')
            else: # 응답 받음
                self.condition = self.get_condition_name_list()
                
                print('보유 조건식 수 : {}'.format(len(self.condition)))

                for key in self.condition.keys():
                    print('(고유번호-{}) 조건식 : {}'.format(key, self.condition[key]))

        except Exception as e: # 에러 발생시
            print(e)
        
        finally:
            self.condition_loop.exit() # [조건조회 이벤트 루프] 해제
    
    def _receive_tr_condition(self, screenNo, codes, conName, conIdx, next):
        """
        :screenNo:str:: 스크린번호
        :codes:str:: 종목코드 목록(구분자 ';')  
        :conName:str:: 조건식이름
        :conIdx:int:: 조건식index
        :next:int:: 조회구분(0-현재 최종페이지, 2-다음페이지 있음) 
        """
        try:
            if not codes: # 조건식 해당 종목 없음
                print('종목 없음')
            else: # 조건식 해당 종목 있음
                codeList = codes.split(';')[:-1]
                for code in codeList:
                    code_name = self.get_master_code_name(code)
                    message = '[조건식 통과 조회(비실시간)] 종목코드 : {}, 종목명 {}'.format(code, code_name)
                    print('[to slack] {}'.format(message))
                    self._slack.notification(text=message)
        finally:
            self.condition_loop.exit()
        
    def _receive_real_condition(self, code, eType, conName, conIdx):
        """
        :code:str:: 종목코드
        :eType:str:: 이벤트유형('I'-종목편입 / 'D'-종목이탈) 
        :conName:str:: 조건식이름
        :conIdx:str:: 조건식Index(*str 주의)
        """
        code_name = self.get_master_code_name(code)
        if eType == 'I':
            message = '[{}] 종목코드 : {}, 종목명 : {}'.format('종목편입', code, code_name)
        elif eType == 'D':
            message = '[{}] 종목코드 : {}, 종목명 : {}'.format('종목이탈', code, code_name)
        else:
            print('No record about this eType - {}'.format(eType))
        print('[슬랙 알림 발송]')
        self._slack.notification(text=message)



################################# 
# 외부(main) 호출 함수 
    def comm_connect(self):

        self.dynamicCall('CommConnect()')
        """
        수동 로그인설정인 경우 로그인창 출력.
        자동로그인 설정인 경우 로그인창에서 자동 로그인
        """
        self.login_event_loop = QEventLoop() # [로그인 이벤트 루프] 생성
        self.login_event_loop.exec_() # [로그인 이벤트 루프] 유지 - 응답까지 대기


    def get_condition_load(self):

        isLoad = self.dynamicCall('GetConditionLoad()')
        """
        서버에 저장된 사용자 조건검색 목록을 요청합니다. 
        조건검색 목록을 모두 수신하면 OnReceiveConditionVer()이벤트가 발생됩니다.
        조건검색 목록 요청을 성공하면 1, 아니면 0을 리턴합니다.
        """
        if not isLoad: # 조건검색 목록 요청 실패 (1==True, 0==False, isLoad가 0일때만 실행)
            print('조건검색 목록 요청 실패 - ## GetConditionLoad()')
        else: # 조건검색 요청 성공
            print('조건검색 목록 요청 성공')
            self.condition_loop = QEventLoop() # [조건검색 요청 이벤트 루프] 생성
            self.condition_loop.exec_() # [조건검색 요청 이벤트 루프] 유지 - 응답까지 대기

    def send_condition(self, screenNo, conName, conIdx, isRealTime):
        """
        :screenNo::str: 스크린번호
        :conName::str: 조건식 이름
        :conIdx::int: 조건식 index
        :isRealTime::int: 조건검색 조회구분(0-tr, 1-realtime)
        """
        isRequest = self.dynamicCall('SendCondition(QString, QString, int, int)', screenNo, conName, conIdx, isRealTime)
        
        if not isRequest:
            print('조건검색 요청 실패')

        else:    
            self.condition_loop = QEventLoop()
            self.condition_loop.exec_()


################################# 
# 기본 dynamicCall wrapping 함수
    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def send_condition_stop(self, screenNo, conName, conIdx):
        ret = self.dynamicCall('SendConditionStop(QString, QString, int)', screenNo, conName, conIdx)
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def get_condition_name_list(self):
        is_condition = self.dynamicCall('GetConditionNameList()')
        if not is_condition:
            print('조건식 없음')
        else:
            condition_list = is_condition.split(';')[:-1]
        
        condition_dict = {}
        for con in condition_list:
            key, val = con.split('^')
            condition_dict[int(key)] = val
        return condition_dict
        