#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 09 15:00:00 2021

@author: cdu022

Toolbox for retrieving and applying motion correction to profiling Lidar observations
"""

import pandas as pd
import numpy as np

# =============================================================================
# Retrieval Tool (Lidar observations)
# =============================================================================    

def DBS_least_squares_retrieval(all_beams, roll, pitch, yaw, az = [0,90,180,270,0], ze = [28,28,28,28,0], rot = False, order = 'zyx'):
    """
    find the 3 dimensional wind vector from radial velocity of a DBS scan, using the least squares method
    
    Ax = b      
    A = N*R 
    
    Least squares method:
    x = (A'A)^(-1)A'b
    
    N:     LOS transformation matrix
    R:     rotation matrix
    b:     radial velocity vector
    x:     estimate for 3D wind vector
    ':     transposed
    ^(-1): inversed
    
    Parameters
    ==========
    all_beams : pandas.DataFrame
        DataFrame containing all available beams of the DBS scan (should be interpolated in time, or filled with nearest)
        [B1, B2, B3, B4, B5]
    theta : float
        cone angle, θ, of DBS scan (rad)
    roll : array
       angle of rotation around x-axis of the system (rad or deg, set unit accordingly)
    pitch : array
        angle of rotation around y-axis of the system (rad or deg, set unit accordingly)
    yaw : array
        angle of rotation around z-axis of the system (rad or deg, set unit accordingly)
    rot : condition
        Indication, if motion compensation should be applied (True or False)
    order : string
        order in which the coordinate system should be rotated 
        xyz: Rotate around z first, than around the transformed y axis, at last around the twice transformed x axis
        zyx: Rotate around x first, than around the transformed y axis, at last around the twice transformed z axis
    """    
    # Define index vector (here corresponding to the time axis)
    time  = np.arange(len(all_beams.index))
    beams = len(all_beams.columns)
    
    # Convert radial velocity time series to 3D array   
    vr = np.array([[all_beams[beam].values] for beam in all_beams.columns])
    
    # Get the LOS transformation vector
    N  = get_N(time, az, ze, beams)    
    
    if rot:
        R = get_R(roll, pitch, yaw, time, order)
        A = multi_dim_matrix_mult(N,R,time)
    else:
        A = N
        
    # Transpose A
    At        = transpose_matrix(A)
    # Multiply Apt and Ap
    AtA       = multi_dim_matrix_mult(At,A,time)
    # find inverse of AptAp
    AtA_inv   = inverse_3x3_matrix(AtA)
      
    # Multiply AptAp_inv and Apt
    AtA_invAt = multi_dim_matrix_mult(AtA_inv,At,time)
    # Do the retrieval  
    retrieval = multi_dim_matrix_mult(AtA_invAt,vr,time)[:,0,:]
    # Convert the retrieved time series to a pandas DataFrame
    retrieval = pd.DataFrame(np.transpose(retrieval), columns = ['u','v','w'], index = all_beams.index)
    
    return retrieval    

# =============================================================================
# Required preparations of the radial velocity vector transformations
# =============================================================================

def get_N(time, az = [0,90,180,270,0], ze = [28,28,28,28,0], beams=5):
    """
    get the LOS transformation vector N
    
    vr = N*u
    
    N[i,:] = [sin(θ_i)*cos(α_i)  sin(θ_i)*sin(α_i)   cos(θ_i)]
    
    θ: zenith angle of the cone  (ze)
    α: azimuth angle of the cone (az)
    i: individual beam
    
    For the default setting (orienting on the WindCube V2) the LOS tansformation matrix will result:
    
    |vr1|   | sin(θ)  0    cos(θ)| 
    |vr2|   |   0   sin(θ) cos(θ)| |u|
    |vr3| = |-sin(θ)  0    cos(θ)|*|v|
    |vr4|   |   0  -sin(θ) cos(θ)| |w|
    |vr5|   |   0     0      1   |
    
    vr1: radial velocity along beam in opposite x-direction (B1)
    vr2: radial velocity along beam in opposite y-direction (B2)
    vr3: radial velocity along beam in x-direction          (B3)
    vr4: radial velocity along beam in y-direction          (B4)
    vr5: radial velocity along beam in z-direction          (B5)
    
    Parameters:
    ===========
    time : array
        1D array containing the time information of the series that is retrieve/analysed
    theta : float
        cone angle, θ, of DBS scan (rad)
    az : list
        azimuth angles corresponding to the beams (deg). Note! len(az) must be equal to beams.
    ze : list
        zenith angles corresponding to the beams (deg). Note! len(ze) must be equal to beams. 
    Returns:
    ========
    N : array
        the LOS transformation matrix [shape: beamsx3xlen(time)]
    """
    
    az = np.deg2rad(np.array(az))
    ze = np.deg2rad(np.array(ze))
    
    N = np.array([[np.cos(az[i])*np.sin(ze[i])*np.ones(len(time)), 
                   np.sin(az[i])*np.sin(ze[i])*np.ones(len(time)), 
                   np.cos(ze[i])*np.ones(len(time))] for i in range(beams)])    

    return N
    
def get_R(roll, pitch, yaw, time, order = 'xyz', unit = 'deg'):
    """
    Get the rotation Matrix
    
    Rx : rotation matrix around the x-axis
    Ry : rotation matrix around the y-axis
    Rz : rotation matrix around the z-axis
    
    Parameters:
    ===========
    roll : array
       angle of rotation around x-axis of the system (rad or deg, set unit accordingly)
    pitch : array
        angle of rotation around y-axis of the system (rad or deg, set unit accordingly)
    yaw : array
        angle of rotation around z-axis of the system (rad or deg, set unit accordingly)
    time : array
        1D array containing the time information of the series that is retrieve/analysed
    order : string
        order in which the coordinate system should be rotated 
        xyz --> Rotate around z first, than around the transformed y axis, at last around the twice transformed x axis
        zyx --> Rotate around x first, than around the transformed y axis, at last around the twice transformed z axis
    """
    if unit == 'deg':
        roll  = np.deg2rad(roll)
        pitch = np.deg2rad(pitch)
        yaw   = np.deg2rad(yaw)
    
    # Define the rotational matrices
    Rx = np.array([[np.ones(len(roll)), np.zeros(len(roll)),np.zeros(len(roll))],
                   [np.zeros(len(roll)), np.cos(roll), -np.sin(roll)],
                   [np.zeros(len(roll)), np.sin(roll),np.cos(roll)]])

    Ry = np.array([[np.cos(pitch), np.zeros(len(pitch)), np.sin(pitch)],
                   [np.zeros(len(pitch)),np.ones(len(pitch)),np.zeros(len(pitch))],
                   [-np.sin(pitch), np.zeros(len(pitch)), np.cos(pitch)]])
    
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), np.zeros(len(yaw))],
                   [np.sin(yaw), np.cos(yaw), np.zeros(len(yaw))],
                   [np.zeros(len(yaw)),np.zeros(len(yaw)),np.ones(len(yaw))]])

    # Usually R should be rotated: 
    Rx = transpose_matrix(Rx)
    Ry = transpose_matrix(Ry)
    Rz = transpose_matrix(Rz)
    
    # Get the rotation matrix including rotation around x, y and z axis
    if order == 'xyz':
        # Rotate around x first, than around the transformed y axis
        RyRx   = multi_dim_matrix_mult(matrix1=Ry,matrix2=Rx,time=time)
        # Additionally rotate around z
        R      = multi_dim_matrix_mult(matrix1=Rz,matrix2=RyRx,time=time) 
    elif order == 'zyx':
        # Rotate around z first, than around the transformed y axis
        RyRz   = multi_dim_matrix_mult(matrix1=Ry,matrix2=Rz,time=time)
        # Additionally rotate around x
        R      = multi_dim_matrix_mult(matrix1=Rx,matrix2=RyRz,time=time)     

    return R

def correct_LOS_vel(all_beams, u_plat, az = [0,90,180,270,0], ze = [28,28,28,28,0]):
    """
    Function to remove translational velocity of a platform from the radial velocity vector 
    
    vr_plat = N*u_plat
    vr_corr = vr-vr_plat
    
    u_plat:  velocity of the platform (kartesian grid) 
    vr_plat: radial velocity of the platform, transposed to LOS  
    N:       the LOS transformation matrix
    
    Parameters
    ==========
    all_beams : pandas.DataFrame
        DataFrame containing all available beams of the DBS scan (should be interpolated in time, or filled with nearest)
        [B1, B2, B3, B4, B5]
    u_plat : array
        velocity (u,v,w) of the platform [size: 3x1xlen(time)]
    theta : float
        cone angle, θ, of DBS scan (rad)
        
    Returns:
    ========
    corr_beams : DataFrame
        radial velocity corrected by platform velocity [shape: len(beams) x len(time)]
    """
    
    time = all_beams.index
    
    # Get the LOS transformation vector
    N  = get_N(time, az, ze, beams = len(all_beams.columns))    
    
    # Estimate the radial velocity vector of the platform
    vr_plat = multi_dim_matrix_mult(N,u_plat,time)[:,0,:]
    
    # convert to DataFrame
    vr_plat = pd.DataFrame(np.transpose(vr_plat), 
                           index = time, 
                           columns = all_beams.columns)
    # Get the radial velocity, corrected by the LOS transformed platform velocity
    corr_beams = all_beams.copy() - vr_plat.copy()
    
    return corr_beams

# =============================================================================
# Required matrix operations for least squares retrieval
# =============================================================================   

def transpose_matrix(matrix):
    """
    method to transpose a time series of matrices
    
    A(t) --> A'(t)
    
    Parameters:
    ===========
    matrix : array
        time series of matrices to be transposed 
        
    transpose : array
        time series of transposed matrices
    """
    transpose = np.zeros((matrix.shape[1],matrix.shape[0],matrix.shape[2]))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            transpose[j,i,:] =  matrix[i,j,:]
    return transpose

def multi_dim_matrix_mult(matrix1,matrix2,time):
    """
    function that is capable of multiplying time series of matrices
    
    Parameters
    ----------
    matrix1 : array
        left hand side 3D matrix
    matrix2 : array
        right hand side 3D matrix
    Returns
    -------
    res : array
        3D matrix product (time series of multiplied matrices)
    
    """
    res = [[[0 for z in range(len(time))] for x in range(len(matrix2[0,:]))] for y in range(len(matrix1[:,0]))]  
         
    # explicit for loops 
    for i in range(len(matrix1[:,0])): 
        for j in range(len(matrix2[0,:])): 
            for k in range(len(matrix2[:,0])): 
         
                # resulted matrix 
                res[i][j][:] += matrix1[i][k][:] * matrix2[k][j][:]
    return np.array(res)

def inverse_3x3_matrix(matrix):
    """
    method to estimate the inverse of a time series of 3x3 matrices
    
    A(t) --> A^(-1)(t)
    
    Parameters:
    ===========
    matrix : array
        time series of matrices to be inverted 
        
    inv_matrix : array
        time series of inverse matrices
    """
    inv_matrix = np.zeros((matrix.shape[0],matrix.shape[1],matrix.shape[2]))
       
    # Find the determinante
    det = matrix[0,0,:]*matrix[1,1,:]*matrix[2,2,:] \
          +matrix[0,1,:]*matrix[1,2,:]*matrix[2,0,:] \
          +matrix[0,2,:]*matrix[1,0,:]*matrix[2,1,:] \
          -matrix[0,2,:]*matrix[1,1,:]*matrix[2,0,:] \
          -matrix[0,0,:]*matrix[1,2,:]*matrix[2,1,:] \
          -matrix[0,1,:]*matrix[1,0,:]*matrix[2,2,:]
    # Get the inverse of the determinante
    inv_det = 1./det
    
    # get the inverse matrix
    inv_matrix[0,0,:] = inv_det*(matrix[1,1,:]*matrix[2,2,:]-matrix[2,1,:]*matrix[1,2,:])
    inv_matrix[0,1,:] = inv_det*(matrix[0,2,:]*matrix[2,1,:]-matrix[0,1,:]*matrix[2,2,:])
    inv_matrix[0,2,:] = inv_det*(matrix[0,1,:]*matrix[1,2,:]-matrix[0,2,:]*matrix[1,1,:])
    inv_matrix[1,0,:] = inv_det*(matrix[1,2,:]*matrix[2,0,:]-matrix[2,2,:]*matrix[1,0,:])
    inv_matrix[1,1,:] = inv_det*(matrix[0,0,:]*matrix[2,2,:]-matrix[0,2,:]*matrix[2,0,:])
    inv_matrix[1,2,:] = inv_det*(matrix[0,2,:]*matrix[1,0,:]-matrix[0,0,:]*matrix[1,2,:])
    inv_matrix[2,0,:] = inv_det*(matrix[1,0,:]*matrix[2,1,:]-matrix[1,1,:]*matrix[2,0,:])
    inv_matrix[2,1,:] = inv_det*(matrix[0,1,:]*matrix[2,0,:]-matrix[0,0,:]*matrix[2,1,:])
    inv_matrix[2,2,:] = inv_det*(matrix[0,0,:]*matrix[1,1,:]-matrix[0,1,:]*matrix[1,0,:])
    return inv_matrix    