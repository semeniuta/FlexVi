# -*- coding: utf-8 -*-
from flexvi.opencv import calibration
from flexvi.opencv import images
import cv2
import numpy as np

def calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, chessboard_corners_results_left, chessboard_corners_results_right):    
    ''' 
    Conducts calibration of a stereo vision system using the photos 
    of chessboard pattern taken by left and right cameras

    Arguments:
    images_left -- a list of images from left camera
    images_right -- a list of images from left camera
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    intrinsics_left -- a tuple (camera_matrix_left, dist_coefs_left)
                       containing left camera intrinsic parameters: 
                       camera matrix and distortion coeffitient     
    intrinsics_right -- a tuple (camera_matrix_right, dist_coefs_right)
                        containing right camera intrinsic parameters: 
                        camera matrix and distortion coeffitient     
    chessboard_corners_results_left -- a list of tuples got from the
                                       cv2.findChessboardCorners function call
                                       for each image taken by left camera
                                       
    chessboard_corners_results_right -- a list of tuples got from the
                                        cv2.findChessboardCorners function call
                                        for each image taken by right camera
    
    IMPORTANT: all the images passed to the function must already be 
    filtered out, so that there is no images that didn't succeed in being
    passed to cv2.findChessboardCorners function; use 
    cvfunctions.chessboard.filter_chessboard_corners_results_stereo function
    to achieve this
    
    Returns a tuple as a result of the cv2.stereoCalibrate function call,
    containing the following calibration results:
    rms, camera_matrix_left, dist_coefs_left,
    camera_matrix_right, dist_coefs_right, R, T, E, F    
    '''    

    
    '''
    Gathering arguments for cv2.stereoCalibrate function call:
     - object points
     - image points for both cameras
     - camera matrices for both cameras
     - distortion coeffitients for both cameras
     - image size
    '''
    
    lr_images = [images_left, images_right]        

    object_points = calibration.get_object_points(len(lr_images[0]), pattern_size, square_size)    
    
    lr_chessboard_corners_results = [chessboard_corners_results_left, chessboard_corners_results_right]        
    image_points_left = calibration.get_image_points(lr_images[0], lr_chessboard_corners_results[0])
    image_points_right = calibration.get_image_points(lr_images[1], lr_chessboard_corners_results[1])
    
    lr_image_points = [image_points_left, image_points_right]
    
    lr_camera_matrices = [intrinsics_left[0], intrinsics_right[0]]
    lr_dist_coefs = [intrinsics_left[1], intrinsics_right[1]]
    
    image_size = images.get_image_size(images_left[0])
    
    ''' 
    Performing stereo calibration    
    '''
    algorithm = cv2.CALIB_FIX_ASPECT_RATIO + cv2.CALIB_ZERO_TANGENT_DIST + cv2.CALIB_SAME_FOCAL_LENGTH + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_K3+ cv2.CALIB_FIX_K4+ cv2.CALIB_FIX_K5
    term = (cv2.TERM_CRITERIA_MAX_ITER+cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    res = cv2.stereoCalibrate(object_points, lr_image_points[0], lr_image_points[1], image_size, lr_camera_matrices[0], lr_dist_coefs[0], lr_camera_matrices[1], lr_dist_coefs[1], criteria=term, flags=algorithm)
    return res
    
def compute_rectification_transforms(intrinsics_left, intrinsics_right, image_size, rotation_matrix, translation_vector):
    '''
    Computes rectification transforms for stereo vision system

    Arguments:
    intrinsics_left -- a tuple (camera_matrix_left, dist_coefs_left)
                       containing left camera intrinsic parameters: 
                       camera matrix and distortion coeffitient     
    intrinsics_right -- a tuple (camera_matrix_right, dist_coefs_right)
                        containing right camera intrinsic parameters: 
                        camera matrix and distortion coeffitient 
    image_size -- a tuple describing the size of an image in pixels
                  (returned by cvfunctions.images.get_image_size function)
    rotation_matrix -- rotation matrix between left and right camera
                       coordinate systems
    translation_vector -- translation vector between left and right camera
                          coordinate systems
                          
    Returns a tuple as a result of the cv2.stereoRectify function call,
    containing the following results:
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2
    '''    
    camera_matrix_left, dist_coefs_left = intrinsics_left    
    camera_matrix_right, dist_coefs_right = intrinsics_right        
    res = cv2.stereoRectify(camera_matrix_left, dist_coefs_left, camera_matrix_right, dist_coefs_right, image_size, rotation_matrix, translation_vector)
    return res
    
def triangulate_points(p1, p2, points1, points2):
    points1_matrix = np.transpose(np.array(points1))
    points2_matrix = np.transpose(np.array(points2))
    
    res = cv2.triangulatePoints(p1, p2, points1_matrix, points2_matrix)
    res = np.transpose(res)
    res_real = np.array([[row[i]/row[3] for i in range(3)] for row in res])
    
    return res_real
    
    