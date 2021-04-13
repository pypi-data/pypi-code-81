"""
Module for 3D reconstructio of a fringe pattern image (the one you get from an FP-LIF setup)

The main method is fp23d which takes an image and an optional calibration as input and reconstructs 3D from it
"""
# import matplotlib.pyplot as plt
import numpy as np
from skimage import measure

from . import helpers as h
from . import Roi 
from . import demodulation as dd

def phase_to_threeD_const(T, theta, s=1):
    """
    Calculation of the proportionality constant between the threeD
    coordinates and the phase of a fringe pattern, assumes ortographic camera.

    :param T: Fringe pattern carrier period on a flat surface as seen with a camera with zero angle
    :param theta: Angle between camera direction to the fringe pattern projection direction in radians.
    :param s: The focal of the telecentric lens which corresponds to the length pixels/unit in the real world.
    :returns: Proportionality constant
    """
    return T / 2 / np.pi / np.sin(theta) / s

def threeD_to_phase_const(T, theta, s=1):
    """Simply the inverse of phase_to_threeD_const"""
    return 1 / phase_to_threeD_const(T, theta, s)


_min_percentile = 0.005
def fp23d(signal, calibration, negative_theta=False):
    """Function for 3D reconstruction of a fringe pattern, if no calibration has been performed you can call the automated calibration fuction `fp23dpy.Calibration.calibrate` and use that as input calibration"""
    isMasked = np.ma.isMaskedArray(signal)
    signal = signal.astype(float)

    if isMasked:
        roi = Roi.find_from_mask(signal.mask)
        signal = roi.apply(signal)
        mask = signal.mask
        principal_point = roi.apply_to_points([calibration['principal_point']])[0] if 'principal_point' in calibration else np.array(signal.shape[::-1]) / 2
    else:
        mask = np.zeros(signal.shape, dtype=bool)
        principal_point = calibration['principal_point'] if 'principal_point' in calibration else np.array(signal.shape[::-1]) / 2

    shape = signal.shape

    # main estimation of phase here, important!
    phase_with_carrier = dd.demodulate(signal, calibration)
    carrier = h.make_carrier(signal.shape[-2:], calibration['T'], calibration['gamma'], principal_point)
    phase = (1 - 2 * negative_theta) * (phase_with_carrier - carrier)

    labels, n_labels = measure.label((~mask).astype(int), return_num=True)
    absolute_phase_label = -1
    if 'absolute_phase' in calibration:
        x_a, y_a, absolute_phase = calibration['absolute_phase']
        if isMasked:
            x_a, y_a = roi.apply_to_points([[x_a, y_a]])[0]
            if phase.mask[y_a, x_a]:
                raise ValueError('absolute_phase point must not be masked by segmentation')
        absolute_phase_label = labels[y_a, x_a]
        absolute_phase_area = labels == absolute_phase_label
        phase[absolute_phase_area] += absolute_phase - carrier[y_a, x_a] - phase[y_a, x_a]

    # setting all labeled areas without absolute_phase label to have minimum close to phase = 0
    sign = int(np.sign(calibration['theta'])) if 'theta' in calibration else 1
    for j in range(1, n_labels + 1):
        if j == absolute_phase_label:
            continue
        area = labels == j
        points = np.sort(phase[area].flatten())
        phase[area] -= points[int(sign * round(_min_percentile * points.size))]
        # phase[valid] -= np.min(phase[valid])

    
    if 'scale' in calibration:
        scale = calibration['scale']
    else:
        # if no scale, make the output have a maximum size of 5
        scale = np.max(signal.shape) / 5

    xscale = yscale = dscale = 1. / scale
    if 'theta' in calibration:
        xscale *= 1 / np.cos(calibration['theta'])
        dscale *= phase_to_threeD_const(calibration['T'], calibration['theta'])
    if 'phi' in calibration:  ## Phi stuff is not really tested 
        dscale *= 1 / np.cos(np.abs(calibration['phi'] - calibration['gamma']))
    threeD = phase * dscale

    Y, X = np.mgrid[:shape[0], :shape[1]]
    x_0, y_0 = principal_point
    X =  (X - x_0) * xscale
    Y = -(Y - y_0) * yscale
    if 'absolute_phase' in calibration and 'theta' in calibration and 'scale' in calibration:
        X = X + threeD * calibration['T'] / 2 / np.pi / dscale * xscale 

    if 'phi' in calibration:
        phi = calibration['phi']
        X_copy = X.copy()
        X = np.cos(phi) * X_copy + np.sin(phi) * Y
        Y = -np.sin(phi) * X_copy + np.cos(phi) * Y

    # Print extent of bounding box for debug
    # print(np.max(X) - np.min(X), np.max(Y) - np.min(Y), np.max(threeD) - np.min(threeD))

    if isMasked:
        mask = threeD.mask
        grid3d = np.ma.stack((np.ma.array(X, mask=mask), np.ma.array(Y, mask=mask), threeD))
        grid3d = roi.unapply(grid3d)
        # X = roi.unapply(X)
        # Y = roi.unapply(Y)
        # threeD = roi.unapply(threeD)
    else:
        grid3d =  np.stack((X, Y, threeD))
    return grid3d
