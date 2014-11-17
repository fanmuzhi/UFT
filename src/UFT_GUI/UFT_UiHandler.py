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

class UFT_UiHandler(UFT_UiForm):
    def __init__(self, parent=None):
        UFT_UiForm.__init__(self)
    

    
if __name__ == "__main__":
    a=QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    
    w=UFT_UiForm()
    w.setupUi(Form)
    view = w.tableView
    Form.show()   
    sys.exit(a.exec_())  
