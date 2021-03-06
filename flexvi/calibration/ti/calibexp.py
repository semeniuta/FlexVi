# -*- coding: utf-8 -*-

from flexvi.core import calibration
from flexvi.core import chessboard
from flexvi.dataanalysis import sampling
import pandas as pd
import cPickle as pickle

COLNAMES = ['rms', 'fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']
INTRINSICS = COLNAMES[1:]

def unpickle_calibexp(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

class CameraCalibrationExperiment:
    
    def __init__(self, imset, set_size, nsets):
        self.imageset = imset
        self.set_size = set_size
        self.nsets = nsets
        self.df = None
        self.images = None
        self.corners = None
    
    def set_corners_and_images(self, corners, images):
        self.corners = corners
        self.images = images
        
    def generate_subsets(self):
        if self.images is None and self.corners is None:
            print 'Images and corners not provided. Opening images and finding corners'
            self.corners, self.images = chessboard.open_images_and_find_corners(self.imageset.imagemask, self.imageset.pattern_size, self.imageset.findcbc_flags)                
        nimages = len(self.images)
        
        self.subsets = sampling.generate_list_of_samples(nimages, self.set_size, self.nsets)
    
    def conduct_experiment(self):
                        
        rows = []
        for s in self.subsets:
            print s
            
            im = [self.images[i] for i in s]
            co = [self.corners[i] for i in s]
            res = calibration.calibrate_camera(im, self.imageset.pattern_size, self.imageset.square_size, co)        
            row = calibration.get_intrinsics_as_a_tuple(res)
            rows.append(row)
        
        self.df = pd.DataFrame(rows, columns=COLNAMES)
            
    def pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    





