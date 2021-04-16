import numpy as np


def rad_to_degree(rad):
    return rad / np.pi * 180


def degree_to_rad(degree):
    return degree / 180 * np.pi


def sind(degree):
    return np.sin(degree_to_rad(degree))


def cosd(degree):
    return np.cos(degree_to_rad(degree))
