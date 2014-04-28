# -*- coding: utf-8 -*-

import math
from numpy.lib.function_base import average

def get_line_equation(x, y):
    slope = (y[1] - y[0]) / (x[1] - x[0])
    intercept = y[0] - slope * x[0]
    return (slope, intercept)
    
def compute_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    return dist
    
def compute_segment_center(p1, p2):
    return [average((p1[dimension], p2[dimension])) for dimension in range(len(p1))]