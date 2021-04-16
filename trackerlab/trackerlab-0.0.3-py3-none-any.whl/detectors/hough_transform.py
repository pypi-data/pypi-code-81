# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:00:38 2021

@author: Martin Fränzl
"""

import numpy as np

from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks

import pandas as pd

def hough_transform(image, sigma, low_threshold, high_threshold, min_radius, max_radius, threshold):
    """
    Detect features using circular Hough transfrom.
    
    Arguments:
        image (2D array): Image data. \n
        sigma (float): Sigma value for the Canny edge detector. \n
        low_threshold (int): Minimum radius in pixels.
        high_threshold (int): Maximum radius in pixels.
        min_radius (int): Minimum radius in pixels.
        max_radius (int): Maximum radius in pixels.
        threshold (int): Threshold for selecting the most prominent circles.
    Returns:
        features (pandas DataFrame): Pandas DataFrame with the detected features. 
    """
    features = pd.DataFrame()
    
    edges = canny(image, sigma, low_threshold, high_threshold) # , low_threshold=80, high_threshold=150
    hough_radii = np.arange(min_radius, max_radius, 1) # np.linspace(20, 45, 50) 
    hough_transform = hough_circle(edges, hough_radii)

    # Select the most prominent circles
    _, x_centers, y_centers, radii = hough_circle_peaks(hough_transform, hough_radii, threshold=threshold)  

    features = pd.DataFrame()
    for x, y, r in zip(x_centers, y_centers, radii):
         features = features.append([{'x': x,
                                      'y': y,
                                      #'max_intensity': image[mask==1].max(),
                                      'radius': r,
                                     }])
        
            
    return features, edges.astype('int')
    


