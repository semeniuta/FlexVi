# -*- coding: utf-8 -*-

'''
Remove outliers from the pairs of the (R, V) pairs
needed for further hand-eye calibration
'''

import numpy as np

def read_poses(pairs_datafile):
    '''
    Read data file with (R, V) pairs in Math3D format
    '''    
    pairs = np.load(pairs_datafile)
    return pairs  
    
def compute_moves(pairs):
    ''' 
    Calculate A and B matrices for each of the (R, V) pairs:
    Ai = inv(Ri-1) * Ri
    '''
    res_AB = []
    res_pairs = []
    
    n = len(pairs)
    for i in range(n-1):
        pair_0 = pairs[i]
        for j in range(i+1, n):
            pair_1 = pairs[j]
            R, V = pair_1
            Rprev, Vprev = pair_0
            
            A = Rprev.inverse() * R
            B = Vprev.inverse() * V

            res_AB.append((A, B))
            res_pairs.append((i, j))
    
    return res_AB, res_pairs

def read_poses_and_compute_moves(pairs_datafile):
    ''' 
    Read the (R, V) pairs from the datafiles and calculate
    the corresponding (A, B) pairs using the specified function
    '''
    pairs = read_poses(pairs_datafile)
    AB, AB_pairs = compute_moves(pairs)
    return pairs, AB, AB_pairs   
    
def eval_moves(AB, X, eval_func):
    ''' 
    Calculate norms for the given pairs of A and B matrices
    and the corresponding result of hand-eye calibration.
    
    The argumets are supplied in Math3D format.
    
    Returns a list of matrices [A*X - X*B] (in NumPy format) 
    and the corresponding norms. 
    '''
    
    norms = []
    for A, B in AB:        
        AX = A * X        
        XB = X * B
        norm = eval_func(AX, XB)
        
        norms.append(norm)
            
    return norms
    

    
            
