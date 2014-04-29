# -*- coding: utf-8 -*-

'''
Legacy module. To be rewritten (flexvi.calibration.svscalib)
'''

import cPickle as pickle
from flexvi.confmanager.cmcalib import CalibrationConfigManager
from flexvi.calibration.stereovisionsystem import StereoVisionSystem
from flexvi.opencv import stereovision as sv
from flexvi.opencv import images
from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import imgtransform
import os
import time
import cv2

cm = CalibrationConfigManager()
params = cm.get_svs_parameters() 

def parametrize_stereo_vision_system(imagemasks, pattern_size, square_size, get_intrinsics_method='compute', saverect=False):
    
    f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS    

    print 'Opening images and finding chessboard corners'
    res = chessboard.open_images_and_find_corners_universal(imagemasks[0], pattern_size, imagemasks[1], findcbc_flags=f)
    corners_left, corners_right, images_left, images_right, filenames_left, filenames_right = res
    
    if get_intrinsics_method == 'compute':
        print "Computing cameras' intrinsic parameters"
        lr_intrinsics = compute_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size)    
    elif get_intrinsics_method == 'read':
        print "Reading cameras' intrinsic parameters"
        lr_intrinsics = unpickle_intrinsics()
    intrinsics_left, intrinsics_right = lr_intrinsics
                
    print 'Performing stereo calibration'
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

def create_results_dir():
    timelabel = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))        
    dirname = '%s_%s' % (params['name'], timelabel)
    res_dir = os.path.join(cm.get_directory('stereo'), dirname)
    os.makedirs(res_dir)
    return res_dir


def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def open_images(imagemasks):
    images_left = images.open_images_from_mask(imagemasks[0])
    images_right = images.open_images_from_mask(imagemasks[1])
    return (images_left, images_right)
    
def unpickle_intrinsics():   
    intrinsics_left = unpickle_data(os.path.join(params['datadir_left'], 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(params['datadir_right'], 'intrinsics.pickle'))         
    return (intrinsics_left, intrinsics_right)

def compute_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)
    
def save_rectified_images(new_images, res_dir):
    savedir = os.path.join(res_dir, 'rectified_images')            
    rectimg_left, rectimg_right = new_images
    images.save_images_to_dir(rectimg_left, savedir, '%d_0.jpg')
    images.save_images_to_dir(rectimg_right, savedir, '%d_1.jpg')