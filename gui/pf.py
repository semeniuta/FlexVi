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
        return ax
    
    def histogram(self, data, nbins, subplot=111, title=None):
        ax = self.fig.add_subplot(subplot)
        res = ax.hist(data, nbins)
        if not title == None:
            ax.title(title)
        return res
        
    def point(self, pt, color='r'):
        plt.plot([pt[0]], [pt[1]], color + 'o')
        
    def circle(self, center, radius, color='r'):
        artist = plt.Circle(center, radius, edgecolor=color, fill=False)
        fig = plt.gcf()
        fig.gca().add_artist(artist)
            
    def show(self):
        plt.show()
        
    def save(self, filename):
        self.fig.savefig(filename)