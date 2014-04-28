# -*- coding: utf-8 -*-

import numpy as np

def flatten_transform(t):
    orient = np.array(t.orient.matrix).flatten()
    pos = np.array(t.pos.matrix).flatten()
    return np.hstack((orient, pos))
