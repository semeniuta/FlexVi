# -*- coding: utf-8 -*-

''' 
The fullcalib module contains the functions used for performing the full
process of stereo vision system calibration:

1. From two given image sets (from left and right cameras) N samples of size n
   are generated;
2. Each corresponding pair of samples is used to calibrate the cameras;
3. Calibration results of the sample that gives the smallest calibration error
   are chosen for further stereo vision system calibration
4. Stereo vision system calibration and rectification transorm computation is
   performed given the selected individual cameras' calibration results
5. StereoVisionSystem and two Camera objects are created as the result

@author: Oleksandr Semeniuta
'''

import os
from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import stereovision
from flexvi.opencv import images
from flexvi.calibration.containers.svs import StereoVisionSystem
from flexvi.calibration.containers.camera import Camera
from flexvi.dataanalysis import sampling

def calibrate_svs(cb_set1, cb_set2, sample_size, nsamples, findcbc_flags):
    ''' 
    Performs the full calibration process for stereo vison system. Returns 
    a tuple containing StereoVisionSystem and two Camera objects

    Arguments:
    cb_set1 -- a cvclasses.imageset.CalibrationImageSet object representing 
               a chessboard pattern imageset for the first camera
    cb_set2 -- a cvclasses.imageset.CalibrationImageSet object representing 
               a chessboard pattern imageset for the second camera
    sample_size -- size of the samples taken for calibration
    nsamples -- number of samples taken for calibration
    findcbc_flags -- flags for calling the cv2.findCHessboardCorners function; 
                     can be taken from flexvi.opencv.calibration.flags dictionary
    '''
    
    pattern_size = cb_set1.pattern_size
    square_size = cb_set1.square_size
    c1, c2, i1, i2, f1, f2 = chessboard.open_images_and_find_corners_universal(cb_set1.imagemask, cb_set1.pattern_size, cb_set2.imagemask, findcbc_flags)
    
    population_size = len(i1)
    samples = sampling.generate_list_of_samples(population_size, sample_size, nsamples)
    
    res1 = []
    res2 = []
    for s in samples:
        
        images1_sample = [i1[num] for num in s]
        images2_sample = [i2[num] for num in s]
        corners1_sample = [c1[num] for num in s]
        corners2_sample = [c2[num] for num in s]
        
        res1_sample = calibration.calibrate_camera(images1_sample, pattern_size, square_size, corners1_sample)
        res2_sample = calibration.calibrate_camera(images2_sample, pattern_size, square_size, corners2_sample)
        
        res1.append(res1_sample)
        res2.append(res2_sample)
    
    min_error_index = 0    
    for i in range(1, nsamples):
        if res1[i][0] < res1[min_error_index][0]:
            min_error_index = i
    print res1[min_error_index][0]
            
    intrinsics1 = calibration.get_intrinsics(res1[min_error_index])
    intrinsics2 = calibration.get_intrinsics(res2[min_error_index])
    
    images1 = i1
    images2 = i2
    corners1 = c1
    corners2 = c2
    
    cal_params = stereovision.calibrate_stereo_vision_system(images1, images2, pattern_size, square_size, intrinsics1, intrinsics2, corners1, corners2)
    svs = StereoVisionSystem()
    svs.set_calibration_parameters(cal_params)
    image_size = images.get_image_size(images1[0])
    rt = stereovision.compute_rectification_transforms(intrinsics1, intrinsics2, image_size, svs.R, svs.T)
    svs.set_rectification_transforms(rt)
    
    cam1 = Camera()
    cam2 = Camera()
    
    cam1.set_intrinsics(intrinsics1)
    cam2.set_intrinsics(intrinsics2)
    
    return svs, cam1, cam2    
    
def get_svs_and_cameras_objects(cb_set1, cb_set2, sample_size, nsamples, findcbc_flags, calib_dir):
    '''
    Returns a tuple containing StereoVisionSystem and two Camera objects:
    either by unpicking the files on the filesystem or by performing
    calibration using the calibrate function of the same module.
    
    If the specified calibraion directory (calib_dir) exists on the filesystem,
    the function will try to unpickle the needed data. Otherwise,
    the calibration will be performed
    
    Arguments:
    cb_set1 -- a cvclasses.imageset.CalibrationImageSet object representing 
               a chessboard pattern imageset for the first camera
    cb_set2 -- a cvclasses.imageset.CalibrationImageSet object representing 
               a chessboard pattern imageset for the second camera
    sample_size -- size of the samples taken for calibration
    nsamples -- number of samples taken for calibration
    findcbc_flags -- flags for calling the cv2.findCHessboardCorners function; 
                     can be taken from flexvi.opencv.calibration.flags dictionary
    calib_dir -- directory to save/load pickle files of calibration results
    
    '''    
    
    pickles = {name: os.path.join(calib_dir, name + '.pickle') for name in ('svs', 'cam1', 'cam2')}
    txtfiles = {name: os.path.join(calib_dir, name + '.txt') for name in ('intrinsics1', 'intrinsics2')}
    if not os.path.exists(calib_dir):
        os.makedirs(calib_dir)
        svs, cam1, cam2  = calibrate_svs(cb_set1, cb_set2, sample_size, nsamples, findcbc_flags)
        svs.pickle(pickles['svs'])
        cam1.pickle(pickles['cam1'])
        cam2.pickle(pickles['cam2'])
        cam1.save_to_txt(txtfiles['intrinsics1'])
        cam2.save_to_txt(txtfiles['intrinsics2'])
    else:
        print 'Reading from %s' % calib_dir
        svs = StereoVisionSystem()
        cam1 = Camera()
        cam2 = Camera()
        svs.unpickle(pickles['svs'])
        cam1.unpickle(pickles['cam1'])
        cam2.unpickle(pickles['cam2'])
        
    return svs, cam1, cam2
