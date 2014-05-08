# -*- coding: utf-8 -*-

from flexvi.opencv import chessboard
from flexvi.opencv import calibration
from flexvi.opencv import stereovision as sv
from flexvi.calibration.containers.svs import StereoVisionSystem
from flexvi.opencv.images import get_image_size
from flexvi.dataanalysis import sampling

def compute_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)

class StereoVisionSystemCalibrator:
    
    def __init__(self, imset1, imset2, sample_size=10, nsamples=5):
            
        self.imset1 = imset1
        self.imset2 = imset2
        
        self.pattern_size = imset1.pattern_size
        self.square_size = imset2.square_size

        self._compute_best_intrinsics(sample_size, nsamples)            
        
        
    def _compute_best_intrinsics(self, sample_size, nsamples):
        
        ''' 1. Generate samples '''
        nimages = len(self.imset1.image_files)
        samples = sampling.generate_list_of_samples(nimages, sample_size, nsamples)
        #print 'Samples: %s' % samples
        
        ''' 
        2. Make a set union among all the samples so that only the needed
        images are opened further
        '''
        all_samples_set = set(samples[0])
        for i in range(1, nsamples):
            all_samples_set.union(samples[i])
        all_indices = list(all_samples_set)
            
        ''' 3. Open images and find chessboard corners '''
        imc = chessboard.open_images_and_find_corners_universal(self.imset1.imagemask, self.pattern_size, self.imset2.imagemask, self.imset1.findcbc_flags, all_indices)
        cres1, cres2, images1, images2 = imc[:-2]        
        
        ''' 
        4. For each of the samples conduct camera calibration only for 
        the first camera
        '''
        calib1_results = []
        indices_list = []
        for s in samples:
            
            indices = [all_indices.index(i) for i in s]
            indices_list.append(indices)            
            
            im1 = [images1[ind] for ind in indices]
            c1 = [cres1[ind] for ind in indices]
            
            res = calibration.calibrate_camera(im1, self.pattern_size, self.square_size, c1)
            calib1_results.append(res)
            
        '''
        5. Find the sample number that leads to the smallest error of
        camera calibration (RMS)
        '''
        min_error_index = 0    
        for i in range(1, nsamples):
            if calib1_results[i][0] < calib1_results[min_error_index][0]:
                min_error_index = i
              
        ''' 
        6. Select the intirnsics results (camera 1) for the best calibration
        and compute intrinsics for the second camera using the same 
        images sample
        '''
        self.rms = calib1_results[min_error_index][0]
        self.intrinsics1 = calib1_results[min_error_index][1:3]
        
        im2 = [images2[ind] for ind in indices_list(min_error_index)]
        c2 = [cres2[ind] for ind in indices_list(min_error_index)]
        self.intrinsics2 = calibration.calibrate_camera(im2, self.pattern_size, self.square_size, c2)[1:3]
            
    def calibrate(self):   
        
        self.svs = StereoVisionSystem()    
        res = sv.calibrate_stereo_vision_system(self.images1, self.images2, self.pattern_size, self.square_size, self.intrinsics1, self.intrinsics2, self.cres1, self.cres2)
        self.rms = res[0]        
        self.svs.set_calibration_parameters(res)
            
        image_size = get_image_size(self.images1[0])
        rect_res = sv.compute_rectification_transforms(self.intrinsics1, self.intrinsics2, image_size, self.svs.R, self.svs.T)
        self.svs.set_rectification_transforms(rect_res)