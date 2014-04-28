# -*- coding: utf-8 -*-

import cPickle as pickle

class StereoVisionSystem:
    def __init__(self):
        ''' Calibration parameters '''        
        self.R = None
        self.T = None
        self.E = None
        self.F = None
        ''' Rectification transofrms '''        
        self.R1 = None
        self.R2 = None
        self.P1 = None
        self.P2 = None
        self.Q = None
        
    @property
    def calib_params(self):
        return (self.R, self.T, self.E, self.F)
    
    @property
    def rotation_matrices(self):
        return (self.R1, self.R2)
        
    @property
    def projection_matrices(self):
        return (self.P1, self.P2)
        
    def set_calibration_parameters(self, stereocalibrate_res):
        self.R, self.T, self.E, self.F = stereocalibrate_res[5:]
        
    def set_rectification_transforms(self, stereorectify_res):
        self.R1, self.R2, self.P1, self.P2, self.Q = stereorectify_res[:-2]
        
    def pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
            
    def unpickle(self, filename):
        with open(filename, 'rb') as f:
            unpickled_dict = pickle.load(f)
            self.__dict__ = unpickled_dict