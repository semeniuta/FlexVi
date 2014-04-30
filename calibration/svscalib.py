# -*- coding: utf-8 -*-

from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import stereovision as sv
from flexvi.calibration.containers.svs import StereoVisionSystem
from flexvi.opencv.images import get_image_size

DEFAULT_FINDCBC = chessboard.flags['at_or_fq']

def compute_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)

class StereoVisionSystemCalibrator:
    
    def __init__(self, imagemasks, pattern_size, square_size, indices=None, findcbc_flags=None):
        if findcbc_flags is None:
            findcbc_flags = DEFAULT_FINDCBC
            
        self.pattern_size = pattern_size
        self.square_size = square_size            
        
        imc = chessboard.open_images_and_find_corners_universal(imagemasks[0], pattern_size, imagemasks[1], findcbc_flags, indices)
        self.cres1, self.cres2, self.images1, self.images2 = imc[:-2]
    
    def calibrate(self):   
        
        lr_intrinsics = compute_intrinsics(self.images1, self.images2, self.cres1, self.cres2, self.pattern_size, self.square_size)    
        self.intrinsics1, self.intrinsics2 = lr_intrinsics
                    
        self.svs = StereoVisionSystem()    
        res = sv.calibrate_stereo_vision_system(self.images1, self.images2, self.pattern_size, self.square_size, self.intrinsics1, self.intrinsics2, self.cres1, self.cres2)
        self.svs.set_calibration_parameters(res)
            
        image_size = get_image_size(self.images1[0])
        rect_res = sv.compute_rectification_transforms(self.intrinsics1, self.intrinsics2, image_size, self.svs.R, self.svs.T)
        self.svs.set_rectification_transforms(rect_res)