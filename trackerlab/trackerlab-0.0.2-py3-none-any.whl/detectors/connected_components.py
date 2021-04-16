# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:00:38 2021

@author: Martin Fränzl
"""

import numpy as np

import skimage
import pandas as pd

def connected_components(image, threshold, min_area, max_area, max_features, invert=False):
    """
    Detect features using connected-component labeling.
    
    Arguments:
        image (float array): The image data. \n
        threshold (float): The threshold value. \n
        ...
    Returns:
        features (pandas DataFrame): A pandas DataFrame with the detected features. 
    """
    features = pd.DataFrame()
    
    threshold_image = (image > threshold).astype(int) # threshold image
    if invert:
        threshold_image = 1 - threshold_image
    label_image = skimage.measure.label(threshold_image)
    regions = skimage.measure.regionprops(label_image = label_image, intensity_image = image) # http://scikit-image.org/docs/dev/api/skimage.measure.html
    j = 0
    for region in regions:
        # Area filter first 
        if region.area < min_area or region.area > max_area:  # Do not add feature
            continue
        if j >= max_features: # Do not add feature
            continue 
        features = features.append([{'y': region.centroid[0], 
                                     'x': region.centroid[1],
                                     'y_weighted': region.weighted_centroid[0],
                                     'x_weighted': region.weighted_centroid[1],
                                     'orientation': region.orientation,
                                     'minor_axis_length': region.minor_axis_length,
                                     'major_axis_length': region.major_axis_length,
                                     'eccentricity': region.eccentricity,
                                     'area': region.area,
                                     'equivalent_diameter': region.equivalent_diameter,
                                     'filled_area': region.filled_area,
                                     'max_intensity': region.max_intensity,
                                     'mean_intensity': region.mean_intensity,}])
            
    return features, threshold_image
    


