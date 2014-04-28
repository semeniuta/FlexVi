# -*- coding: utf-8 -*-

from glob import glob

class CalibrationImageSet:
    def __init__(self, name, imagemask, pattern_size, square_size):
        self.name = name  
        self.imagemask = imagemask
        self.pattern_size = pattern_size
        self.square_size = square_size
        
    def set_findcbc_flags(self, f):
        self.findcbc_flags = f
            
    def get_tuple(self):
        return (self.imagemask, self.pattern_size, self.square_size, self.name)
    
    @property
    def image_files(self):
        return glob(self.imagemask)

    def __str__(self):
        return 'CalibrationImageSet %s (%s)' % (self.name, self.imagemask)
         