# -*- coding: utf-8 -*-

from flexvi.calibration.ti.calibexp import CameraCalibrationExperiment
from flexvi.calibration.ti import tifuncs 

class TrueIntrinsicFinder:
    def __init__(self, imset, sample_size=12, nsamples=10):
        self.ce = CameraCalibrationExperiment(imset, sample_size, nsamples)
        self.ce.conduct_experiment()
        self.ti_values = None
        
    def find_ti(self):        
        self.ti_values = tifuncs.find_ti(self.ce.df)

    @property
    def intrinsics(self):        
        if not self.ti_values:
            self.find_ti()
        
        return tifuncs.construct_intrinsics(self.ti_values)
        