#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2013
@author: mzfa
'''

import time
from PyQt4.QtGui import QKeySequence, QIcon, QPixmap
from PyQt4.QtCore import Qt
from UFT_Ui import Ui_Form as UFT_UIForm

class UFT_UiHandler(UFT_UIForm):
    def __init__(self, parent=None):
        UFT_UIForm.__init__(self)
    
