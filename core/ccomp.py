# -*- coding: utf-8 -*-

import cv2
import pandas as pd
import numpy as np

def find_ccomp(im, *args, **kvargs):
    
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(im, *args, **kvargs)
    stats_df = pd.DataFrame(stats, columns=['left', 'top', 'width', 'height', 'area'])
    stats_df['x'] = centroids[:,0]
    stats_df['y'] = centroids[:,1]
    return labels, stats_df
    
def filter_ccomp(stats, min_area=None, max_area=None):
    if min_area == max_area == None:
        return stats
    
    if min_area == None:
        min_area = 0
    elif max_area == None:
        max_area = stats.area.max()
        
    stats_filtered = stats.loc[(stats.area >= min_area) & (stats.area <= max_area)]
    return stats_filtered
    
def one_label(labels, num):
    rows, cols = labels.shape
    res = np.zeros(labels.shape)
    for r in range(rows):
        for c in range(cols):
            if labels[r, c] == num:
                res[r, c] = 255
    return res