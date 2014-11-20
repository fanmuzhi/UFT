# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, QtSql
import sys 
from UFT_GUI import UFT_Ui

def createConnection(): 
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE") 
    db.setDatabaseName("../configuration.db") 
    db.open()
    
class TableModel(QtSql.QSqlTableModel):   
    def __init__(self,parent,table_name):   
        QtSql.QSqlTableModel.__init__(self,parent)   
        self.setTable(table_name)
        self.select()
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)

class RelationModel(QtSql.QSqlRelationalTableModel):   
    def __init__(self,parent,table1_name, table1_index_num ,rel_table_name, rel_index_name,):   
        QtSql.QSqlRelationalTableModel.__init__(self,parent)   
        self.setTable(table1_name)
        self.setRelation(table1_index_num, QtSql.QSqlRelation(QtCore.QString(rel_table_name),QtCore.QString(rel_index_name),QtCore.QString(u"*")))
        self.select()
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)


if __name__=="__main__":
    a=QtGui.QApplication(sys.argv)
    createConnection()
    Form = QtGui.QWidget()
    
    w=UFT_Ui.Ui_Form()
    w.setupUi(Form)
    
    config_model = TableModel(None, "configuration")
    def pop_comboBox(combobox, model, column):
        combobox.setModel(model)
        combobox.setModelColumn(model.fieldIndex(column))
    pop_comboBox(w.partNum_comboBox, config_model, "PARTNUMBER")
    pop_comboBox(w.description_comboBox, config_model, "DESCRIPTION")
    pop_comboBox(w.revision_comboBox, config_model, "REVISION")
    
    test_item_view = w.test_item_tableView
    test_item_model = TableModel(test_item_view,"test_item")
    test_item_view.setModel(test_item_model)
    def testItem_update():
        config = TableModel(None, "configuration")
        current_pn = w.partNum_comboBox.currentText()
        current_desc = w.description_comboBox.currentText()
        current_rev = w.revision_comboBox.currentText()
        filter_combo = "PARTNUMBER = '"+current_pn+"' and DESCRIPTION = '"+current_desc+"' AND REVISION = '"+current_rev+"'"
        config.setFilter(filter_combo)
        config.select()
        config_id = config.record(0).value('ID').toString()
    #     test_item_model = RelationModel(test_item_view, "configuration", 0, "test_item", "CONFIGID")
        test_item_model.setFilter("CONFIGID = "+config_id)
        test_item_model.select()
    testItem_update()
    
    w.partNum_comboBox.currentIndexChanged.connect(testItem_update)
    w.description_comboBox.currentIndexChanged.connect(testItem_update)
    w.revision_comboBox.currentIndexChanged.connect(testItem_update)
    
    def submit():
        for i in range(test_item_model.rowCount()):
            record = test_item_model.record(i)
            test_item_model.setRecord(i, record)
        test_item_model.submitAll()
    w.submit_pushButton.clicked.connect(submit)
    
    Form.show()   
    sys.exit(a.exec_())  
