# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:00:38 2021

@author: Martin Fränzl
"""

import numpy as np

from skimage.feature import blob_dog
import pandas as pd

def difference_of_gaussians(image_in, min_sigma=1, max_sigma=30, sigma_ratio=1.6, threshold=0.1, overlap=0.5):
    """
    Detect features using difference of Gaussians.
    
    Arguments:
        image_in (2D array): The input, grayscale image, the features are assumed to be light on dark background (white on black). \n
        min_sigma (float): The minimum standard deviation for Gaussian kernel. Reduce to detect smaller features. \n
        max_sigma (float): The maximum standard deviation for Gaussian kernel. Increase to detect larger features. \n
        sigma_ratio (float): The ratio between the standard deviation of Gaussian kernels used for computing the difference of Gaussians. \n
        threshold (float): The absolute lower bound for scale space maxima. Local maxima smaller than threshold are ignored. Reduce to detect blobs with less intensities. \n
        overlap (float): A value between 0 and 1. If the area of two features overlaps by a fraction greater than threshold, the smaller feature is eliminated. \n
    Returns:
        features (pandas DataFrame): A pandas DataFrame with the detected features.\n
        image_out (2D array): The output image. 
    """
    
    features = pd.DataFrame()
    
    image = image_in/image_in.max()
    mlist = blob_dog(image, min_sigma, max_sigma, sigma_ratio, threshold, overlap)
    radii = mlist[:, 2]*np.sqrt(2)

    x, y = np.meshgrid(np.arange(0, image.shape[1], 1), np.arange(0, image.shape[0], 1))
    if mlist.size > 0:
        for j in range(mlist.shape[0]):
            mask = (((x - mlist[j, 1])**2 + (y - mlist[j, 0])**2) < (mlist[j, 2]*np.sqrt(2))**2).astype(int)
            features = features.append([{'y': mlist[j, 0],
                                         'x': mlist[j, 1],
                                         'max_intensity': image[mask==1].max(),
                                         'mean_intenity': image[mask==1].mean(),
                                         'area': 2*np.pi*mlist[j, 2]**2,
                                         }])
                                         
    return features, image
    
