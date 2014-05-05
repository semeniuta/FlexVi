# -*- coding: utf-8 -*-

import numpy as np

TRANSFORM_PARAMS = ['r11', 'r12', 'r13', 'r21', 'r22', 'r23', 'r31', 'r32', 'r33', 'd1', 'd2', 'd3']

def flatten_transform(t):
    orient = np.array(t.orient.matrix).flatten()
    pos = np.array(t.pos.matrix).flatten()
    return np.hstack((orient, pos))
