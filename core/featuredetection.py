# -*- coding: utf-8 -*-

import cv2
from flexvi import cvoutput
from matplotlib import pyplot as plt

at_algorithms = {
    'mean': cv2.ADAPTIVE_THRESH_MEAN_C,
    'gaussian': cv2.ADAPTIVE_THRESH_GAUSSIAN_C 
}

def threshold_binary(image, threshold, maxval=256, invert=False):
    thresold_type = cv2.THRESH_BINARY if not invert else cv2.THRESH_BINARY_INV
    retval, image_t = cv2.threshold(image, threshold, maxval, thresold_type)
    return image_t
    
def threshold_adaptive(image, method_key='gaussian', maxval=256, block_size=3, c_const=0.25):
    method = at_algorithms[method_key]
    threshold_type = cv2.THRESH_BINARY
    image_t = cv2.adaptiveThreshold(image, maxval, method, threshold_type, block_size, c_const)
    return image_t
    
def hough_circles(image, dp=2, min_dist=50):
    res = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, min_dist)
    if res is None:
        return None
    else:
        return [([x, y], radius) for x, y, radius in res[0]]
    
def detect_circles_as_blobs(image):
    '''
    Finds circular blobs on pre-thresholded image using      
    OpenCV's SimpleBlobDetector tool
    '''
    p = cv2.SimpleBlobDetector_Params()
    p.minCircularity = 0.8
    p.maxCircularity = 1.2
    p.filterByCircularity = True
    
    det = cv2.SimpleBlobDetector(p)
    
    blobs = det.detect(image)
    return blobs
    
def display_blobs(image, blobs, display_numbers=False):
    x_list = []
    y_list = []
    size_list = []
    for b in blobs:
        x, y = b.pt
        x_list.append(x)
        y_list.append(y)
        size_list.append(b.size)
    
    circles = [((x_list[i], y_list[i]), size_list[i]) for i in range(len(blobs))]
    
    cvoutput.plot_image(image)    
    cvoutput.plot_circles(circles)
    cvoutput.plot_points(x_list, y_list)
    
    if display_numbers:
        display_blobs_numbers(blobs)
    
def display_blobs_numbers(blobs, display_sizes=False):
    num = 0
    for b in blobs:
        x, y = b.pt

        if display_sizes:
            text = '%d (%.2f)' % (num, b.size)
        else:
            text = num
            
        plt.text(x, y, text, color='w')
        num += 1
