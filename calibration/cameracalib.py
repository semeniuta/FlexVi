# -*- coding: utf-8 -*-

'''
CameraCalibrator class used for simple camera calibration 
using a predefined set of images or all images from the set

@author: Oleksandr Semeniuta
'''

from flexvi.core import chessboard
from flexvi.core import calibration
from flexvi.core import images as improcess
from flexvi.calibration.containers.camera import Camera

DEFAULT_FINDCBC = chessboard.flags['at_or_fq']

class CameraCalibrator:
    
    '''
    Usage:
    cal = CameraCalibrator(imset)
    cal.calibrate()
    
    To access the results:    
    cal.calib_res - raw OpenCV calibration result
    cal.camera - parametrized Camera object
    cal.camera_matrix, cal.dist_coefs - accesing the intrinsics separately
    '''
    
    def __init__(self, imset, indices=None, findcbc_flags=None):

        self.images = improcess.open_images_from_mask(imset.imagemask, indices)
        self.pattern_size = imset.pattern_size
        self.square_size = imset.square_size
        
        if findcbc_flags is None:
            self.findcbc_flags = DEFAULT_FINDCBC
        else:
            self.findcbc_flags = findcbc_flags
    
    def calibrate(self): 
        self._find_corners()
        self.calib_res = calibration.calibrate_camera(self.images, self.pattern_size, self.square_size, self.cres)
        intrinsics = self.calib_res[1:3]
        self.camera = Camera(intrinsics)
       
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
