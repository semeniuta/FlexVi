# -*- coding: utf-8 -*-

import matplotlib
from PySide import QtGui
import sys

matplotlib.rcParams['backend.qt4']='PySide'

def create_app():
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(sys.argv)
    return app

def create_mpl_canvas(fig):
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    canvas = FigureCanvas(fig)
    return canvas
    
def show_mpl(fig):
    canvas = create_mpl_canvas(fig)
    app = create_app()    
    win = QtGui.QMainWindow()
    win.setCentralWidget(canvas)
    win.show()  
    sys.exit(app.exec_())
