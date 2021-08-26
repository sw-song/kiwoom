import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QCoreApplication

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 키움증권 로그인
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall('CommConnect()') # 로그인요청

        # 연결한 api 사용
        self.kiwoom.OnEventConnect.connect(self.event_connect) # 로그인하면 에러코드 반환하는 api와 연결
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata) # TR요청하는 api와 연결

        # UI 구성
        # UI - Window
        self.setWindowTitle('PyStock')
        self.setGeometry(300,300,300,150)
        # UI - 화면 텍스트
        label = QLabel('code: ', self)
        label.move(20,20)
        # UI - 입력창
        self.code_edit = QLineEdit(self)
        self.code_edit.move(80,20)
        self.code_edit.setText('039490')
        # UI - 버튼
        btn = QPushButton('click',self)
        btn.move(190,20)
        btn.clicked.connect(self.btn_clicked)
        # UI - 텍스트상자
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10,60,280,80)
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("login success")
        else:
            self.text_edit.append("login failed")

    def btn_clicked(self):
        code = self.code_edit.text() # 입력창에서 입력받은 텍스트 할당
        self.text_edit.append('code: '+code) # 텍스트박스에 입력한 텍스트 표기

        # api 사용(SetInputValue : 입력데이터설정, 데이터타입을 파라미터로 입력)
        self.kiwoom.dynamicCall('SetInputValue(QString,QString)', '종목코드', code) # 종목코드 : 앞에서 입력한 종목코드
        # api 사용(CommRqData : TR 전송, 데이터타입을 파라미터로 입력)
        self.kiwoom.dynamicCall('CommRqData(QString,QString,int,QString)', 'opt10001_req','opt10001',0,'0101')

    # OnReceiveTrData 이벤트 발생시 동작.
    # OnReceiveTrData 이벤트가 발생했다는 것은 TR요청에 응답했다는 것
    # 따라서 아래 함수에서는 돌려주는 데이터를 받아야한다.
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == 'opt10001_req':
            name = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)',
                                           trcode, "", rqname, 0, '종목명')
            volume = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)',
                                             trcode, "", rqname, 0, '거래량')

            # 받은 데이터 텍스트상자에 표시
            self.text_edit.append('종목명: '+name.strip())
            self.text_edit.append('거래량: '+volume.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

        
