from kiwoom.tr_account import GetAccountInfo
#from kiwoom.tr_chart import GetChartInfo
#from kiwoom.realtime import GetRealTimeInfo
import sys # system - specific parameters and functions
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print('Main() class call')
        
        self.app = QApplication(sys.argv)
        self.account = GetAccountInfo() 
        #self.chart = GetChartInfo()
        #self.realtime = GetRealTimeInfo()
        self.app.exec_() # event loop(프로그램 종료하지 않고, 동시성 지원)

if __name__ == "__main__":
    Main()