# -*- coding: utf-8 -*-

'''
Point class transforms a point expressed in pixels
to the real-world coordinates and vice-versa
'''

import numpy as np
from numpy.linalg import inv

def construct_ois_matrix(rotation, translation):
    rt = (rotation, translation)
    return np.hstack(rt)
    
def pt_homog_to_cart(pt):
    pt_cartesian = [el/pt[-1] for el in pt[:-1]]
    return np.array(pt_cartesian)

class PointTransformer:
    '''
    p = M T P

    p - pixel homogeneous coordinates
    M - camera matrix
    T - object-in-sensor transoformation [R|t]
    P - real-world homogeneous coordinates        
    '''    
        
    def __init__(self, camera_matrix, object_in_sensor):
        
        self.camera_matrix = camera_matrix
        self.object_in_sensor = object_in_sensor

        
    def pixels_to_rw(self, pixel_coordinates):

        p = np.hstack((pixel_coordinates, 1))      
        
        M_inv = inv(self.camera_matrix)
        T_inv = inv(self.object_in_sensor)
        
        M_inv_T_inv = np.dot(M_inv, T_inv)
        P = np.dot(M_inv_T_inv, p)
        
        return pt_homog_to_cart(P)
        
    
    def rw_to_pixels(self, rw_coordinates):
        
        P = np.hstack((rw_coordinates, 1))
        
        MT = np.dot(self.camera_matrix, self.object_in_sensor)
        p = np.dot(MT, P)
        
        return pt_homog_to_cart(p)
         
        
        