# -*- coding: utf-8 -*-

from flexvi.handeye import pairs
from flexvi.handeye.hecalibrators.parkmartin import ParkMartinCalibrator

class BasicOutliersEliminator:
    def __init__(self, datafile):
        
        ''' 
        Open data file with pose pairs (R, V) and calculate all 
        move pairs (A, B)
        '''    
        self.pose_pairs, self.AB, combinations = pairs.read_poses_and_compute_moves(datafile)
        
        '''
        Perform calibration with ALL move pairs
        '''
        old_pmc = ParkMartinCalibrator(self.pose_pairs)    
        self.old_sif = old_pmc.sensor_in_flange
        
                