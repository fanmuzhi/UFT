# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UFT.ui'
#
# Created: Mon Oct 13 10:11:56 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
from pyaardvark import Adapter
from logger import logger


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.message=""

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(477, 426)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btn_ClickMe = QtGui.QPushButton(Form)
        self.btn_ClickMe.setObjectName(_fromUtf8("btn_ClickMe"))
        self.btn_ClickMe.clicked.connect(self.clickme)

        self.verticalLayout_2.addWidget(self.btn_ClickMe)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "UFT_TestExecutive", None))
        #self.plainTextEdit.setPlainText(_translate("Form", "Hello~", None))
        self.btn_ClickMe.setText(_translate("Form", "ClickMe", None))

    def clickme(self):
        adapter = Adapter(bitrate=400)
        devices =  adapter.find_devices()
        if devices > 0:
            adapter.open(portnum=0)
            self.message += "Find device: " + adapter.unique_id_str() + "\n"
        else:
            self.message += "No device found." + "\n"
        self.plainTextEdit.setPlainText(self.message)
        adapter.close()


if __name__ == "__main__":
    logger.info("hello mzfa!")
    logger.debug("debug")
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())
