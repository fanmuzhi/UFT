#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''

import time
from PyQt4.QtGui import QKeySequence, QIcon, QPixmap
from PyQt4.QtCore import Qt
from UFT import UFT_Ui as UI

class UFT_UiHandler(UFT_UIForm):
    def __init__(self, parent=None):
        UI.Ui_Form.__init__(self)
    
