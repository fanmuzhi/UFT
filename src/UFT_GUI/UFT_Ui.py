# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UFT_Ui.ui'
#
# Created: Wed Nov 26 14:08:45 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1036, 722)
        Form.setMinimumSize(QtCore.QSize(0, 722))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Narrow"))
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.info = QtGui.QWidget()
        self.info.setObjectName(_fromUtf8("info"))
        self.gridLayout_2 = QtGui.QGridLayout(self.info)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.sn_lineEdit_1 = QtGui.QLineEdit(self.groupBox)
        self.sn_lineEdit_1.setText(_fromUtf8(""))
        self.sn_lineEdit_1.setObjectName(_fromUtf8("sn_lineEdit_1"))
        self.verticalLayout.addWidget(self.sn_lineEdit_1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_4 = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.sn_lineEdit_2 = QtGui.QLineEdit(self.groupBox_4)
        self.sn_lineEdit_2.setObjectName(_fromUtf8("sn_lineEdit_2"))
        self.verticalLayout_9.addWidget(self.sn_lineEdit_2)
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_9.addWidget(self.label_3)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.groupBox_3 = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.sn_lineEdit_3 = QtGui.QLineEdit(self.groupBox_3)
        self.sn_lineEdit_3.setObjectName(_fromUtf8("sn_lineEdit_3"))
        self.verticalLayout_8.addWidget(self.sn_lineEdit_3)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_8.addWidget(self.label_4)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.sn_lineEdit_4 = QtGui.QLineEdit(self.groupBox_2)
        self.sn_lineEdit_4.setObjectName(_fromUtf8("sn_lineEdit_4"))
        self.verticalLayout_7.addWidget(self.sn_lineEdit_4)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_7.addWidget(self.label_5)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.start_pushButton = QtGui.QPushButton(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_pushButton.sizePolicy().hasHeightForWidth())
        self.start_pushButton.setSizePolicy(sizePolicy)
        self.start_pushButton.setObjectName(_fromUtf8("start_pushButton"))
        self.horizontalLayout.addWidget(self.start_pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.groupBox_5 = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.imageLabel = QtGui.QLabel(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setMinimumSize(QtCore.QSize(400, 400))
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.gridLayout_7.addWidget(self.imageLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout_6.addWidget(self.groupBox_5, 0, 1, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(self.info)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.info_textBrowser = QtGui.QTextBrowser(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_textBrowser.sizePolicy().hasHeightForWidth())
        self.info_textBrowser.setSizePolicy(sizePolicy)
        self.info_textBrowser.setAutoFillBackground(True)
        self.info_textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.info_textBrowser.setObjectName(_fromUtf8("info_textBrowser"))
        self.gridLayout_8.addWidget(self.info_textBrowser, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.tabWidget.addTab(self.info, _fromUtf8(""))
        self.charts = QtGui.QWidget()
        self.charts.setObjectName(_fromUtf8("charts"))
        self.gridLayout_3 = QtGui.QGridLayout(self.charts)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioButton = QtGui.QRadioButton(self.charts)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.buttonGroup = QtGui.QButtonGroup(Form)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radioButton)
        self.horizontalLayout_3.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.charts)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.buttonGroup.addButton(self.radioButton_2)
        self.horizontalLayout_3.addWidget(self.radioButton_2)
        self.radioButton_3 = QtGui.QRadioButton(self.charts)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.buttonGroup.addButton(self.radioButton_3)
        self.horizontalLayout_3.addWidget(self.radioButton_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.groupBox_7 = QtGui.QGroupBox(self.charts)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_10 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.mplwidget = MatplotlibWidget(self.groupBox_7)
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.gridLayout_10.addWidget(self.mplwidget, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_7, 1, 0, 1, 1)
        self.groupBox_8 = QtGui.QGroupBox(self.charts)
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout_11 = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.mplwidget_2 = MatplotlibWidget(self.groupBox_8)
        self.mplwidget_2.setObjectName(_fromUtf8("mplwidget_2"))
        self.gridLayout_11.addWidget(self.mplwidget_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_8, 1, 1, 1, 1)
        self.groupBox_9 = QtGui.QGroupBox(self.charts)
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.gridLayout_12 = QtGui.QGridLayout(self.groupBox_9)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.mplwidget_3 = MatplotlibWidget(self.groupBox_9)
        self.mplwidget_3.setObjectName(_fromUtf8("mplwidget_3"))
        self.gridLayout_12.addWidget(self.mplwidget_3, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_9, 2, 0, 1, 1)
        self.groupBox_10 = QtGui.QGroupBox(self.charts)
        self.groupBox_10.setObjectName(_fromUtf8("groupBox_10"))
        self.gridLayout_13 = QtGui.QGridLayout(self.groupBox_10)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.mplwidget_4 = MatplotlibWidget(self.groupBox_10)
        self.mplwidget_4.setObjectName(_fromUtf8("mplwidget_4"))
        self.gridLayout_13.addWidget(self.mplwidget_4, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_10, 2, 1, 1, 1)
        self.tabWidget.addTab(self.charts, _fromUtf8(""))
        self.configuration = QtGui.QWidget()
        self.configuration.setObjectName(_fromUtf8("configuration"))
        self.gridLayout_9 = QtGui.QGridLayout(self.configuration)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.partNum_comboBox = QtGui.QComboBox(self.configuration)
        self.partNum_comboBox.setObjectName(_fromUtf8("partNum_comboBox"))
        self.gridLayout_4.addWidget(self.partNum_comboBox, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.configuration)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Unicode MS"))
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.configuration)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 0, 1, 1, 1)
        self.revision_comboBox = QtGui.QComboBox(self.configuration)
        self.revision_comboBox.setObjectName(_fromUtf8("revision_comboBox"))
        self.gridLayout_4.addWidget(self.revision_comboBox, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.configuration)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Unicode MS"))
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 0, 2, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.configuration)
        self.descriptionLabel.setText(_fromUtf8(""))
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout_4.addWidget(self.descriptionLabel, 1, 2, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.test_item_tableView = QtGui.QTableView(self.configuration)
        self.test_item_tableView.setObjectName(_fromUtf8("test_item_tableView"))
        self.gridLayout_9.addWidget(self.test_item_tableView, 1, 0, 1, 1)
        self.submit_pushButton = QtGui.QPushButton(self.configuration)
        self.submit_pushButton.setObjectName(_fromUtf8("submit_pushButton"))
        self.gridLayout_9.addWidget(self.submit_pushButton, 2, 0, 1, 1)
        self.tabWidget.addTab(self.configuration, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.search_lineEdit = QtGui.QLineEdit(self.tab)
        self.search_lineEdit.setInputMask(_fromUtf8(""))
        self.search_lineEdit.setObjectName(_fromUtf8("search_lineEdit"))
        self.horizontalLayout_2.addWidget(self.search_lineEdit)
        self.search_pushButton = QtGui.QPushButton(self.tab)
        self.search_pushButton.setObjectName(_fromUtf8("search_pushButton"))
        self.horizontalLayout_2.addWidget(self.search_pushButton)
        self.search_result_label = QtGui.QLabel(self.tab)
        self.search_result_label.setText(_fromUtf8(""))
        self.search_result_label.setObjectName(_fromUtf8("search_result_label"))
        self.horizontalLayout_2.addWidget(self.search_result_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.log_tableView = QtGui.QTableView(self.tab)
        self.log_tableView.setMinimumSize(QtCore.QSize(994, 0))
        self.log_tableView.setMaximumSize(QtCore.QSize(994, 16777215))
        self.log_tableView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.log_tableView.setObjectName(_fromUtf8("log_tableView"))
        self.gridLayout_5.addWidget(self.log_tableView, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.sn_lineEdit_1, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.sn_lineEdit_2.setFocus)
        QtCore.QObject.connect(self.sn_lineEdit_2, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.sn_lineEdit_3.setFocus)
        QtCore.QObject.connect(self.sn_lineEdit_3, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.sn_lineEdit_4.setFocus)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "AGIGA CORONADO PGEM UFT V1.0", None))
        self.groupBox.setTitle(_translate("Form", "Slot #1", None))
        self.sn_lineEdit_1.setPlaceholderText(_translate("Form", "Serial Number", None))
        self.label_2.setText(_translate("Form", "Test Result", None))
        self.groupBox_4.setTitle(_translate("Form", "Slot #2", None))
        self.sn_lineEdit_2.setPlaceholderText(_translate("Form", "Serial Number", None))
        self.label_3.setText(_translate("Form", "Test Result", None))
        self.groupBox_3.setTitle(_translate("Form", "Slot #3", None))
        self.sn_lineEdit_3.setPlaceholderText(_translate("Form", "Serial Number", None))
        self.label_4.setText(_translate("Form", "Test Result", None))
        self.groupBox_2.setTitle(_translate("Form", "Slot #4", None))
        self.sn_lineEdit_4.setPlaceholderText(_translate("Form", "Serial Number", None))
        self.label_5.setText(_translate("Form", "Test Result", None))
        self.start_pushButton.setText(_translate("Form", "START", None))
        self.groupBox_5.setTitle(_translate("Form", "item picture", None))
        self.imageLabel.setText(_translate("Form", "TextLabel", None))
        self.groupBox_6.setTitle(_translate("Form", "info", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.info), _translate("Form", "test", None))
        self.radioButton.setText(_translate("Form", "vin", None))
        self.radioButton_2.setText(_translate("Form", "vcap", None))
        self.radioButton_3.setText(_translate("Form", "temp", None))
        self.groupBox_7.setTitle(_translate("Form", "dut #1", None))
        self.groupBox_8.setTitle(_translate("Form", "dut #2", None))
        self.groupBox_9.setTitle(_translate("Form", "dut #3", None))
        self.groupBox_10.setTitle(_translate("Form", "dut #4", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.charts), _translate("Form", "charts", None))
        self.label_6.setText(_translate("Form", "Part Number: ", None))
        self.label_8.setText(_translate("Form", "Revision: ", None))
        self.label_7.setText(_translate("Form", "Description: ", None))
        self.submit_pushButton.setText(_translate("Form", "submit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configuration), _translate("Form", "configuration", None))
        self.search_lineEdit.setPlaceholderText(_translate("Form", "search by serial number", None))
        self.search_pushButton.setText(_translate("Form", "Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "test log", None))

from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

