# -*- coding: utf-8 -*-

from scipy import stats
from flexvi.core import calibration
from flexvi.calibration.ti import calibexp
import numpy as np

def construct_intrinsics(ti_values):
    camera_matrix = calibration.get_camera_matrix_from_tuple(ti_values[:4])
    dist_coefs = ti_values[4:]
    res = (camera_matrix, tuple(dist_coefs)) 
    return res

def find_ti(data):
    
    m, sd = norm_fit(data)
    dfg, mg, sdg = six_sigma_loop(data, m, sd)
    
    return mg
    
def find_ti_cm(data):
    '''
    Find TI using six sigma loop. 
    Return TI as a camera matrix
    '''
    
    mg = find_ti(data)
    cm, df = calibration.get_intrinsics_from_tuple(mg)    
    
    return cm, df
    
def norm_fit(df):
        
    means = []
    s_deviations = []
    
    for c in calibexp.COLNAMES[1:]:
        d = df[c]    
        
        m, sd = stats.norm.fit(d)
        
        means.append(m)
        s_deviations.append(sd)
    
    return means, s_deviations
    
def six_sigma(df, m, sd):

    rows = df.shape[0]
    cols = len(m)

    res = np.zeros((rows, cols))

    for j in range(cols):
        col = df.ix[:, j+1]
        bottom = m[j] - 3 * sd[j]
        top = m[j] + 3 * sd[j]
        res[:, j] = (col >= bottom) & (col <= top)    

    sum_vec = np.zeros(rows)
    for j in range(cols):
        sum_vec += res[:, j]

    is_good = sum_vec == cols
    good_indices = [i for i in range(rows) if is_good[i]]

    return good_indices
    
def six_sigma_loop(df, m=None, sd=None):
    
    if m == None or sd == None:
        m, sd = norm_fit(df)
    
    last_len = len(df)
    while True:
        good = six_sigma(df, m, sd)
        if len(good) == last_len:
            break
        last_len = len(good)
        df = df.ix[good]
        df.index = range(len(good))
        m, sd = norm_fit(df)

    return df, m, sd

def find_closest(dfg, mg, n=10):
    '''
    For each of of the intrinsic parameters,
    find indices of n data samples closest
    to the mean value
    '''

    res = []
    for j in range(len(calibexp.INTRINSICS)):
        col = dfg.ix[:, j+1]
        mean = mg[j]
        diff = col - mean
        diff_s = sorted(diff)
        
        ten_smallest = diff_s[:n]
        ten_smallest_ind = [diff[diff == num].index[0] for num in ten_smallest]
        
        res.append(ten_smallest_ind)        
        
    return res
