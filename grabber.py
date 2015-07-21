# -*- coding: utf-8 -*-

'''
This module is depecated and will be replaced
with a workable image grabber package having more consistent API 
'''


from glob import glob
from flexvi.core.images import open_image

class StereoImageGrabber:
    
    def __init__(self, g1, g2):
        self.g1 = g1
        self.g2 = g2
    
    def __iter__(self):
        return self
        
    def next(self):
        im1 = self.g1.next()
        im2 = self.g2.next()
        return im1, im2

class DiskImageGrabber:    
    '''
    g = DiskImageGrabber()
    g.set_mask('images/*.png')
    
    # number of images
    print len(g)   
    
    # grab specific image
    im3 = g.grab_image(3)
    
    # grab images using an iterator
    for im in g:
        print im.shape
    '''
    
    def __init__(self):
        self._next_index = 0
        self._opened_images = dict()
        pass
    
    def __iter__(self):
        return self
    
    def next(self):
        if self._next_index < len(self):   
            im = self.grab_image(self._next_index)
            self._next_index += 1
            return im
        else:
            raise StopIteration()
    
    def __len__(self):
        return len(self._fnames)
    
    def grab_next(self):
        return self.next()
        
    def grab_image(self, i=0):
        fname = self._fnames[i]
        if fname in self._opened_images:
            print 'Already opened'
            return self._opened_images[fname]
        else:
            im = open_image(self._fnames[i])
            self._opened_images[fname] = im
            return im
    
    def set_mask(self, m):
        self._fnames = glob(m)
    
    def set_image_list(self, filenames):
        self._fnames = filenames
            
    
    
