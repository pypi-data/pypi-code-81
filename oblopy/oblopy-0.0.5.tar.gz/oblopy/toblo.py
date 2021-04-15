#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:05:09 2020

@author: cdu022

Toolbox for analysis and visualisation
Functions handy for analysis of (atmospheric) data 
"""

import pandas as pd
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
from netCDF4 import num2date, date2num
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from sklearn.linear_model import LinearRegression
from scipy import signal
from scipy.signal import butter, lfilter, freqz

# =============================================================================
# Statistical Tools
# =============================================================================

def fft(data, dt):
    """
    Estimate the Energy spectrum (depending on frequency or wavenumber) 
    from fourier transform of time ore spacial series 
    """
    data_mask = np.arange(len(data))
    mask = np.isnan(data)
      
    if len(np.where(np.isnan(data))[0]) == len(data):
        N  = len(data)
        T  = dt*N
        df = 1.0/T
        f = np.fft.rfftfreq(N)*N*df
            
        E = pd.DataFrame(f[1:int(N/2)]*np.nan, index = f[1:int(N/2)])
    else:      
        xfiltered = np.interp(data_mask, data_mask[~mask], data[~mask])
            
        N  = len(xfiltered)
        T  = dt*N
            
        df = 1.0/T      # Maximum Frequency
        dw = 2.*np.pi*df
        ny = dw*N/2
            
        a = np.fft.rfft(xfiltered)
        f = np.fft.rfftfreq(N)*N*df
            
        # get the energy content corresponding to each of the frequencies
        E = pd.DataFrame(abs(a[1:int(N/2)]*np.conj(a[1:int(N/2)])), index = f[1:int(N/2)])

    return E


def do_regression(x,y):
    """
    Do a linear regression between two Datasets x & y
    """
    # Remove all points corresponding to nan values
    coords = np.where((~np.isnan(x)) & (~np.isnan(y)))[0]

    x = x[coords].reshape(-1, 1)
    y = y[coords].reshape(-1, 1)
    
    # Utilize the linear regression model
    reg = LinearRegression().fit(x, y)
#    reg_coef  = reg.coef_[0,0]
#    reg_score = reg.score(x, y)
    return x,y,reg
    
def cal_consistency_param(x_array, y_array, condition):
    """
    Do a full consistency/ comparison analysis corresponding to a range of conditions
    """
    reg_coef  = np.zeros(len(condition))
    reg_score = np.zeros(len(condition))
    bias      = np.zeros(len(condition))
    sde       = np.zeros(len(condition))
    corr_coef = np.zeros(len(condition))
    c = 0
    for i in condition:
        x = x_array[i].values
        y = y_array[i].values
        # estimate the bias, sde & correlation
        bias[c]      = np.nanmean(y-x)
        sde[c]       = np.nanstd(y-x)
        corr_coef[c] = np.corrcoef(x,y)[0,1]
    
        x,y,reg = do_regression(x,y)
    
        reg_coef[c]  = reg.coef_[0,0]
        reg_score[c] = reg.score(x, y) # Mearsure for correlation?

        c = c+1    
    return bias, sde, reg_coef, reg_score, corr_coef

# =============================================================================
# Filtering tools
# =============================================================================

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def despike(x, interval = 1800):
    """
    Remove spikes from a dataset
    """

    x_roll = x.rolling(interval,0,center = True).mean().copy()

    x_detrend = (x-x_roll).copy()
    x_destd = x_detrend.rolling(int(interval/15),0,center = True).std().rolling(interval,0,center = True).mean().copy()

    x[x_detrend>4*x_destd] = np.nan
    x[x_detrend<-4*x_destd] = np.nan
    
    return x   
# =============================================================================
# geographical tools    
# =============================================================================

def cal_dist_dir_on_sphere(longitude, latitude):
    """
    function to calculate a series of distances between 
    coordinate points (longitude and latitude) 
    of a platform between sequential timesteps
        
    Parameters
    ----------
    longitude : pd.Series
         time Series of logitudinal coordinates [deg] of the platform
    latitude : pd.Series
        time Series of latitudinal coordinates [deg] of the platform
            
    Returns 
    -------
    distance : pd.Series
        distance the platform travelled between each of the timesteps
    speed : pd.Series
        speed the platform travelled between each of the timesteps
    heading : pd.Series
        direction platform headed between each of the timesteps
               
    """
    
    # Define the Earths Radius (needed to estimate distance on Earth's sphere)
    R = 6378137. # [m]
        
    # Convert latitude and logitude to radians
    lon = longitude * np.pi/180.
    lat = latitude  * np.pi/180.
        
    # Calculate the differential of lon and lat between the timestamps 
    dlon = lon.diff()
    dlat = lat.diff()
        
    # Create a shifted time Series
    lat_t1 = lat.shift(periods=1)
    lat_t2 = lat.copy()
        
    # Calculate interim stage
    alpha = np.sin(dlat/2.)**2 + np.cos(lat_t1) * np.cos(lat_t2) * np.sin(dlon/2.)**2
        
    distance = 2*R*np.arctan2(np.sqrt(alpha),np.sqrt(1-alpha))#(np.arcsin(np.sqrt(alpha))
           
    time_delta = pd.Series((lat.index[1:]-lat.index[0:-1]).seconds, index = lat.index[1::])
    speed = (distance/time_delta)
        
    # Calculate the ships heading
    arg1 = np.sin(dlon) * np.cos(lat_t2)
    arg2 = np.cos(lat_t1) * np.sin(lat_t2) -np.sin(lat_t1) * np.cos(lat_t2) * np.cos(dlon)
        
    heading = np.arctan2(arg1,arg2) * (-180./np.pi) + 90.0
    heading[heading<0.0] = heading + 360.
    heading[heading>360.0] = heading - 360.
    
    return distance, speed, heading
# =============================================================================
# Wind analysis tools    
# =============================================================================

def get_wind_vector(u_h,wd):
    """
    Estimate the horizontal wind speed components u & v from horizontal wind speed and direction
    Transformation from polar coodinates to cartesian coordinates
    
    Parameters
    ----------
    u_h : float
        horizontal wind speed
    wd : float
        horizontal wind direction
    
    Returns
    -------
    u : float
        longitudinal wind component
    v : float
        latitudinal wind component
    """
   
    # transform wd unit (deg) to radians
    wd_rad = wd/180*np.pi
    
    u = - u_h * np.sin(wd_rad)
    v = - u_h * np.cos(wd_rad)
    
    return u,v

def get_wind_from_vector(u,v):
    """
    Estimate the horizontal wind speed and direction from the horizontal wind speed components u & v
    Transformation from cartesian coordinates to coodinates
    
    Parameters
    ----------
    u : float
        array of longitudinal wind component    
    v : float
        array of latitudinal wind component
    Results
    -------
    u_h : float
        array of horizontal wind speed
    wd : float
        array of horizontal wind direction        
    """
    
    # Get the horizontal wind speed
    u_h = np.sqrt(u**2+v**2)
    
    # Get the wind direction
    wd = 180/np.pi * np.arctan(u/v)
    
    # Differentiate between the different wind direction sectors
    wd[(u>=0)&(v>=0)] = wd[(u>=0)&(v>=0)] + 180
    wd[(u<=0)&(v>=0)] = wd[(u<=0)&(v>=0)] + 180     
    wd[(u>=0)&(v<=0)] = wd[(u>=0)&(v<=0)] + 360    
    # Make sure no wind direction value exeeds 360 or falls below 0
    wd[wd>=360] = wd[wd>=360] - 360
    wd[wd<   0] = wd[wd<   0] + 360
    
    return u_h, wd

def rot_wind_vector_in_dir(U,V):
    """
    Function to estimate the along wind or parallel to mean wd (new_U) and 
    cross wind or perpendicular to mean wd (new_V) components 
     
    Parameters
    ----------
    u : float
        pandas Dataframe (with datetime index) of longitudinal wind component (in east west direction)
    v : float
        pandas Dataframe (with datetime index) of latitudinal wind component (in north south direction)

    Results
    -------
    new_U : float
        pandas Dataframe (with datetime index) of along wind component or parallel to mean wd
    new_V : float
        pandas Dataframe (with datetime index) of cross wind component or perpendicular to mean wd
    """
    mean_U = U.rolling(600,0,center=True).mean()#.resample('10min',loffset='5min').mean().copy()
    mean_V = V.rolling(600,0,center=True).mean()#.resample('10min',loffset='5min').mean().copy()
      
    mean_wind, mean_wd = get_wind_from_vector(mean_U,mean_V)
    wd_ups = 270.-mean_wd#.reindex(U.index, method='nearest') 
      
    new_U = U*np.cos(wd_ups/180.*np.pi) +V*np.sin(wd_ups/180.*np.pi)
    new_V = -U*np.sin(wd_ups/180.*np.pi) + V*np.cos(wd_ups/180.*np.pi)
      
    return new_U, new_V

def alt_rot_wind_vector_in_dir(U,V):
    """
    alternative rotate wind in mean wind direction
    """
    mean_U = U.rolling(600,0,center=True).mean()#.resample('10min',loffset='5min').mean().copy()
    mean_V = V.rolling(600,0,center=True).mean()#.resample('10min',loffset='5min').mean().copy()
      
    mean_wind, mean_wd = get_wind_from_vector(mean_U,mean_V)
    wind, wd = get_wind_from_vector(U,V)
    
    # Get wind direction fluctuations
    del_wd = (mean_wd-wd)*np.pi/180.
    
    new_U = wind*np.cos(del_wd)
    new_V = wind*np.sin(del_wd)

# =============================================================================
# Stability (conversion) Tools
# =============================================================================

def calc_p_z(p0,T0,z):
    """
    Calculate the pressure at a certain altitude
    
    Parameters
    ==========
    p0 : float
        Pressure at sea level
    T0 : float
        Temperature at sea level
    z : float
       altitude above sea level
    """
    # Earth-surface gravitational acceleration
    g = 9.81
    # Constant-pressure specific heat
    cp = 1004.68506
    # Molar mass of dry air
    M = 0.02896968
    # Universal gas constant
    R0 = 8.314462618
    
    return p0*(1 - g/(cp*T0)*z)**(cp*M/R0)

def cal_e_sat(T):
    """
    Calculate the water vapour saturation pressure
    
    Parameters
    ==========
    T : float
        Air Temperature at the Height of interest [K]
    """
    
    A = 6.112 
    m = 17.62
    Tn = 243.12
    T = T-273.15 # Convert to deg C
    
    Pws = A * np.exp((m*T)/(Tn+T))
    
    return Pws

def cal_e(T,RH):
    """
    Calculate the water vapour pressure
      
    Parameters
    ==========      
    Pws : water vapour saturation pressure (Is dependent on the temperature)
    """
    Pws = cal_e_sat(T)
    
    return Pws*RH/100.

def cal_mix_ratio(P,T,RH):
    """
    Calculate the mixing ratio
    """    
    Pw = cal_e(T,RH)
    return 0.622 * Pw/(P-Pw)

def cal_Td(P,T,RH):
    """
    calculate dew point
    """
    
    r = cal_mix_ratio(P,T,RH)
    
    A = 6.112 
    m = 17.62
    Tn = 243.12
    
    return Tn*np.log(r*P/((0.622+r)*A))/(m-np.log(r*P/((0.622+r)*A)))+273.15

def cal_virt_T(P,T,RH):
    """
    Calculate the virtual temperature
    """
    e = cal_e(T,RH)    
    q_v = 0.622*e/P    

    T_v = T*(1+0.608*q_v)
    
    return T_v 

def cal_pot_T(P,T,RH):
    """
    Calculate potential and virtual potential temperature
    """
#    r = cal_mix_ratio(P,T,RH)
    
    # Estimate virtual temperature
    T_v = cal_virt_T(P,T,RH)
    
    # Potential Temperature
    theta = T*(1000./P)**0.286
    
    # Virtual potential temperature    
    theta_v = T_v*(1000./P)**0.286 #theta*(1+0.61*r)
    
    return theta, theta_v

def cal_N(theta,alt):
    """
    Calculate the Brunt-Väisälä frequency
    
    """      
    g = 9.81

    del_thetha = theta[:,:-1]-theta[:,1:]
    del_z      = alt[:,:-1] - alt[:,1:]

    mean_theta = (theta[:,:-1]+theta[:,1:])/2
    mean_alt = (alt[:,:-1] + alt[:,1:])/2
    
    N = g/mean_theta * del_thetha/del_z
    
    return N, mean_alt

def cal_M(U,V,alt):
    """
    Calculate the shear frequency
    """
    del_U = U[:,:-1] - U[:,1:]
    del_V = V[:,:-1] - V[:,1:]
    del_z      = alt[:,:-1] - alt[:,1:]
    
    M = (del_U/del_z)**2 + (del_V/del_z)**2

    return M

def cal_Ri_number(P,T,RH, U_diff, V_diff, z):
    """
    Calculate the gradient Richardson number
    """
    # Get the gravity constant
    g   = 9.81 # kg/m^2s
    
    theta, theta_v = cal_pot_T(P,T,RH)
    
    # Estimate Brunt-Vaisaila Frequency (Buoyancy)
    N2 = (g/theta_v * theta_v.diff()/z.diff())
    # Estimate shear frequency
    M2 = (U_diff/z.diff())**2+(V_diff/z.diff())**2
    Ri = N2/M2
    
    return Ri

def cal_moist_lapse_rate(P,T,RH):
    """
    Calculate the moist adiabatic lapse rate
    """
    # Define constants
    g   = 9.8076  # m/s**2
    Hv  = 2501000 # J/kg
    Rsd = 287     # J/kgK
    Rsw = 461.5   # J/kg
#    eps = 0.622   #
    cpd = 1003.5  # J/kgK
    
    # estimate other needed parameters
    r = cal_mix_ratio(P,T,RH)
    
    # estimate moist adiabatic lapse rate (dependent on T)
    return g * (1+ (Hv*r/(Rsd*T)))/(cpd+Hv**2*r/(Rsw*T**2))*1000

# =============================================================================
# Profile analysis --- mainly for temperature, humidity and wind
# =============================================================================

def get_adiabates():
    """
    Estimate the dry and moist adiabate for a certain temperature range (Both Celsius and Kelvin)
    """
    # Define essential parameters
    R=287.04  #Jkg^-1K^-1
    cp=1005   #Jkg^-1K^-1
    p0=1000 #hPa
    L=2.5*10**6 #J kg^-1

    temp_celsius = np.array(range(-80,41))
    temp_kelvin=temp_celsius+273.15
    pressure_hPa=np.array(range(1050,90,-10))

    #make a grid of the data
    tempdata,pressdata=np.meshgrid(temp_kelvin,pressure_hPa*100.)

    #Initialise the arrays
    pot_temp_kelvin=np.zeros(tempdata.shape)
    es=pot_temp_kelvin
    ms=es
    pseudo_pot_temp_kelvin=es

    #Get the potential temperature                         
    pot_temp_kelvin=tempdata*(p0*100/pressdata)**(R/cp)

    #Get the saturation mix ratio
    #first the saturation vapor pressure after Magnus
    #Definition of constants for the Magnus-formula
    c1=17.62
    c2=243.12

    es=6.112*np.exp((17.62*(tempdata-273.15))/(243.12+tempdata-273.15)) #hPa
    #Now I'm calculation the saturation mixing ratio
    ms=622*(es/(pressdata/100-es)) #g/kg

    #At least I need the pseudo-adiabatic potential temperature
    pseudo_pot_temp_kelvin=pot_temp_kelvin*np.exp(L*ms/1000./cp/tempdata)

    #define the levels which should be plotted in the figure
    levels_theta=np.array(range(200,405,5))
    levels_ms=np.array([0.1,0.2,0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0])
    levels_theta_e=np.array(range(220,410,10))

    #The plot
    fig = plt.figure(figsize=(10,10))
    theta=plt.contour(temp_celsius,pressure_hPa,pot_temp_kelvin,levels_theta,colors='blue')
    #plt.clabel(theta,levels_theta[0::2], fontsize=10, fmt='%1.0f')

    #sat_mix_ratio=plt.contour(temp_celsius,pressure_hPa,ms,levels_ms,colors='green')
    #plt.clabel(sat_mix_ratio,fontsize=10,fmt='%1.1f')
    theta_e=plt.contour(temp_celsius,pressure_hPa,pseudo_pot_temp_kelvin,levels_theta_e,colors='red')
    plt.clabel(theta_e,levels_theta_e[1::2],fontsize=10,fmt='%1.0f')

    plt.xlabel('Temperature [$^\circ$C]')
    plt.ylabel('Pressure [hPa]')
    plt.xticks(range(-80,45,5))
    plt.xlim((-80,50))
    plt.yticks(range(1050,50,-50))
    plt.gca().invert_yaxis()
    plt.grid(color='black',linestyle='-')

    # Get the moist adiabates
    moist_adiabates = pd.DataFrame()
    dry_adiabates = pd.DataFrame()
    # Get the moist adiabates
    for i in range(len(theta_e.allsegs)):
        buffer = pd.DataFrame(theta_e.allsegs[i][0][:,0], index = theta_e.allsegs[i][0][:,1], columns =[i])
        moist_adiabates = pd.concat([moist_adiabates, buffer], axis=0)
        buffer = pd.DataFrame(theta.allsegs[i][0][:,0], index = theta.allsegs[i][0][:,1], columns =[i])
        dry_adiabates = pd.concat([dry_adiabates, buffer], axis=0)
    
    moist_adiabates = moist_adiabates.sort_index().interpolate(method='pchip')+273.15
    dry_adiabates = dry_adiabates.sort_index().interpolate(method='pchip')+273.15

    return dry_adiabates, moist_adiabates

# =============================================================================
# Plotting tools
# =============================================================================

def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(9, 13),
                           subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax


# =============================================================================
# Tools to save data in a certain format 
# =============================================================================

def save_to_netcdf(global_atrributes, dimensions, variables, path, filename):
    """
    Save a dataset to netcdf format
          
    Parameters
    ----------
          
    global_atrributes : dict
        dictionary containing all global attributes that will be displayed in the netcdf file
          
    dimensions : dict
        dictionary containing all dimensions that are used in the netcdf file
              
          
    Returns
    -------
    """          
    # Open the netcdf file (in write)          
    dataset = Dataset(path + filename, 'w', format = 'NETCDF4_CLASSIC')
    # Set global attributes
    for attr in global_atrributes.keys():
        dataset.setncattr(attr, global_atrributes[attr])
      
    # Define Set of dimensions used for the variables
    # dataset includes time, height, latitude and longitude information (profile trajectory)
    if 'level' in dimensions.keys():
        level      = dataset.createDimension('level', dimensions['level'])
    time       = dataset.createDimension('time', dimensions['time'])
    latitude   = dataset.createDimension('latitude', dimensions['latitude'])
    longitude  = dataset.createDimension('longitude',dimensions['longitude'])
          
    # Define the Variables to be used
    for var in variables.keys():

        if len(variables[var]['dimension']) == 2:
            dataset.createVariable(var, variables[var]['precision'], 
                               (variables[var]['dimension'][0],
                                variables[var]['dimension'][1]), 
                                fill_value=-9999)            
            # write data to variables
            dataset.variables[var][:,:] = variables[var]['data']
        else:
            dataset.createVariable(var, variables[var]['precision'], 
                                   (variables[var]['dimension'],), fill_value=-9999) 
            # write data to variables
            dataset.variables[var][:] = variables[var]['data']
                      
        # set long names      
        dataset.variables[var].long_name = variables[var]['long_name']
        # set units 
        dataset.variables[var].units = variables[var]['units']
    
    # close the dataset
    dataset.close()


def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)
                    
