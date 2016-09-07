# -*- coding: utf-8 -*-

from flexvi.core import chessboard

class ChessboardCornersFinder:

    def __init__(self, imset1, imset2=None):
        self.imset1 = imset1
        self.imset2 = imset2    
        self.pattern_size = imset1.pattern_size
        self.square_size = imset1.square_size
        
        if imset2 is None:
            self.stereo_vision = False
        else:
            self.stereo_vision = True
                
    def find(self):
        
        if self.stereo_vision:
            res = chessboard.open_images_and_find_corners_universal(self.imset1.imagemask, self.pattern_size, self.imset2.imagemask, self.imset1.findcbc_flags)
            self.cres1, self.cres2, self.images1, self.images2, self.fnames1, self.fnames2 = res
        else:
            res = chessboard.open_images_and_find_corners_universal(self.imset1.imagemask, self.pattern_size, findcbc_flags=self.imset1.findcbc_flags)
            self.cres, self.images, self.fnames = res
        
