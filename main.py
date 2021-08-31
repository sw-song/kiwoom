from kiwoom.kiwoom import Kiwoom
import sys # system - specific parameters and functions
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print('Main() class call')
        
        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom() 
        self.app.exec_() # event loop(프로그램 종료하지 않고, 동시성 지원)

if __name__ == "__main__":
    Main()