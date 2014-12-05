# -*- coding: utf-8 -*-
'''
Created on Nov 01, 2014
@author: mzfa
'''
import sys
from PyQt4 import QtCore, QtSql
from UFT_GUI import UFT_Ui
from UFT.config import RESULT_DB, CONFIG_DB


class MyDB():
    def __init__(self):
        # select database type
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.query = None
        self.current_db = None

    def open(self):
        if not self.db.open():
            self.db.open()  # connect to or create database
            self.query = QtSql.QSqlQuery()  # sql handler

    def switch_to_configuration(self):
        if not self.current_db == "pgem_config":
            self.db.setDatabaseName(
                "C:/UFT_DB/pgem_config.db")  # set database name
            self.db.open()
            self.current_db = "pgem_config"
        else:
            return

    def switch_to_pgem(self):
        if not self.current_db == "pgem":
            self.db.setDatabaseName("C:/UFT_DB/pgem.db")  # set database name
            self.db.open()
            self.current_db = "pgem"
        else:
            return


class TableModel(QtSql.QSqlTableModel):
    def __init__(self, parent, table_name):
        QtSql.QSqlTableModel.__init__(self, parent)
        self.setTable(table_name)
        self.select()
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)


class RelationModel(QtSql.QSqlRelationalTableModel):
    def __init__(self, parent, table1_name, table1_index_num, rel_table_name,
                 rel_index_name, rel_cols=u""):
        QtSql.QSqlRelationalTableModel.__init__(self, parent)
        self.setTable(table1_name)
        self.setRelation(table1_index_num,
                         QtSql.QSqlRelation(QtCore.QString(rel_table_name),
                                            QtCore.QString(rel_index_name),
                                            QtCore.QString(rel_cols)))
        self.select()
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)


if __name__ == "__main__":
    from PyQt4 import QtGui

    a = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()

    w = UFT_Ui.Ui_Form()
    w.setupUi(Form)

    config_model = TableModel(None, "configuration")

    def pop_comboBox(combobox, model, column):
        combobox.setModel(model)
        combobox.setModelColumn(model.fieldIndex(column))

    pop_comboBox(w.partNum_comboBox, config_model, "PARTNUMBER")
    test_item_view = w.test_item_tableView
    test_item_model = RelationModel(test_item_view, 'test_item', 1,
                                    'configuration', 'ID', u"")

    #
    test_item_view.setModel(test_item_model)

    def comboBox_update():
        config = TableModel(None, "configuration")
        current_pn = w.partNum_comboBox.currentText()
        config.setFilter("PARTNUMBER='" + current_pn + "'")
        pop_comboBox(w.revision_comboBox, config, "REVISION")

    def update_table():
        config1 = TableModel(None, "configuration")
        current_pn = w.partNum_comboBox.currentText()
        current_rev = w.revision_comboBox.currentText()
        filter_combo = "PARTNUMBER = '" + current_pn + "' AND REVISION = '" + \
                       current_rev + "'"
        config1.setFilter(filter_combo)
        config1.select()
        config_id = config1.record(0).value('ID').toString()
        description = config1.record(0).value('DESCRIPTION').toString()
        w.descriptionLabel.setText(description)
        test_item_model.setFilter("CONFIGID = " + config_id)
        test_item_model.select()

    def testItem_update():
        comboBox_update()
        update_table()

    testItem_update()
    w.partNum_comboBox.currentIndexChanged.connect(testItem_update)
    w.revision_comboBox.currentIndexChanged.connect(update_table)

    def submit():
        for i in range(test_item_model.rowCount()):
            record = test_item_model.record(i)
            test_item_model.setRecord(i, record)
        test_item_model.submitAll()

    w.submit_pushButton.clicked.connect(submit)

    Form.show()
    sys.exit(a.exec_())  
