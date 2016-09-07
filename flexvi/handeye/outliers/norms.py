# -*- coding: utf-8 -*-

from flexvi.handeye import recalc
from flexvi.handeye import pairs
from flexvi.handeye.hecalibrators.parkmartin import ParkMartinCalibrator
from flexvi.handeye.outliers import precision
from flexvi.handeye.outliers.basic import BasicOutliersEliminator
from flexvi.handeye.outliers.evalfuncs import m3d_distance

class NormsOutliersEliminator(BasicOutliersEliminator):
    
    def __init__(self, datafile):
        BasicOutliersEliminator.__init__(self, datafile)
        self.old_norms = pairs.eval_moves(self.AB, self.old_sif, m3d_distance)
        
        '''Calculate object to base transform: R*X*inv(V) '''
        self.old_object_in_base = precision.get_oib_data(self.pose_pairs, self.old_sif)

    
    def remove_outliers(self, top_limit):
            
        ''' 
        Filter out some of the transformations based on specified criterion
        '''
        self.filtered_indices = recalc.filter_pairs(self.old_norms, lambda x: x < top_limit)
        
        
    def recalibrate(self):
        '''
        Perform calibration without filtered transformations and calculate norms 
        of |AX-XB| matrix
        '''
        new_pmc = ParkMartinCalibrator(self.pose_pairs)
        new_pmc.update_move_pairs(self.filtered_indices)
        self.new_sif = new_pmc.sensor_in_flange    
        self.new_norms = pairs.eval_moves(self.AB, self.new_sif, m3d_distance)
        
        '''Calculate object to base transform: R*X*inv(V) '''
        self.new_object_in_base = precision.get_oib_data(self.pose_pairs, self.new_sif)