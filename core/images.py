# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import os
import mimetypes
from glob import glob
import cv2

def open_image_opencv(image_file, gray=True):
    if gray:
        return cv2.imread(image_file, flags=cv2.IMREAD_GRAYSCALE)
    else:
        return cv2.imread(image_file)
    

def open_image(image_file, gray=True):
    ''' 
    Opens an image file specified as a string
    '''
    im = Image.open(image_file)
    if gray:
        im = im.convert('L')
    return np.array(im)

def open_images_from_dir(directory):
    '''
    Open images from the specified directory and returns a list of pixel arrays
    for each image    
    '''
    image_files = [os.path.join(directory, el) for el in os.listdir(directory)]
    image_files = filter(file_is_image, image_files)
    return [open_image(imgfile) for imgfile in image_files]
    
def open_images_from_mask(mask, indices=None):
    '''
    Open images from the specified mask 
    (e.g. r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg') 
    and returns a list of pixel arrays for each image    
    '''
    image_files = glob(mask)
    if indices:
        selected_image_files = []
        for i in indices:
            selected_image_files.append(image_files[i])
        image_files = selected_image_files
    return [open_image(imgfile) for imgfile in image_files]
    
def file_is_image(filename):
    '''
    Checks if the specified file is an image
    '''
    mt = mimetypes.guess_type(filename)
    return mt[0].split('/')[0] == 'image'
    
def get_image_size(img):
    '''
    Retuns image size in pixels as a tuple with width and height length    
    '''
    h, w = img.shape
    return (w, h)
    
def save_image(img, filename):
    '''
    Saves the image in array representation into specified file    
    '''
    cv2.imwrite(filename, img)
    
def save_images_to_dir(images, directory, mask='%d.jpg'):
    if not os.path.exists(directory):    
        os.makedirs(directory)
    
    for i in range(len(images)):
        save_image(images[i], os.path.join(directory, mask % i))
        
def merge_images(img1, img2):
    return np.concatenate((img1, img2), axis=1)
    