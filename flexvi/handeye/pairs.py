# -*- coding: utf-8 -*-

'''
Functions for manipulations of hand-eye pose and move pairs 
'''

import numpy as np

def read_poses(datafile):
    '''
    Read data file with pose pairs (R, V) in Math3D format
    '''    
    pairs = np.load(datafile)
    return pairs  
    
def compute_moves(pairs):
    ''' 
    Calculate move pairs (A, B) for each of the pose pairs:

    Ai = inv(Ri-1) * Ri
    Bi = inv(Vi-1) * Vi
    
    It is assumed that V transfomation is from the camera to the object
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
    Read pose pairs from the datafiles and calculate
    the corresponding move pairs
    '''
    pairs = read_poses(pairs_datafile)
    AB, AB_pairs = compute_moves(pairs)
    return pairs, AB, AB_pairs   
    
def eval_moves(AB, X, eval_func):
    ''' 
    For each move pair evalueate the quality of sensor-in-flange
    transofrmation X using the specified evaluation function     
    
    Arguments:
    AB - move pairs in Math3D format
    X - sensor-in-flange transfotmation in Math3D format
    eval_func - function used to compare transfotmations AX and XB
    
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
    

    
            
