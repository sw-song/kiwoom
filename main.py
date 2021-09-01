from kiwoom import Kiwoom
import sys
from PyQt5.QtWidgets import QApplication



if __name__ == "__main__":
    print('==Program Start==')
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    kiwoom.get_condition_load()
    kiwoom.send_condition('0','결산이격도',0,0)
    app.exec_()