# -*- coding: utf-8 -*-

def m3d_distance(AX, XB):
    '''
    Calculate distance between the two transforms AX and XB
    '''
    return XB.pos.dist(AX.pos)
    
def m3d_angle(AX, XB):
    '''
    Calculate angle between the two transforms AX and XB
    '''
    return XB.orient.ang_dist(AX.orient)