# -*- coding: utf-8 -*-

from flexvi.calibration.ti import calibexp
from matplotlib import pyplot as plt
import cPickle as pickle
from flexvi.core import chessboard, calibration
import cv2
import numpy as np
from numpy import sqrt, mean, square
import pandas as pd

def unpickle_experiment(pfile):
    df, subsets = pd.read_pickle(pfile)
    return df, subsets

def plot_data_histograms(df):
    for col in calibexp.COLNAMES:
        plt.figure()
        plt.hist(df[col], 100)
        plt.title(col)

def find_min(df, col):
    return df[df[col] == df[col].min()]

def get_imageset_object(name):
    from flexvi.confmanager.cmcalib import CalibrationConfigManager
    cm = CalibrationConfigManager()
    imset = cm.get_chessboard_imageset(name)
    return imset

def min_rms(df):
    return df[df.rms == df.rms.min()]

def get_projected_impoints(cm, dc, objpoints, impoints=None):
    _, rvec, tvec = cv2.solvePnP(objpoints, impoints, cm, dc)
    impoints2, _ = cv2.projectPoints(objpoints, rvec, tvec, cm, dc)
    return impoints2.reshape(-1, 2)

def compare_intrinsics(imset, all_images, all_corners, indices, params_variants):
    '''
    Compare two intrinsic parameters for given image set and indices
    '''

    psize = imset.pattern_size
    sqsize = imset.square_size

    images = [all_images[ind] for ind in indices]
    corners = [all_corners[ind] for ind in indices]

    rms = [[] for p in params_variants]

    objpoints = calibration.get_object_points(1, psize, sqsize)[0]

    for i in range(len(params_variants)):

        cm, dc = params_variants[i]

        for ind in range(len(images)):
            impoints = corners[ind]

            impoints2 = get_projected_impoints(cm, dc, objpoints, impoints)

            diff = impoints - impoints2

            # OLD and wrong
            #rms_val = mean(sqrt(square(diff)))

            squared_distances = np.sum(np.square(diff), axis=1)
            rms_val = sqrt(mean(squared_distances))

            rms[i].append(rms_val)

    return rms

def get_intrinsics_with_min_rms(df):
    intr = tuple(np.array(min_rms(df).ix[:,1:])[0])
    return calibration.get_intrinsics_from_tuple(intr)

def get_intrinsics_by_id(df, id):
    intr = tuple(np.array(df.ix[id]))
    return calibration.get_intrinsics_from_tuple(intr)

def open_imageset(imset, indices=None):

    N = len(imset.image_files)
    print 'N = %d' % N

    if indices is None:
        corners, images = chessboard.open_images_and_find_corners(imset.imagemask, imset.pattern_size, imset.findcbc_flags)
    else:
        corners, images, _ = chessboard.open_images_and_find_corners_universal(imset.imagemask, imset.pattern_size, findcbc_flags=imset.findcbc_flags, indices=indices)

    N_s = len(images)
    print 'N_s = %d' % N_s

    s_rate = N_s / (N + 0.0)
    print 'Success rate = %.2f' % s_rate

    return (corners, images)
