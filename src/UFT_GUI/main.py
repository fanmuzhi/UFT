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
import logging
import time
from PyQt4.QtGui import QApplication
from PyQt4 import QtGui, QtCore
from UFT_GUI.handlers.UFT_UiHandler import UFT_UiHandler
from UFT_GUI.handlers import log_handler, sql_handler

try:
    import UFT
    from UFT.channel import Channel, ChannelStates
except Exception as e:
    print e.message


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.qtobj = QtCore.QObject()
        self.ui = UFT_UiHandler()
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.__setupSignal()

    def __setupSignal(self):
        '''start_pushButton for log display test,
        to be changed as "start" function later'''
        handler = log_handler.QtHandler()
        handler.setFormatter(UFT.formatter)
        UFT.logger.addHandler(handler)
        UFT.logger.setLevel(logging.INFO)
        log_handler.XStream.stdout().messageWritten.connect(
            self.ui.append_format_data)
        self.ui.start_pushButton.clicked.connect(self.start_click)
        self.ui.show_image("./res/icons/despicableMe.jpg")
        self.ui.partNum_comboBox.currentIndexChanged.connect(
            self.ui.testItem_update)
        self.ui.revision_comboBox.currentIndexChanged.connect(
            self.ui.update_table)
        self.ui.submit_pushButton.clicked.connect(self.ui.submit_config)
        self.ui.search_lineEdit.returnPressed.connect(self.ui.search)
        self.ui.search_pushButton.clicked.connect(self.ui.search)
        self.ui.buttonGroup.buttonClicked.connect(self.ui.push_multi_mpls)

    def start_click(self):
        # try:
        ch = Channel(barcode_list=self.ui.barcodes(), channel_id=0,
                     name="UFT_CHANNEL")
        ch.setDaemon(True)
        ch.queue.put(ChannelStates.INIT)
        ch.queue.put(ChannelStates.CHARGE)
        ch.queue.put(ChannelStates.PROGRAM_VPD)
        ch.queue.put(ChannelStates.CHECK_ENCRYPTED_IC)
        ch.queue.put(ChannelStates.CHECK_TEMP)
        ch.queue.put(ChannelStates.LOAD_DISCHARGE)
        ch.queue.put(ChannelStates.CHECK_CAPACITANCE)
        ch.queue.put(ChannelStates.EXIT)
        self.u = Update(ch)
        self.u.start()
        self.qtobj.connect(self.u, QtCore.SIGNAL('progress_bar'),
                           self.ui.progressBar.setValue)
        self.qtobj.connect(self.u, QtCore.SIGNAL('is_alive'),
                           self.ui.auto_enable_disable_widgets)
        self.qtobj.connect(self.u, QtCore.SIGNAL("dut_status"),
                           self.ui.set_status_text)


from UFT_GUI.test_elements import Progressbar


class Update(QtCore.QThread):
    def __init__(self, ch):
        QtCore.QThread.__init__(self)
        self.ch = ch

    def __del__(self):
        self.wait()

    def run(self):
        self.ch.start()
        while self.ch.isAlive():
            time.sleep(1)
            self.emit(QtCore.SIGNAL("progress_bar"), self.ch.progressbar)
            self.emit(QtCore.SIGNAL("is_alive"), self.ch.isAlive())
            for dut in self.ch.dut_list:
                self.emit(QtCore.SIGNAL("dut_status"), dut.slotnum, dut.status)

        self.emit(QtCore.SIGNAL("progress_bar"), self.ch.progressbar)
        for dut in self.ch.dut_list:
            self.emit(QtCore.SIGNAL("dut_status"), dut.slotnum, dut.status)

        self.emit(QtCore.SIGNAL("is_alive"), 0)
        self.terminate()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()