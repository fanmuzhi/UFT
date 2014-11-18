#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''
__author__ = "mzfa"
__version__ = "1.0"
__email__ = "mzfa@cypress.com"

import sys
from PyQt4.QtGui import QApplication
from PyQt4 import QtGui, QtCore
from UFT_GUI.handlers.UFT_UiHandler import UFT_UiHandler
from UFT_GUI.handlers import log_handler

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = UFT_UiHandler()
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.__setupSignal()
        
    def __setupSignal(self):
        '''for log display test, to be changed as "start" function later'''
        self.ui.start_pushButton.clicked.connect(log_handler.test)
        
        
def main():
    app = QApplication(sys.argv)
    app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()