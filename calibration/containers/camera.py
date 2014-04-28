# -*- coding: utf-8 -*-

import cPickle as pickle
import numpy as np

class Camera:
    def __init__(self, intrinsics=None):
        if intrinsics == None:
            self.camera_matrix = None
            self.dist_coefs = None
        else:
            self.set_intrinsics(intrinsics)
        self.metadata = {}
        
    @property
    def intrinsics(self):
        return (self.camera_matrix, self.dist_coefs)
        
    def set_intrinsics(self, intrinsics):
        self.camera_matrix, self.dist_coefs = intrinsics
        
    def pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.intrinsics, f) 
    
    def unpickle(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        self.set_intrinsics(data)   
    
    def save_npy(self, cm_filename, dc_filename):
        np.save(cm_filename, self.camera_matrix)
        np.save(dc_filename, self.dist_coefs)
        
    def load_from_npy(self, cm_filename, dc_filename):
        self.camera_matrix = np.load(cm_filename)
        self.dist_coefs = np.load(dc_filename)
        
    def save_to_txt(self, filename):
        with open(filename, 'w') as f:
            f.write('Camera matrix\n')
            f.write(str(self.camera_matrix))
            f.write('\n\n')
            f.write('Distortion coefficients\n')
            f.write(str(self.dist_coefs))
            f.write('\n\n')
            
            if self.metadata:
                for k, v in self.metadata.iteritems():
                    f.write('%s\n' % k)
                    f.write('%s\n' % v)