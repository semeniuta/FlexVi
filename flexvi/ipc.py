# -*- coding: utf-8 -*-

class ImageProcessingChain:
    
    def __init__(self):
        self._chain = []
    
    def add_function(self, f, *args, **kvargs):    
        self._chain.append((f, args, kvargs))
    
    def process(self, im):
        im_current = im
        for f, args, kvargs in self._chain:
            im_current = f(im_current, *args, **kvargs)
        return im_current
        

        