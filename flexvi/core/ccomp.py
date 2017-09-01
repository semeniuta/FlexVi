# -*- coding: utf-8 -*-

import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from flexvi import cvoutput

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
    return labels == num

def get_bbox_subimage(im, stats, i):
    left, top = stats.ix[i].left, stats.ix[i].top
    w, h = stats.ix[i].width, stats.ix[i].height
    return im[int(top):int(top+h), int(left):int(left+w)]

def get_subimages(im, ccomp_stats):

    subimages = []
    for i in ccomp_stats.index:
        subimages.append(get_bbox_subimage(im, ccomp_stats, i))
    return subimages

def show_centroids(stats):

    for i in stats.index:

        x, y = stats.ix[i].x, stats.ix[i].y
        left, top = stats.ix[i].left, stats.ix[i].top
        w, h = stats.ix[i].width, stats.ix[i].height

        cvoutput.plot_point((x, y), 'y')
        plt.text(x, y, i, color='y')
