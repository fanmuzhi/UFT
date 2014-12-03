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

import logging
import log_handler
import mpl_handler
import sql_handler
# try:
#     import UFT
#     from UFT.channel import Channel, ChannelStates
# except Exception as e:
#     print e.message


class UFT_UiHandler(UFT_UiForm):
    def __init__(self, parent=None):
        UFT_UiForm.__init__(self)
        # handler = log_handler.QtHandler()
        # handler.setFormatter(UFT.formatter)
        # UFT.logger.addHandler(handler)
        # UFT.logger.setLevel(logging.INFO)
        self.dut_image = None
        self.config_table = QtGui.QTableView()
        self.my_db = sql_handler.MyDB()
        self.config_model = None
        self.test_item_model = None
        self.data_table = QtGui.QTableView()


    def setupWidget(self, wobj):
        wobj.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("./res/icons/logo.png")))
        ''' initial configuration tab combobox and table  '''
        self.my_db.switch_to_configuration()
        self.config_model = sql_handler.TableModel(self.config_table,
                                                   "configuration")
        self.test_item_model = sql_handler.RelationModel(
            self.test_item_tableView,
            "test_item",
            1,
            "configuration",
            "CONFIGID")
        self.__popComboBox(self.partNum_comboBox, self.config_model,
                           "PARTNUMBER")
        self.test_item_tableView.setModel(self.test_item_model)
        self.testItem_update()
        ''''''
        # self.push_multi_mpls()

    def auto_enable_disable_widgets(self, ch_is_alive):
        if ch_is_alive:
            self.start_pushButton.setDisabled(True)
            self.sn_lineEdit_1.setDisabled(True)
            self.sn_lineEdit_2.setDisabled(True)
            self.sn_lineEdit_3.setDisabled(True)
            self.sn_lineEdit_4.setDisabled(True)
        else:
            self.start_pushButton.setDisabled(False)
            self.sn_lineEdit_1.setDisabled(False)
            self.sn_lineEdit_2.setDisabled(False)
            self.sn_lineEdit_3.setDisabled(False)
            self.sn_lineEdit_4.setDisabled(False)

    def append_format_data(self, data):
        if data:
            self.info_textBrowser.insertPlainText(data)
            self.info_textBrowser.moveCursor(QtGui.QTextCursor.End)

    def set_status_text(self, dut_list):
        if dut_list:
            self.label_1.setText(str(dut_list[0].status))
            self.label_2.setText(str(dut_list[1].status))
            self.label_3.setText(str(dut_list[2].status))
            self.label_4.setText(str(dut_list[4].status))

    def barcodes(self):
        barcodes = [str(self.sn_lineEdit_1.text()),
                    str(self.sn_lineEdit_2.text()),
                    str(self.sn_lineEdit_3.text()),
                    str(self.sn_lineEdit_4.text())]
        for i in barcodes:
            if not i:
                i = ""
        return barcodes

    # def start_click(self):
    #     try:
    #         ch = Channel(barcode_list = self.barcodes(), channel_id=0,
    #                      name="UFT_CHANNEL")
    #         ch.setDaemon(True)
    #         ch.start()
    #         ch.queue.put(ChannelStates.INIT)
    #         ch.queue.put(ChannelStates.CHARGE)
    #         ch.queue.put(ChannelStates.PROGRAM_VPD)
    #         ch.queue.put(ChannelStates.CHECK_ENCRYPTED_IC)
    #         ch.queue.put(ChannelStates.LOAD_DISCHARGE)
    #         ch.queue.put(ChannelStates.EXIT)
    #         #ch.isAlive.connect(self.auto_enable_disable_widgets)
    #     except Exception as e:
    #         msg = QtGui.QMessageBox()
    #         msg.setText(e.message)
    #         msg.show()
    #         msg.exec_()

    # def auto_enable_disable_widgets(self, ch_is_alive):
    #     if ch_is_alive:
    #         self.start_pushButton.setDisabled(True)
    #     else:
    #         self.start_pushButton.setDisabled(False)

    def show_image(self, image):
        my_pixmap = QtGui.QPixmap(image)
        my_scaled_pixmap = my_pixmap.scaled(self.imageLabel.size(),
                                            QtCore.Qt.KeepAspectRatio)
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
        test_log_model = sql_handler.RelationModel(self.data_table,
                                                   "cycle",
                                                   5,
                                                   "dut",
                                                   "id",
                                                   u"barcode")
        test_log_model.setFilter("barcode IN ('" + "', ".join(barcodes) + "')")
        test_log_model.select()
        self.data_table.setModel(test_log_model)
        return test_log_model

    def search(self):
        if self.search_lineEdit.text():
            self.search_result_label.setText("")
            barcodes = []
            barcodes.append(str(self.search_lineEdit.text()))
            test_log_model = self.get_log_data(barcodes)
            if test_log_model.rowCount() == 0:
                self.search_result_label.setText("No Item Found")
            self.log_tableView.setModel(test_log_model)

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
        mpl_data_model = self.get_log_data(barcodes)
        mpl_data_model.record().indexOf("id")
        for i in range(len(mpls)):
            time = []
            data = []
            mpls[i].setFocus()
            mpl_data_model.setFilter("barcode = '" + barcodes[i] + "'")
            mpl_data_model.select()
            for j in range(mpl_data_model.rowCount()):
                record = mpl_data_model.record(j)
                time.append(int(record.value("time").toString()))
                data.append(float(record.value(item).toString()))
            self.plot(mpls[i], time, data)

    def plot(self, mpl_widget, t, d):
        mpl_widget.axes.plot(t, d)
        mpl_widget.draw()


if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    w = UFT_UiHandler()
    w.setupUi(Form)
    w.setupWidget(Form)
    w.show_image("../res/icons/despicableMe.jpg")
    Form.show()
    sys.exit(a.exec_())  
