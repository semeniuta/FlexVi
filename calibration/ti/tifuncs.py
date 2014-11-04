# -*- coding: utf-8 -*-

from scipy import stats
from flexvi.core import calibration
from flexvi.calibration.ti import calibexp

def construct_intrinsics(ti_values):
    camera_matrix = calibration.get_camera_matrix_from_tuple(ti_values[:4])
    dist_coefs = ti_values[4:]
    res = (camera_matrix, tuple(dist_coefs)) 
    return res

def find_ti(data):
    
    ti_values = []
    for c in calibexp.COLNAMES[1:]:
        d = data[c]    
        m, sd = stats.norm.fit(d)
        ti_values.append(m)
    
    return ti_values