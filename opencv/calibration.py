import cv2
import numpy as np
from flexvi.opencv.images import get_image_size

def calibrate_camera(images, pattern_size, square_size, chessboard_corners_results):
    '''
    Conducts camera calibration using the photos of chessboard pattern

    Arguments:
    images -- a list of images to process
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    chessboard_corners_results -- a list of tuples got from the
                                  cv2.findChessboardCorners function call
                                  for each image
    
    IMPORTANT: all the images passed to the function must already be 
    filtered out, so that there is no images that didn't succeed in being
    passed to cv2.findChessboardCorners function; use 
    cvfunctions.chessboard.filter_chessboard_corners_results function
    to achieve this
    
    Returns a tuple as a result of the cv2.calibrateCamera function call,
    containing the following calibration results:
    rms, camera_matrix, dist_coefs, rvecs, tvecs
    '''
    
    image_size = get_image_size(images[0])
    
    object_points = get_object_points(len(images), pattern_size, square_size)
    image_points = get_image_points(chessboard_corners_results)
     
    res = cv2.calibrateCamera(object_points, image_points, image_size)
    return res
        
def get_image_points(chessboard_corners_results):
    ''' 
    Returns image points for the given calibration task

    Arguments:
    chessboard_corners_results -- a list of tuples got from the
                                  cv2.findChessboardCorners function call
                                  for each image (default None)            
    '''    
    
    image_points = []
    
    for found, corners in chessboard_corners_results:
        image_points.append(corners.reshape(-1, 2))
        
    return image_points
    
def get_object_points(num_images, pattern_size, square_size):
    ''' 
    Returns object points for the given calibration task

    Arguments:
    num_images -- number of images to process
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    '''
    pattern_points = get_pattern_points(pattern_size, square_size)
    object_points = [pattern_points for i in range(num_images)]
    return object_points


def get_pattern_points(pattern_size, square_size):
    '''
    Returns a matrix of the pattern points for using in the
    calibration algorithm
    
    Arguments:
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    '''
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    return pattern_points

def get_intrinsics(res):
    '''
    Returns a tuple containing camera matrix and an array of
    distortion coefficients 
    '''
    return tuple(res[1:3])

def get_intrinsics_as_a_tuple(res):
    ''' 
    Returns a tuple of the following calibration results:
    rms, fx, fy, cx, cy, k1, k2, p1, p2, k3    
    '''
    rms, camera_matrix, dist_coefs, rvecs, tvecs = res       
    
    fx, fy, cx, cy = camera_matrix_to_tuple(camera_matrix)
    k1, k2, p1, p2, k3 = dist_coefs[0]
    
    return (rms, fx, fy, cx, cy, k1, k2, p1, p2, k3) 

def camera_matrix_to_tuple(camera_matrix):
    '''
    Returns a tuple of camera intrinsic parameters 
    (based on the camera matrix privided) in the following order:
    fx, fy, cx, cy
    '''
    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    
    return (fx, fy, cx, cy)
    
def get_camera_matrix_from_tuple(params):
    '''
    Returns camera matrix based on given intrinsic parameters
    of the camera: fx, fy, cx, cy (supplied as a tuple or other sequence)
    '''
    
    fx, fy, cx, cy = params
    cm = np.zeros((3, 3))
    cm[0, 0] = fx
    cm[1, 1] = fy
    cm[0, 2] = cx
    cm[1, 2] = cy
    cm[2, 2] = 1
    
    return cm
    
