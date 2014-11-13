#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''

from PyQt4 import QtGui, QtCore
from UFT_UiHandler import UFT_UiHandler

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = UFT_UiHandler()
        self.ui.setupUi(self)
