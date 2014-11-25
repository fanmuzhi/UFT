#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2014
@author: mzfa
'''
import sys
import time
from PyQt4 import QtCore, QtGui
from UFT_GUI.UFT_Ui import Ui_Form as UFT_UiForm
import log_handler
import mpl_handler
import sql_handler


class UFT_UiHandler(UFT_UiForm):
    def __init__(self, parent=None):
        UFT_UiForm.__init__(self)
        self.dut_image = None
        self.config_table = QtGui.QTableView()
        log_handler.XStream.stdout().messageWritten.connect(self.__append_format_data)
        self.my_db = sql_handler.MyDB()
        self.config_model = None
        self.test_item_model = None

    def setupWidget(self, wobj):
        wobj.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("./res/icons/logo.png")))
        ''' initial configuration tab combobox and table  '''
        self.my_db.switch_to_configuration()
        self.config_model = sql_handler.TableModel(self.config_table, "configuration")
        self.test_item_model = sql_handler.RelationModel(self.test_item_tableView,
                                                         "test_item",
                                                         1,
                                                         "configuration",
                                                         "CONFIGID")
        self.__popComboBox(self.partNum_comboBox, self.config_model, "PARTNUMBER")
        self.test_item_tableView.setModel(self.test_item_model)
        self.testItem_update()
        ''''''

    def __append_format_data(self, data):
        self.info_textBrowser.insertPlainText(time.strftime("%Y-%m-%d %X\t") + data)
        self.info_textBrowser.moveCursor(QtGui.QTextCursor.End)

    def show_image(self, image):
        my_pixmap = QtGui.QPixmap(image)
        my_scaled_pixmap = my_pixmap.scaled(self.imageLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(my_scaled_pixmap)

    def __popComboBox(self, combobox, model, column):
        combobox.setModel(model)
        combobox.setModelColumn(model.fieldIndex(column))

    def comboBox_update(self):
        config = sql_handler.TableModel(self.config_table, "configuration")
        current_pn = self.partNum_comboBox.currentText()
        config.setFilter("PARTNUMBER='" + current_pn + "'")
        self.__popComboBox(self.revision_comboBox, config, "REVISION")

    def update_table(self):
        self.my_db.switch_to_configuration()
        config1 = sql_handler.TableModel(self.config_table, "configuration")
        filter_combo = "PARTNUMBER = '" + self.partNum_comboBox.currentText() + \
                       "' AND REVISION = '" + self.revision_comboBox.currentText() + "'"
        config1.setFilter(filter_combo)
        config1.select()
        config_id = config1.record(0).value('ID').toString()
        description = config1.record(0).value('DESCRIPTION').toString()
        self.descriptionLabel.setText(description)
        # self.test_item_model = sql_handler.RelationModel(None,
        # "test_item",
        # 1,
        #                                                  "configuration",
        #                                                  "CONFIGID")
        self.test_item_model.setFilter("CONFIGID = " + config_id)
        self.test_item_model.select()

    def testItem_update(self):
        self.my_db.switch_to_configuration()
        self.comboBox_update()
        self.update_table()

    def submit_config(self):
        self.my_db.switch_to_configuration()
        for i in range(self.test_item_model.rowCount()):
            record = self.test_item_model.record(i)
            self.test_item_model.setRecord(i, record)
        self.test_item_model.submitAll()

    def get_log_data(self, barcodes):
        self.my_db.switch_to_pgem()
        data_table = QtGui.QTableView()
        test_log_model = sql_handler.RelationModel(data_table,
                                                   "cycle",
                                                   5,
                                                   "dut",
                                                   "id",
                                                   u"barcode")
        test_log_model.setFilter("barcode IN ('" + "', ".join(barcodes) + "')")
        test_log_model.select()
        return test_log_model

    def search(self):
        if self.search_lineEdit.text():
            barcodes = []
            barcodes.append(str(self.search_lineEdit.text()))
            test_log_model = self.get_log_data(barcodes)
            self.log_tableView.setModel(test_log_model)

    def push_mpl(self, mpl_widget, barcodes=["AGIGA9811-001BCA02143500000001-01"]):
        for barcode in barcodes:
            mpl_data_model = self.get_log_data(barcodes)
            mpl_widget.setFocus()
            mpl_handler.plot(self.mplwidget.axes)


if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    w = UFT_UiHandler()
    w.setupUi(Form)
    w.setupWidget(Form)
    w.show_image("../res/icons/despicableMe.jpg")
    Form.show()
    sys.exit(a.exec_())  
