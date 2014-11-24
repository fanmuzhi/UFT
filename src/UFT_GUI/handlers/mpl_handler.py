# -*- coding: utf-8 -*-
'''
Created on Nov 01, 2014
@author: mzfa
'''
import sys
import numpy as np
import random
from PyQt4 import QtCore, QtGui
from UFT_GUI import UFT_Ui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

def plot(axes):
    x = np.linspace(-10, 10)
    # axes.plot(x, x**2)
    axes.plot(x, x**3)

def plot_2(axes):
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2*np.pi*t)
    axes.plot(t, s)

def plot_3(axes):
    axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
    l = [random.randint(0, 10) for i in range(4)]
    axes.plot([0, 1, 2, 3], l, 'r')

#===============================================================================
#   Example
#===============================================================================
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = UFT_Ui.Ui_Form()
    ui.setupUi(Form)

    ui.mplwidget.setFocus()
    plot(ui.mplwidget.axes)

    ui.mplwidget_2.setFocus()
    plot_2(ui.mplwidget_2.axes)

    ui.mplwidget_3.setFocus()

    def update_mpl_3():
        plot_3(ui.mplwidget_3.axes)
        ui.mplwidget_3.draw()
    ui.mplwidget.timer = QtCore.QTimer()
    ui.mplwidget.timer.timeout.connect(update_mpl_3)
    ui.mplwidget.timer.start(1000)
    ui.mplwidget_3.draw()

    ui.mplwidget_4.setFocus()
    



    
    
    
    Form.show()
    sys.exit(app.exec_())
