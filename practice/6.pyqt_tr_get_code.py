import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # api 연결
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # login
        self.kiwoom.dynamicCall('CommConnect()')

        # UI 구성
        ##UI - window
        self.setWindowTitle('PyStock')
        self.setGeometry(300,300,300,150)
        ##UI - button
        btn = QPushButton('Get Stock Code', self)
        btn.move(190,10)
        btn.clicked.connect(self.btn_clicked)
        ##UI - list (목록보기)
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10,10,170,130)

    def btn_clicked(self):
        # GetCodeListByMarket(sMarket) :: sMarket - 0:장내, 8:ETF, 10:코스닥
        ret = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)',['0'])
        kospi_code_list = ret.split(';') # delimeter ';' - 종목코드 저장
        kospi_code_name_list = []
        
        for c in kospi_code_list:
            name = self.kiwoom.dynamicCall('GetMasterCodeName(QString)',[c])
            kospi_code_name_list.append(c+' : '+name) # 'code : name' 형태로 각 종목 리스트화
        
        # UI-list에 '종목코드 : 종목명'으로 보여주기
        self.listWidget.addItems(kospi_code_name_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
