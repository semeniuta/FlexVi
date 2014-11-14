'''
Fixed pose calibrator

Determines a transformation between a fixed object (e.g. a feeder) and
a camera
 
'''

import numpy as np
import cv2
from flexvi.core import chessboard
from flexvi.core import images as improcess
from flexvi.core import calibration

DEFAULT_FINDCBC = chessboard.flags['at_or_fq']

class FixedPoseCalibrator:
    
    '''
    Usage:
    
    cal = FixedPoseCalibrator(img, pattern_size, square_size, intrinsics)
    cal.calibrate()
    
    To access the results:
    cal.rotation
    cal.translation
    cal.homography_matrix
    '''
    
    def __init__(self, img, pattern_size, square_size, intrinsics):
        #self.chessboard_image = improcess.open_image(img)
        self.chessboard_image = img
        self.pattern_size = pattern_size
        self.square_size = square_size
        self._specify_camera_intrinsics(intrinsics)
        
    def calibrate(self, findcbc_flags=None):
        
        if findcbc_flags is None:
            findcbc_flags = DEFAULT_FINDCBC
        
        self._find_corners(findcbc_flags)
        self._solve_pnp()
    
    def _specify_camera_intrinsics(self, intrinsics):
        cm, dc = intrinsics 
        self.camera_matrix = cm
        self.dist_coefs = dc
     
    def _find_corners(self, findcbc_flags):
        cres = chessboard.find_chessboard_corners_on_image(self.chessboard_image, self.pattern_size, findcbc_flags=findcbc_flags)
        success, corners_mat = cres
        if success:
            self.corners_mat = corners_mat
            
    def _set_results(self, rvec, tvec):
        self.rotation = cv2.Rodrigues(rvec)[0]
        self.translation = tvec
        self._create_homography_matrix()
        
    def _create_homography_matrix(self):
        ''' H = sM[r1 r2 t] '''
        modified_transform = np.hstack((self.rotation[:,:-1], self.translation))
        self.homography_matrix = np.dot(self.camera_matrix, modified_transform)
        
        #corners2 = cv2.undistortPoints(self.corners_mat, self.camera_matrix, self.dist_coefs)
        self.homography_matrix2, _ = cv2.findHomography(self.object_points, self.corners_mat)
        '''
        If H is obtained from intrinsic and extrinsic parameters (homography_matrix),
        distortion is probably taken into accound
        If cv2.findHomography is used, it should be assumed that the image is
        undistorted in advance
        '''
    
    def _solve_pnp(self):
        self.object_points = calibration.get_object_points(1, self.pattern_size, self.square_size)[0]        
        image_points = self.corners_mat.reshape(-1, 2)
        
        pnp_res = cv2.solvePnP(self.object_points, image_points, self.camera_matrix, self.dist_coefs)
        rms, rvecs, tvecs = pnp_res
        self._set_results(rvecs, tvecs)
