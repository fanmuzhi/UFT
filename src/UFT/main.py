#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''

import sys
from PyQt4.QtGui import QApplication
from UFT import MainWidget

__author__ = "mzfa"
__version__ = "1.0"
__email__ = "mzfa@cypress.com"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())