# -*- coding: utf-8 -*-

from flexvi.transform import m3dinteract as m3di
import numpy as np
import pandas as pd

COLNAMES = ['r11', 'r12', 'r13', 'r21', 'r22', 'r23', 'r31', 'r32', 'r33', 'd1', 'd2', 'd3']

def calc_object_in_base(R, V, X):
    '''
    Compute the "object in base" matrix for the given pose pair (R and V
    matrices) and the "sensor on flange" matrix X
    
    A, B and X are supplied in Math3D format
    '''
    return R*X*V.inverse()

def get_oib_data(pose_pairs, X):
    '''
    For each of the provided pose pairs, the function calculates the
    "object in base" transfotmation matrix and flattens it into a sequence
    [r11, f12, r13, r21, r22 ... r33, d1, d2, d3]. Then, the function
    returns a NumPy array composed of the previously created lists
    '''
    oib_list = [m3di.flatten_transform(calc_object_in_base(R, V, X)) for R, V in pose_pairs]
    return np.array(oib_list)
    
def get_oib_data_pandas(oib_data):
    '''
    Transofm the NumPy array provied by get_oib_data function into a 
    Pandas dataframe with the following colum names:
    'r11', 'r12', 'r13', 'r21', 'r22', 'r23', 'r31', 'r32', 'r33',
    'd1', 'd2', 'd3'
    '''
    return pd.DataFrame(oib_data, columns=COLNAMES)
    
def get_variances(oib, components):
    df = get_oib_data_pandas(oib)
    return [df[c].var() for c in components]
    
def get_means(oib, components):
    df = get_oib_data_pandas(oib)
    return [df[c].mean() for c in components]

def precision_test(noe, top_limits, components=COLNAMES):
    
    vars_1 = []
    vars_2 = []    
    
    to_delete = []
    for i in range(len(top_limits)):
        tlim = top_limits[i]
        noe.remove_outliers(tlim)
        if len(noe.filtered_indices) < 3:
            print 'Too few moves: %d' % len(noe.filtered_indices)
            to_delete.append(i)
            continue
        
        noe.recalibrate()        
        current_vars_1 = get_variances(noe.old_object_in_base, components)               
        current_vars_2 = get_variances(noe.new_object_in_base, components)               
        vars_1.append(current_vars_1)
        vars_2.append(current_vars_2)
    
    top_limits_2 = []
    for i in range(len(top_limits)):
        if i not in to_delete:
            top_limits_2.append(top_limits[i])
            
    vars_df_1 = pd.DataFrame(np.array(vars_1), columns=components, index=top_limits_2)        
    vars_df_2 = pd.DataFrame(np.array(vars_2), columns=components, index=top_limits_2)    
    
    return vars_df_1, vars_df_2, top_limits_2
    
    
    
    