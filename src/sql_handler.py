# -*- coding: utf-8 -*-
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
from PyQt4.QtSql import * 
import sys 
from PyQt4 import QtCore, QtGui
import UFT_Ui

def createConnection(): 
    db = QSqlDatabase.addDatabase("QSQLITE") 
    db.setDatabaseName("./ufttry.db") 
    db.open() 

def createTable(): 
    q = QSqlQuery() 
    q.exec_("create table if not exists t1 (f1 integer primary key,f2 varchar(20))") 
    q.exec_("delete from t1") 
    q.exec_(u"insert into t1 values(1,'mzfa')") 
    q.exec_(u"insert into t1 values(2,'qibo')") 
    q.exec_("commit") 


class Model(QSqlTableModel):   
    def __init__(self,parent):   
        QSqlTableModel.__init__(self,parent)   
        self.setTable("t1")   
        self.select()   
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)   


class TestWidget(QWidget):   
    def __init__(self):   
        QWidget.__init__(self)   
        vbox=QVBoxLayout(self)   
        self.view=QTableView()   
        self.model=Model(self.view)   
        self.view.setModel(self.model)   
        vbox.addWidget(self.view)   
  
if __name__=="__main__":
    
    a=QApplication(sys.argv)
    createConnection()
    createTable()
    Form = QtGui.QWidget()
    
    w=UFT_Ui.Ui_Form()
    w.setupUi(Form)
    view = w.tableView
    model = Model(view)
    view.setModel(model)
    Form.show()   
    sys.exit(a.exec_())  
