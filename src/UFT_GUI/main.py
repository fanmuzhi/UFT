#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2014
@author: mzfa
'''
__author__ = "mzfa"
__version__ = "1.0"
__email__ = "mzfa@cypress.com"

import sys
from PyQt4.QtGui import QApplication
from PyQt4 import QtGui, QtCore
from UFT_GUI.handlers.UFT_UiHandler import UFT_UiHandler
from UFT_GUI.handlers import log_handler, sql_handler

import UFT
import logging
from UFT.channel import Channel, ChannelStates
import time


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = UFT_UiHandler()
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.__setupSignal()

    def __setupSignal(self):
        '''start_pushButton for log display test,
        to be changed as "start" function later'''
        self.ui.start_pushButton.clicked.connect(start_click)
        self.ui.show_image("./res/icons/despicableMe.jpg")
        self.ui.partNum_comboBox.currentIndexChanged.connect(
            self.ui.testItem_update)
        self.ui.revision_comboBox.currentIndexChanged.connect(
            self.ui.update_table)
        self.ui.submit_pushButton.clicked.connect(self.ui.submit_config)
        self.ui.search_lineEdit.returnPressed.connect(self.ui.search)
        self.ui.search_pushButton.clicked.connect(self.ui.search)
        self.ui.buttonGroup.buttonClicked.connect(self.ui.push_multi_mpls)

def start_click():
    handler = log_handler.QtHandler()
    UFT.logger.addHandler(handler)
    UFT.logger.setLevel(logging.DEBUG)

    UFT.logger.debug("clicked.")

    barcode = "AGIGA9601-002BCA02143500000002-04"
    ch = Channel(barcode_list=[barcode, "", "", ""], channel_id=0,
                 name="UFT_CHANNEL")
    ch.start()

    ch.queue.put(ChannelStates.INIT)
    ch.queue.put(ChannelStates.CHARGE)
    ch.queue.put(ChannelStates.PROGRAM_VPD)
    ch.queue.put(ChannelStates.CHECK_ENCRYPTED_IC)
    ch.queue.put(ChannelStates.LOAD_DISCHARGE)
    ch.queue.put(ChannelStates.EXIT)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()