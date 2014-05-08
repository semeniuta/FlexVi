# -*- coding: utf-8 -*-

from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import stereovision as sv
from flexvi.calibration.containers.svs import StereoVisionSystem
from flexvi.opencv.images import get_image_size
from flexvi.dataanalysis import sampling

class StereoVisionSystemCalibrator:
    
    def __init__(self, corners_finder, sample_size=10, nsamples=5):
            
        self.corners_finder = corners_finder

        self._compute_best_intrinsics(sample_size, nsamples)            
                
    def _compute_best_intrinsics(self, sample_size, nsamples):
                    
    
        ''' 1. Generate samples '''
        nimages = len(self.corners_finder.images1)
        samples = sampling.generate_list_of_samples(nimages, sample_size, nsamples)
        
        ''' 
        4. For each of the samples conduct camera calibration only for 
        the first camera
        '''
        
        psize = self.corners_finder.pattern_size
        sqsize = self.corners_finder.square_size
        calib1_results = []
        for s in samples:
            
            im1 = [self.corners_finder.images1[ind] for ind in s]
            c1 = [self.corners_finder.cres1[ind] for ind in s]
            
            res = calibration.calibrate_camera(im1, psize, sqsize, c1)
            calib1_results.append(res)
            
        '''
        5. Find the sample number that leads to the smallest error of
        camera calibration (RMS)
        '''
        min_error_index = 0    
        for i in range(1, nsamples):
            if calib1_results[i][0] < calib1_results[min_error_index][0]:
                min_error_index = i
        print 'Calib1 RMS: %.3f' % calib1_results[min_error_index][0]
              
        ''' 
        6. Select the intirnsics results (camera 1) for the best calibration
        and compute intrinsics for the second camera using the same 
        images sample
        '''
        self.rms = calib1_results[min_error_index][0]
        self.intrinsics1 = calib1_results[min_error_index][1:3]
        
        s = samples[min_error_index]
        im2 = [self.corners_finder.images2[ind] for ind in s]
        c2 = [self.corners_finder.cres2[ind] for ind in s]
        self.intrinsics2 = calibration.calibrate_camera(im2, psize, sqsize, c2)[1:3]
        
        self.images1 = [self.corners_finder.images1[ind] for ind in s]
        self.images2 = im2
            
    def calibrate(self):   
        
        self.svs = StereoVisionSystem()  
        
        psize = self.corners_finder.pattern_size
        sqsize = self.corners_finder.square_size
        im1 = self.corners_finder.images1
        im2 = self.corners_finder.images2
        c1 = self.corners_finder.cres1
        c2 = self.corners_finder.cres2

        res = sv.calibrate_stereo_vision_system(im1, im2, psize, sqsize, self.intrinsics1, self.intrinsics2, c1, c2)

        self.rms = res[0]        
        self.svs.set_calibration_parameters(res)
            
        image_size = get_image_size(self.images1[0])
        rect_res = sv.compute_rectification_transforms(self.intrinsics1, self.intrinsics2, image_size, self.svs.R, self.svs.T)
        self.svs.set_rectification_transforms(rect_res)