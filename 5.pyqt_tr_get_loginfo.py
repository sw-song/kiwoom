import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 키움 api 연결
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # api로 로그인
        self.kiwoom.dynamicCall('CommConnect()')
        # api로 연결 상태 확인
        self.kiwoom.OnEventConnect.connect(self.event_connect)


        # UI 구성
        ## UI - window
        self.setWindowTitle('PyStock')
        self.setGeometry(300,300,300,150)
        ## UI - button
        btn = QPushButton('Get Account', self)
        btn.move(190,20)
        btn.clicked.connect(self.btn_clicked)
        ## UI - text
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10,60,280,80)
        self.text_edit.setEnabled(False)

    def btn_clicked(self):
        account_num = self.kiwoom.dynamicCall('GetLoginInfo(QString)', ['ACCNO'])
        self.text_edit.append('account number : '+account_num)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append('Login Success')
        else:
            self.text_edit.append('Login Failed')


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()