# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib import cm

class PlotFigure:

    def __init__(self, use_pyplot=True):
        if use_pyplot:        
            self.fig = plt.figure()
        else:        
            self.fig = Figure()
        
    def image(self, image, subplot=111, gray=True):    
        ax = self.fig.add_subplot(subplot)
        if gray:
            ax.imshow(image, cm.gray)
        else:
            ax.imshow(image)
    
    def histogram(self, data, nbins, subplot=111, title=None):
        ax = self.fig.add_subplot(subplot)
        res = ax.hist(data, nbins)
        if not title == None:
            ax.title(title)
        return res
        
    def show(self):
        plt.show()