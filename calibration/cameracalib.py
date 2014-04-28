# -*- coding: utf-8 -*-

'''
This module contain functions for simple camera calibration tasks
such as calibration a camera using a predefined set of images

@author: Oleksandr Semeniuta
'''

from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import images as improcess

DEFAULT_FINDCBC = chessboard.flags['at_or_fq']

class CameraCalibrator:
    
    def __init__(self, imset, findcbc_flags=None, indices=None):

        self.images = improcess.open_images_from_mask(imset.imagemask, indices)
        self.pattern_size = imset.pattern_size
        self.square_size = imset.square_size
        
        if findcbc_flags is None:
            self.findcbc_flags = DEFAULT_FINDCBC
        else:
            self.findcbc_flags = findcbc_flags
            
        self._find_corners()
    
    def calibrate(self):        
        self.calib_res = calibration.calibrate_camera(self.images, self.pattern_size, self.square_size, self.cres)
       
    @property
    def camera_matrix(self):
        return self.calib_res[1]
        
    @property
    def dist_coefs(self):
        return self.calib_res[2]

    def _find_corners(self):
        cres = chessboard.find_chessboard_corners(self.images, self.pattern_size, findcbc_flags=self.findcbc_flags)
        cres_f, images_f = chessboard.filter_chessboard_corners_results(cres, self.images)
        
        self.rejected_cb_images = len(cres) - len(cres_f)
        
        self.cres = cres_f
        self.images = images_f