# -*- coding: utf-8 -*-

from flexvi.handeye import recalc
from flexvi.handeye import olrem
from flexvi.handeye.hecalibrators.park_martin_calibration import ParkMartinCalibrator
from flexvi.handeye.outliers import precision
from flexvi.handeye.outliers.basic import BasicOutliersEliminator
from flexvi.handeye.outliers.evalfuncs import m3d_distance

class NormsOutliersEliminator(BasicOutliersEliminator):
    
    def __init__(self, datafile):
        BasicOutliersEliminator.__init__(self, datafile)
        self.old_norms = olrem.calc_norms(self.AB, self.old_sif, m3d_distance)
        
        '''Calculate object to base transform: R*X*inv(V) '''
        self.old_object_in_base = precision.get_oib_data(self.pose_pairs, self.old_sif)

    
    def remove_outliers(self, top_limit):
            
        ''' 
        Filter out some of the transformations based on specified criterion
        '''
        filtered_indices = recalc.filter_pairs(self.old_norms, lambda x: x < top_limit)
        print filtered_indices
        
        '''
        Perform calibration without filtered transformations and calculate norms 
        of |AX-XB| matrix
        '''
        new_pmc = ParkMartinCalibrator(self.pose_pairs)
        new_pmc.update_move_pairs(filtered_indices)
        self.new_sif = new_pmc.sensor_in_flange    
        self.new_norms = olrem.calc_norms(self.AB, self.new_sif, m3d_distance)
        
        '''Calculate object to base transform: R*X*inv(V) '''
        self.new_object_in_base = precision.get_oib_data(self.pose_pairs, self.new_sif)