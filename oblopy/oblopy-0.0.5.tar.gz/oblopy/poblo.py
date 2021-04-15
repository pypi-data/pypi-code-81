#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:54:11 2020

@author: cdu022

The processing skript for the OBLO infrastructure
"""

from roblo import *
from toblo import *
import pandas as pd
import numpy as np
import glob


# =============================================================================
# Processing Methods (Instruments)
# =============================================================================

def process_radial_vel_zephir(directory, filename):
    """
    Get the Wind speed and direction from Radial velocities
    """
    
    radial_vel = read_zephir_spectra(directory, filename)
    
    # Seperate the series for each scan (same reference)
    first_scan = np.array(radial_vel['Reference'])[0]
    last_scan  = np.array(radial_vel['Reference'])[-1]
    
    h_buf = []
    U_buf = []
    w_buf = []
    wd_buf = []
    h_buf = []    
    for i in np.arange(first_scan,last_scan+1):
        if len(radial_vel[radial_vel['Reference']==i]) > 0:
            # Radial velocities corresponding to one scan
            vr_vec = radial_vel['Radial velocities (m/s)'][radial_vel['Reference']==i]
            # azimuth/ phase corresponding to one scan
            phase_vec = radial_vel['Phase (rad)'][radial_vel['Reference']==i]
            # get the height of scan
            height = np.median(radial_vel['Height (m)'][radial_vel['Reference']==i])
        
            # Get the "wind direction" from maximal correlation
            offset = np.arange(0,np.pi+0.1,0.1) # Define the offset
            corr = np.zeros(len(offset))
            for j in np.arange(len(offset)):
                corr[j] = np.corrcoef(np.array(0.5*abs(np.cos(phase_vec-offset[j]))),
                                      np.array(vr_vec))[0,1]

            wd_apx = offset[np.where(corr==np.max(corr))[0][0]]

            # Do a least square fit for the absolute wind vector components: ¦Uh¦ and ¦w¦ 
            # Define the radial velocity matrix
            b = np.transpose(np.matrix(vr_vec))
            ### use the 2D approach ###
            At = np.matrix([np.array(0.5*abs(np.cos(phase_vec-wd_apx))),
                            np.cos(1./6.*np.pi)*np.ones(len(phase_vec))])
            # If u,v and w component is to be retrieved
            #At = np.matrix([np.array(0.5*abs(np.cos(phase_vec))),np.array(0.5*abs(np.sin(phase_vec))),np.cos(1./6.*np.pi)*np.ones(len(phase_vec))])

            # Transpose A
            A = np.transpose(At)
            # Multiply At and A
            [U,w] = np.linalg.inv(At*A)*At*b
            U = U[0,0]
            w = w[0,0]

            h_buf  = np.append(h_buf, height)
            U_buf  = np.append(U_buf, U)
            w_buf  = np.append(w_buf, w)
            wd_buf = np.append(wd_buf, np.round(180/np.pi*wd_apx))

            retrieval = pd.DataFrame({'height':h_buf,
                                      'U':U_buf,
                                      'w':w_buf,
                                      'WD':wd_buf})

#            plt.figure()
#            plt.title('h = '+str(int(height))+' U = '+str(np.round(U,1))+' w = '+str(np.round(w,2))+r' $\theta$ = '+str(np.round(180/np.pi*wd_apx)))
#            plt.plot(vr_vec)
#            plt.plot(abs(0.5*U*np.cos(phase_vec-wd_apx)+w*np.cos(1./6.*np.pi)))
      
    # Sort retrieval by height
    levels = [10, 20, 30, 50, 60, 80, 100, 125, 150, 200] 
    U_sorted = {}
    w_sorted = {}
    wd_sorted = {}
    
    for level in levels:
        U_sorted[level] = np.array(retrieval['U'][retrieval['height']==level])
        w_sorted[level] = np.array(retrieval['w'][retrieval['height']==level])
        wd_sorted[level] = np.array(retrieval['WD'][retrieval['height']==level])
    # estimate u and v
    u_sorted, v_sorted = get_wind_vector(u_h=U_sorted,wd=wd_sorted)
    
    #plt.figure(figsize=[5,5])
    #plt.scatter(u_sorted.mean(),v_sorted.mean())    
    #plt.xlim([-20,20])
    #plt.ylim([-20,20])
    
    return u_sorted, v_sorted, w_sorted, U_sorted, wd_sorted


def process_ship_based_zephir(path_zephir, path_ship, delimiter,rot = 0, levels = [10, 20, 30, 38, 50, 60, 80, 100, 125, 150, 200]):
    """
    correct for ship movement and yawing of ship
    
    path_zephir = '/scratch/Data/GEOF232_2020/Zephir/Wind_Data/'
    delimiter = ';'
    path_ship = '/scratch/Data/GEOF232_2020/Ship_log/raw/'
    """
    
    # =============================================================================
    # Read the processed data
    # =============================================================================

    uh, wd, w, met = read_zephir(path = path_zephir, 
                                           delimiter=delimiter, 
                                           rot = rot)

    uh.columns = levels
    wd.columns = levels

    # Convert data to u and v components
    u, v = get_wind_vector(u_h = uh , wd = wd)

    # =============================================================================
    # Read ship log data (Kristine Bonnevie)
    # =============================================================================
    files = glob.glob(path_ship+'*.csv')
    log = pd.DataFrame()
    for file in files:
        print(file)
        log_buf = read_kristine_bonnevie(file)
        log = pd.concat([log,log_buf], axis=0)
    log = log.sort_index()
    
    # Get the positions
    lat = log['Latitude'][~log.index.duplicated()].reindex(u.index, method='nearest')
    lon = log['Longitude'][~log.index.duplicated()].reindex(u.index, method='nearest')
    
    position = pd.concat([lon,lat], axis=1)
    
    # Get SST and AirT
    airT = log['Air temp'][~log.index.duplicated()].reindex(u.index, method='nearest')
    ssT  = log['Water temp'][~log.index.duplicated()].reindex(u.index, method='nearest') 
    
    # Get Air Pressure 
    p = log['Air pressure'][~log.index.duplicated()].reindex(u.index, method='nearest')
    
    # Get humidity
    rh = log['Humidity'][~log.index.duplicated()].reindex(u.index, method='nearest')
    
    # Define yaw/heading
    yaw = (log['Heading'][~log.index.duplicated()].reindex(u.index, method='nearest'))/180*np.pi
    
    # Get the ship speed 
    ship_speed = (log['Speed']*1.8)/3.6 # convert from knots to m/s
    ship_speed = ship_speed[~log.index.duplicated()].reindex(uh.index, method = 'nearest')

    # Get u and v component of ship speed
    u_s =   ship_speed * np.cos(yaw) 
    v_s = - ship_speed * np.sin(yaw)
    

    # and of wind speed collected by ship
    us, vs = get_wind_vector(u_h =  log['Wind'], wd = log['Wind dir'])
    
    # Convert to same time resolution as Lidar observations
    us_new = us[~us.index.duplicated()].reindex(u.index, method = 'nearest').copy()
    vs_new = vs[~vs.index.duplicated()].reindex(u.index, method = 'nearest').copy()
    
    # Get the corresponding wind speed and direction (for this resolution)
    ush_new, wds_new = get_wind_from_vector(u = us_new, v = vs_new)

    # =============================================================================
    # Correct the wind data
    # =============================================================================

    # rotate the wind components 
    u_rot = {}
    v_rot = {}
    for level in levels:
        u_rot[level] =  u[level]*np.cos(yaw)+v[level]*np.sin(yaw)
        v_rot[level] = -u[level]*np.sin(yaw)+v[level]*np.cos(yaw)
    u_rot = pd.DataFrame(u_rot)
    v_rot = pd.DataFrame(v_rot)    

    # Get the wind speed and direction from the rotated coordinates
    uh_new, wd_new = get_wind_from_vector(u = u_rot, v = v_rot)

    # Correct for rotated wd estimates of Lidar
    for level in levels:
        wd_buf = wd_new[level].copy()
        wd_buf = pd.DataFrame(wd_buf, columns = [level])
        wd_buf[abs(wd_buf[level] - wds_new)>135] = wd_buf[abs(wd_buf[level] - wds_new)>135] -180
        wd_buf[wd_buf<0] = wd_buf[wd_buf<0] +360
        wd_buf[wd_buf>360] = wd_buf[wd_buf>360]-360
        
        wd_new[level] = wd_buf.copy()
        
    # Get the u and v components from updated wind direction
    u_new, v_new = get_wind_vector(u_h =  uh, wd = wd_new)
    
    # Get the final wind components (corrected for ship movement)
    u_f = {}
    v_f = {} 
    for level in levels:
        u_f[level] = u_new[level] + u_s
        v_f[level] = v_new[level] + v_s
    u_f = pd.DataFrame(u_f)
    v_f = pd.DataFrame(v_f)
    
    uh_f, wd_f = get_wind_from_vector(u = u_f, v = v_f)
    
    return u_f, v_f, uh_f, wd_f, ush_new, wds_new, ship_speed, yaw, position, airT, ssT, p, rh

def seperate_processed_Windcube_components(lidar_data):
    """
    """
    # Define the components
    u_cols = ['x_wind_speed_'+str(i) for i in range(12)]
    v_cols = ['y_wind_speed_'+str(i) for i in range(12)]
    w_cols = ['z_wind_speed_'+str(i) for i in range(12)]
    
    
    ws_cols = ['wind_speed_'+str(i) for i in range(12)]
    wd_cols = ['wind_direction_'+str(i) for i in range(12)]
    
    u  = lidar_data[u_cols]
    v  = lidar_data[v_cols]    
    w  = lidar_data[w_cols]    
    ws = lidar_data[ws_cols]        
    wd = lidar_data[wd_cols]    
    
    return u, v, w, ws, wd

def fit_curve(x,y,var):
    """
    Fit curve using a linear squares approach
    
    func can be: log (N*log(x)), 0 (D*x^0), 1 (C*x^1), 2 (B*x^2), 3 (A*x^3)
    """
    
    # Define the necessary matrices
    if var == 'wind':
        A_T = np.matrix([[np.log(i) for i in x],[i**2 for i in x],[i for i in x],[1 for i in x]])
    elif var == 'temp':
        A_T = np.matrix([[i**5 for i in x],[i**4 for i in x],[i**3 for i in x],[i**2 for i in x],[i for i in x],[1 for i in x]])  
    
    A = np.transpose(A_T)
    
    y = np.transpose(np.matrix([y]))
    
    # Estimate the regression-parameters using least-squares approach
    alpha = np.linalg.inv(A_T*A)*A_T*y
    
    return alpha
    
    
def estm_new_curve(new_x, alpha, var): 
    """
    Estimate new profile unsing estimated regression parameters
    """
    # Calculated fit and estimate corresponding derivative  
    if var == 'wind':
        A_T_new = np.matrix([[np.log(i) for i in new_x],[i**2 for i in new_x],[i for i in new_x],[1 for i in new_x]])#,[1 for i in new_z]])
#        dydx = np.array(alpha[0])[0,0]*1/new_x + np.array(alpha[1])[0,0]*3*new_x**2 + np.array(alpha[2])[0,0]*2*new_x +np.array(alpha[3])[0,0]
        dydx = np.array(alpha[0])[0,0]*1/new_x + np.array(alpha[1])[0,0]*2*new_x + np.array(alpha[2])[0,0] #+ 2* np.log(new_x)/new_x*np.array(alpha[4])[0,0]#+ 3*new_x**2*np.array(alpha[4])[0,0]
    elif var == 'temp':
        A_T_new = np.matrix([[i**5 for i in new_x],[i**4 for i in new_x],[i**3 for i in new_x],[i**2 for i in new_x],[i for i in new_x],[1 for i in new_x]]) 
        dydx = np.array(alpha[0])[0,0]*5*new_x**4 +np.array(alpha[1])[0,0]*4*new_x**3 +np.array(alpha[2])[0,0]*3*new_x**2 + np.array(alpha[3])[0,0]*2*new_x + np.array(alpha[4])[0,0]
    A_new = np.transpose(A_T_new)
    y_new = A_new*alpha
      
          
    return np.array(y_new)[:,0], dydx

# =============================================================================
# Processing Tools
# =============================================================================


