# -*- coding: utf-8 -*-

import matplotlib
from PySide import QtGui
import sys

matplotlib.rcParams['backend.qt4']='PySide'

def create_app():
    '''
    Create QtGui.QApplication object
    '''    
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(sys.argv)
    return app

def create_mpl_canvas(fig):
    '''
    Create Matplotlib figure canvas to be embedded in Qt appliations
    
    Parameters:
    fig - a matplotlib.figure.Figure object
    '''
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
    canvas = FigureCanvasQTAgg(fig)
    return canvas
    
def show_mpl(fig):
    '''
    Create a simple Qt application displaying a Matplotlib figure
    '''
    canvas = create_mpl_canvas(fig)
    app = create_app()    
    win = QtGui.QMainWindow()
    win.setCentralWidget(canvas)
    win.show()  
    sys.exit(app.exec_())
