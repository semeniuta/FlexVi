# -*- coding: utf-8 -*-

import numpy as np

def invert(image):
    return 255 - image
    
def clamp(image, a, b):
    interval_len = b - a    
    return (interval_len/255.0) * image + a
    
def adjust_contrast_and_brightness(image, contrast_gain, brightness_bias):
    new_im = np.zeros(image.shape, dtype=np.uint8)  
    
    h, w = image.shape
    for i in range(h):
        for j in range(w):
            new_value = contrast_gain * image[i, j] + brightness_bias
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            new_im[i, j] = new_value
                
    return new_im