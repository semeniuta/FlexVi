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
    
def norm_fit(df):
        
    means = []
    s_deviations = []
    
    for c in calibexp.COLNAMES[1:]:
        d = df[c]    
        
        m, sd = stats.norm.fit(d)
        
        means.append(m)
        s_deviations.append(sd)
    
    return means, s_deviations
    
    
def find_outliers(df, means, s_deviations):
    colnames = calibexp.COLNAMES[1:]    
    outliers = []
    for row in df.index:
        for col in colnames:
            val = df.loc[row][col]
            i = colnames.index(col)            
            m = means[i]
            sd = s_deviations[i]
            low_lim = m - 3 * sd
            top_lim = m + 3 * sd
            if val < low_lim or val > top_lim:
                print 'Bad row found: %s=%f lies outside [%f, %f]' % (col, val, low_lim, top_lim)
                outliers.append(row)
                break
    return outliers