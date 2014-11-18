#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''
import sys
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QKeySequence, QIcon, QPixmap
from PyQt4.QtCore import Qt
from UFT_GUI.UFT_Ui import Ui_Form as UFT_UiForm

import log_handler
import mpl_handler
import sql_handler

class UFT_UiHandler(UFT_UiForm):
    def __init__(self, parent=None):
        UFT_UiForm.__init__(self)
        log_handler.XStream.stdout().messageWritten.connect(self.__append_formatData)
        
    def setupWidget(self, wobj):
        wobj.setWindowIcon(QIcon(QPixmap("./res/icons/logo.png")))
        
        
    def __append_formatData(self, data):
        self.info_textBrowser.insertPlainText(time.strftime("%Y-%m-%d %X\t")+data)
        self.info_textBrowser.moveCursor(QtGui.QTextCursor.End)
        
    
    
if __name__ == "__main__":
    a=QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    w=UFT_UiHandler()
    w.setupUi(Form)
    w.setupWidget(Form)
    Form.show()   
    sys.exit(a.exec_())  
