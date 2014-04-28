# -*- coding: utf-8 -*-

import numpy as np

def pt_cart_to_homog(pt):
    return np.hstack(pt, 1)
    
def pt_homog_to_cart(pt):
    pt_cartesian = [el/pt[-1] for el in pt[:-1]]
    return np.array(pt_cartesian)

def transform_point(point, homography_matrix, homogenous=False):

    if not homogenous:
        point_in = pt_cart_to_homog(point)
    else:
        point_in = np.array(point)
        
    point_out = np.dot(homography_matrix, point_in)
    
    if not homogenous:
        return pt_homog_to_cart(point_out)
    else:
        return point_out        