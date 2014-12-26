#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2014
@author: mzfa
'''
import sys
import os
import re
from PyQt4 import QtCore, QtGui, QtSql
from UFT_GUI.UFT_Ui import Ui_Form as UFT_UiForm
from UFT.config import RESULT_DB, CONFIG_DB

BARCODE_PATTERN = re.compile(
    r'(?P<SN>(?P<PN>AGIGA\d{4}-\d{3}\w{3})(?P<VV>\d{2})(?P<YY>[1-2][0-9])'
    r'(?P<WW>[0-4][0-9]|5[0-3])(?P<ID>\d{8})-(?P<RR>\d{2}))')


class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)

    def focusInEvent(self, event):
        #print 'This widget is in focus'
        self.clear()
        QtGui.QLineEdit.focusInEvent(self,
                                     QtGui.QFocusEvent(QtCore.QEvent.FocusIn))


class UFT_UiHandler(UFT_UiForm):
    def __init__(self, parent=None):
        UFT_UiForm.__init__(self)
        self.dut_image = None

        # setup config db, view and model
        self.config_db = QtSql.QSqlDatabase.addDatabase("QSQLITE", "config")
        self.config_db.setDatabaseName(CONFIG_DB)
        self.config_db.open()
        self.config_tableView = QtGui.QTableView()
        # self.test_item_tableView already created in UI.
        self.config_model = QtSql.QSqlTableModel(db=self.config_db)
        self.test_item_model = QtSql.QSqlRelationalTableModel(db=self.config_db)

        # setup log db, view and model
        self.log_db = QtSql.QSqlDatabase.addDatabase("QSQLITE", "log")
        self.log_db.setDatabaseName(RESULT_DB)
        self.log_db.open()
        # self.log_tableView
        self.log_model = QtSql.QSqlTableModel(db=self.log_db)
        self.cycle_model = QtSql.QSqlRelationalTableModel(db=self.log_db)

    def setupWidget(self, wobj):
        wobj.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("./res/icons/logo.png")))

        # setup configuration model
        self.config_model.setTable("configuration")
        self.test_item_model.setTable("test_item")
        self.test_item_model.setRelation(1, QtSql.QSqlRelation(
            "configuration", "id", "partnumber"))

        # setup log model
        self.log_model.setTable("dut")
        self.cycle_model.setTable("cycle")
        self.cycle_model.setRelation(7, QtSql.QSqlRelation("cycle", "id",
                                                           "barcode"))
        # update comboBox
        #self.partNum_comboBox.setModel(self.config_model)
        #self.partNum_comboBox.setModelColumn(
        #    self.config_model.fieldIndex("partnumber"))

        self.config_model.select()      # get data
        for row in range(self.config_model.rowCount()):
            index = self.config_model.index(row, 1)     # 1 for partnumber
            self.partNum_comboBox.addItem(self.config_model.data(
                index).toString())

        self.revision_comboBox.setModel(self.config_model)
        self.revision_comboBox.setModelColumn(self.config_model.fieldIndex(
            "revision"))
        self.test_item_tableView.setModel(self.test_item_model)
        self.testItem_update()

    def auto_enable_disable_widgets(self, ch_is_alive):
        if ch_is_alive:
            self.start_pushButton.setDisabled(True)
            self.sn_lineEdit_1.setDisabled(True)
            self.sn_lineEdit_2.setDisabled(True)
            self.sn_lineEdit_3.setDisabled(True)
            self.sn_lineEdit_4.setDisabled(True)
        else:
            self.start_pushButton.setEnabled(True)
            self.sn_lineEdit_1.setEnabled(True)
            self.sn_lineEdit_2.setEnabled(True)
            self.sn_lineEdit_3.setEnabled(True)
            self.sn_lineEdit_4.setEnabled(True)

    def append_format_data(self, data):
        if data:
            self.info_textBrowser.append(data)
            # self.info_textBrowser.moveCursor(QtGui.QTextCursor.End)
        else:
            pass

    def set_status_text(self, slotnum, status):
        status_list = ["Idle", "Pass", "Fail", "Charging", "Discharging"]
        label = [self.label_1, self.label_2, self.label_3, self.label_4]
        color_list = ["background-color: wheat",
                      "background-color: green",
                      "background-color: red",
                      "background-color: yellow",
                      "background-color: yellow"]
        label[slotnum].setText(status_list[status])
        label[slotnum].setStyleSheet(color_list[status])

    def barcodes(self):
        barcodes = [str(self.sn_lineEdit_1.text()),
                    str(self.sn_lineEdit_2.text()),
                    str(self.sn_lineEdit_3.text()),
                    str(self.sn_lineEdit_4.text())]
        for i in barcodes:
            if not i:
                i = ""
        return barcodes

    def show_image(self):
        barcodes = self.barcodes()
        image_labels = [self.imageLabel1,
                        self.imageLabel2,
                        self.imageLabel3,
                        self.imageLabel4]
        for i in range(len(barcodes)):
            r = BARCODE_PATTERN.search(barcodes[i])
            if barcodes[i] == "":
                image_labels[i].setText("")
            elif r:
                barcode_dict = r.groupdict()
                partnumber = barcode_dict["PN"]
                image_file = "./res/dut_image/" + partnumber + ".jpg"
                if os.path.isfile(image_file):
                    my_pixmap = QtGui.QPixmap(image_file)
                    my_scaled_pixmap = my_pixmap.scaled(
                        image_labels[i].maximumSize(),
                        QtCore.Qt.KeepAspectRatio)
                    image_labels[i].setPixmap(my_scaled_pixmap)
                else:
                    image_labels[i].setText("No dut image found")
            else:
                image_labels[i].setText("Invalid Serial Number")

    def comboBox_update(self):
        # config = sql_handler.TableModel(self.config_table, "configuration")
        current_pn = self.partNum_comboBox.currentText()

        self.config_model.setFilter("PARTNUMBER='" + current_pn + "'")
        self.config_model.select()

        #self.revision_comboBox.setModel(self.config_model)
        #self.revision_comboBox.setModelColumn(self.config_model.fieldIndex(
        #    "revision"))

    def update_table(self):
        filter_combo = "PARTNUMBER = '" + self.partNum_comboBox.currentText() \
                       + "' AND REVISION = '" \
                       + self.revision_comboBox.currentText() + "'"
        self.config_model.setFilter(filter_combo)
        self.config_model.select()
        config_id = self.config_model.record(0).value('ID').toString()
        descrip = self.config_model.record(0).value('DESCRIPTION').toString()
        self.descriptionLabel.setText(descrip)
        self.test_item_model.setFilter("CONFIGID = " + config_id)
        self.test_item_model.select()
        self.test_item_tableView.resizeColumnsToContents()

    def testItem_update(self):
        self.comboBox_update()
        self.update_table()

    def submit_config(self):
        for i in range(self.test_item_model.rowCount()):
            record = self.test_item_model.record(i)
            self.test_item_model.setRecord(i, record)
        re = self.test_item_model.submitAll()
        msg = QtGui.QMessageBox()
        if re:
            msg.setText("Update Success!")
            msg.exec_()
        else:
            error_msg = self.test_item_model.lastError().text()
            msg.critical(msg, "error", error_msg)

    def get_log_data(self, barcodes):
        test_log_model = self.cycle_model
        test_log_model.record().indexOf("id")
        test_log_model.setFilter(
            "barcode IN ('" + "', ".join(barcodes) + "') AND archived = 0")
        test_log_model.select()
        return test_log_model

    def get_dut_data(self, barcodes):
        test_log_model = self.log_model
        test_log_model.record().indexOf("id")
        # test_log_model.setFilter(
        # "barcode IN ('" + "', ".join(barcodes) + "') AND archived = 0")
        test_log_model.setFilter(
            "barcode IN ('" + "', ".join(barcodes) + "')")
        test_log_model.select()
        return test_log_model

    def search(self):
        if self.search_lineEdit.text():
            self.search_result_label.setText("")
            barcodes = []
            barcodes.append(str(self.search_lineEdit.text()))
            test_log_model = self.get_dut_data(barcodes)
            if test_log_model.rowCount() == 0:
                self.search_result_label.setText("No Item Found")
            self.log_tableView.setModel(test_log_model)
            self.log_tableView.resizeColumnsToContents()

    def push_multi_mpls(self):
        mpls = [self.mplwidget,
                self.mplwidget_2,
                self.mplwidget_3,
                self.mplwidget_4]
        barcodes = self.barcodes()
        item = ""
        for i in self.buttonGroup.buttons():
            if i.isChecked():
                item = i.text()

        for i in range(len(mpls)):
            time = []
            data = []
            mpls[i].setFocus()
            mpl_data_model = self.get_log_data([barcodes[i]])
            # mpl_data_model.record().indexOf("id")
            # mpl_data_model.setFilter("barcode = '" + barcodes[i] + "'")
            # mpl_data_model.select()
            for j in range(mpl_data_model.rowCount()):
                record = mpl_data_model.record(j)
                time.append(int(record.value("counter").toString()))
                data.append(float(record.value(item).toString()))
            self.plot(mpls[i], time, data)

    def plot(self, mpl_widget, t, d):
        mpl_widget.axes.plot(t, d)
        mpl_widget.draw()

    def print_time(self, t):
        a = t // 60
        t = t - a * 60
        b = t
        self.lcdNumber.display(str(a) + ":" + str(b) if b > 10 else "0")


if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    w = UFT_UiHandler()
    w.setupUi(Form)
    w.setupWidget(Form)
    w.show_image("../res/icons/despicableMe.jpg")
    Form.show()
    sys.exit(a.exec_())  
