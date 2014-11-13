# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle

class PlotFigure:

    def __init__(self, *args, **kvargs):
        self.subplots = {}        
        self.hist_res = {}
        
        self.fig = plt.figure(*args, **kvargs)
        
    def image(self, image, subplot=111, gray=True):    
        ax = self.fig.add_subplot(subplot)
        if gray:
            ax.imshow(image, cm.gray)
        else:
            ax.imshow(image)
        self.subplots[subplot] = ax
        return ax
    
    def histogram(self, data, nbins, subplot=111):
        ax = self.fig.add_subplot(subplot)
        self.hist_res[subplot] = ax.hist(data, nbins)
        self.subplots[subplot] = ax        
        return ax
        
    def plot(self, d1, d2=None, style='b', subplot=111):
        ax = self.fig.add_subplot(subplot)
        if d2 is None:
            ax.plot(d1, style)
        else:
            ax.plot(d1, d2, style)
        self.subplots[subplot] = ax        
        return ax
        
    def point(self, pt, color='r', subplot=111):
        self.plot([pt[0]], [pt[1]], color+'o', subplot)
        
    def circle(self, center, radius, edgecolor='r', fill=False, subplot=111):
        ax = self.fig.add_subplot(subplot)        
        artist = plt.Circle(center, radius, edgecolor=edgecolor, fill=fill)
        self.fig.gca().add_artist(artist)
        return ax
        
    def rectangle(self, lowerleft, width, height, edgecolor='g', fill=False, subplot=111):
        ax = self.fig.add_subplot(subplot)         
        artist = plt.Rectangle(lowerleft, width, height, edgecolor=edgecolor, fill=fill)
        self.fig.gca().add_artist(artist)
        return ax
            
    def show(self):
        plt.show()
        
    def save(self, filename):
        self.fig.savefig(filename)
        
if __name__ == '__main__':
    import random
    data = [random.randint(0, 20) for i in range(100)]
    f = PlotFigure()
    
    f.histogram(data, nbins=10, subplot=121)
    f.plot([1, 2, 10], [20, 40, 3], style='ro-', subplot=122)
    f.point((3, 5), 'r', subplot=121)
    f.circle((5, 15), 2, 'r', subplot=121)
    #f.rectangle((0, 0), 5, 3)
    #f.show()