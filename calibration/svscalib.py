# -*- coding: utf-8 -*-

import cv2
from flexvi.opencv import chessboard
from flexvi.opencv import calibration

DEFAULT_FINDCBC = chessboard.flags['at_or_fq']

def compute_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)

class StereoVisionSystemCalibrator:
    
    def __init__(self, imagemasks, pattern_size, square_size, findcbc_flags=None):
        if findcbc_flags is None:
            findcbc_flags = DEFAULT_FINDCBC
            
        self.pattern_size = pattern_size
        self.square_size = square_size            
        
        imc = chessboard.open_images_and_find_corners_universal(imagemasks[0], pattern_size, imagemasks[1], findcbc_flags)
        self.cres1, self.cres2, self.images1, self.images2 = imc
    
    def calibrate(self):   
        
        lr_intrinsics = compute_intrinsics(self.images1, self.images2, self.cres1, self.cres2, pattern_size, square_size)    
        intrinsics_left, intrinsics_right = lr_intrinsics
                    
        svs = StereoVisionSystem()    
        res = sv.calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left, corners_right)
        print 'Calibration error: %f' % res[0]
        
        print res[5:]    
        
        svs.set_calibration_parameters(res)
            
        print 'Performing stereo rectification'
        image_size = images.get_image_size(images_left[0])
        rect_res = sv.compute_rectification_transforms(intrinsics_left, intrinsics_right, image_size, svs.R, svs.T)
        svs.set_rectification_transforms(rect_res)    
        
        res_dir = create_results_dir()    
        
        print 'Saving data'    
        svs.pickle(os.path.join(res_dir, 'svs.pickle'))
        
        if saverect:
            print 'Rectifying and saving images'
            new_images = imgtransform.undistort_and_rectify_images_stereo(images_left, images_right, intrinsics_left, intrinsics_right, svs.rotation_matrices, svs.projection_matrices)
            save_rectified_images(new_images, res_dir)
        
        return svs