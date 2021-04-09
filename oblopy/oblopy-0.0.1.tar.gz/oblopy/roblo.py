#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:47:45 2020

@author: cdu022

The "Read" Oblo instrumentation files - function collection 
"""
from toblo import *
import pandas as pd
import numpy as np
import glob, os
import copy
import numpy.ma as ma 
from scipy.io import loadmat
import datetime as dt
from datetime import datetime, timedelta 
import netCDF4 as nc
from netCDF4 import Dataset
from netCDF4 import num2date, date2num 

# =============================================================================
###############################################################################
############################## IN SITU MESUREMENTS ############################
###############################################################################
# =============================================================================
# =============================================================================
# Read Alliance Ship meteorology data
# =============================================================================
def read_alliance(data_loc):
    """
    data_loc = '/scratch/Data/IGP/Alliance_Meteo_QC2/IGP_ship_met_QC2.nc'

    """
    dataset = Dataset(data_loc, 'r')

    time = pd.to_datetime(num2date(dataset['time'][:].data,'minutes since 2018-02-05 00:00:00'))
    sst  =     dataset['sea_surface_temperature_interpolated'][:].data
    airT =     dataset['air_temperature_interpolated'][:].data
    rh  =      dataset['relative_humidity'][:].data
    p  =       dataset['air_pressure'][:].data
    wind =     dataset['wind_speed'][:].data
    wind_dir = dataset['wind_direction'][:].data
    longitude = dataset['longitude_nmea'][:].data
    latitude = dataset['latitude_nmea'][:].data
    heading = dataset['heading_nmea'][:].data
    speed   = dataset['water_speed_nmea'][:].data
    ship_data = pd.DataFrame({'sst':sst,'airT':airT, 'rh':rh, 'p':p, 'wind':wind, 
                              'wind_dir':wind_dir, 'lon':longitude,
                              'lat':latitude, 'speed':speed,'heading':heading}, index = time)
    dataset.close()
    return ship_data

# =============================================================================
# Read the ship log from Kristine Bonnevie
# =============================================================================

def read_kristine_bonnevie(file):
    """
    file = '/scratch/Data/GEOF232_2020/Ship_log/raw/pos02-03-2020.csv'
    """
    
    log = pd.read_csv(file, skiprows=2, encoding = "ISO-8859-1", engine='python')
    
    # Get the date
    day = file.split('/')[-1][3:5]
    month = file.split('/')[-1][6:8]
    year = file.split('/')[-1][9:13]
    
    log.Time = pd.to_datetime(year+'-'+month+'-'+day+' '+log.Time)
    log.Time.iloc[-1] = log.Time.iloc[-1]+timedelta(days=1)
    
    log.index = log.Time
    
    # Get the longitude and latitude information
    lon = np.zeros(len(log))
    lat = np.zeros(len(log))
    for i in range(len(log)):
        try:
            lon[i] = float(log['Longitude'].iloc[i][:3]) + float((log['Longitude'].str.split(' ').iloc[i][0])[3:])/60.
            lat[i] = float(log['Latitude'].iloc[i][:2]) +  float((log['Latitude'].str.split(' ').iloc[i][0])[2:])/60.
        except TypeError:
            lon[i] = np.nan
            lat[i] = np.nan
            
    log['Longitude'] = lon
    log['Latitude']  = lat
    
    log[log==-999] = np.nan
    
    return log
    
# =============================================================================
# Read the Radiosonde Data (IGP, netcdf)
# =============================================================================

def read_radiosonde(data_loc):
    """
    
    """
    origin_dir = os.getcwd()        
    # Change to directory that includes the files to be read                                      
    os.chdir(data_loc)   

    # Scan list fo all dates of selected period (Must be slightly altered from original syntax)
    filenames = sorted(glob.glob('*.nc'))  
    #nc_data = Dataset(data_loc+'ncas-radiosonde-2_alliance_20180212-113916_sonde_v0.nc','r')

    sonde = {}
    for file in filenames:
        nc_data = Dataset(file)
        single  = {}
        single['temperature']       = nc_data['air_temperature'][:].data
        single['relative_humidity'] = nc_data['relative_humidity'][:].data
        single['pressure']          = nc_data['air_pressure'][:].data
        single['altitude']          = nc_data['altitude'][:].data
        single['time']              = pd.to_datetime(nc.num2date(nc_data['time'][:].data,
                                                               'seconds since 1970-01-01'))
        single['wind_speed']        = nc_data['wind_speed'][:].data
        single['wind_direction']    = nc_data['wind_from_direction'][:].data 
        sonde[file.split('_')[2]]   = pd.DataFrame(single, index = single['altitude'])
        nc_data.close()

    os.chdir(origin_dir) 

    temp = {}
    ws   = {}
    wd   = {}
    rh   = {}
    p    = {}
    dz  = 10
    
    ascents = []
    new_index = np.arange(10,4000,dz)
    for ascent in sonde.keys():
#        if ascent == '20180303-114432' or ascent == '20180305-175442' or ascent == '20180316-204817' or ascent =='20180216-114326':
#            print('skip')
#        else:
##            print(ascent)
        reindex = sonde[ascent].copy()
        reindex.index = sonde[ascent].index.astype(int)
        reindex = reindex[~reindex.index.duplicated()]
        reindex = reindex.sort_index()
        reindex = reindex.interpolate().reindex(index=new_index,method='bfill').interpolate()#np.array(windcube.level)+10
      
        # Combine the reindexed time series of 
        time_stamp = reindex.time[reindex.index[0]].strftime('%Y-%m-%d %H:%M:%S')
      
        temp[time_stamp] = np.array(reindex.temperature)
        ws[time_stamp]   = np.array(reindex.wind_speed)
        wd[time_stamp]   = np.array(reindex.wind_direction)
        rh[time_stamp]   = np.array(reindex.relative_humidity)
        p[time_stamp]    = np.array(reindex.pressure)
        del reindex
        ascents.append(ascent)
        
    temp = pd.DataFrame(temp, index = new_index)
    wd   = pd.DataFrame(wd, index = new_index)                    
    ws   = pd.DataFrame(ws, index = new_index)
    rh   = pd.DataFrame(rh, index = new_index)
    p    = pd.DataFrame(p, index = new_index)

    radio_ws = ws.transpose()
    radio_ws.index = pd.to_datetime(radio_ws.index)
    radio_wd = wd.transpose()
    radio_wd.index = pd.to_datetime(radio_wd.index)

    radio_temp = temp.transpose()
    radio_temp.index = pd.to_datetime(radio_temp.index)
    radio_rh = rh.transpose()
    radio_rh.index = pd.to_datetime(radio_rh.index)
    radio_p  = p.transpose()
    radio_p.index = pd.to_datetime(radio_p.index)    
    
    return radio_temp, radio_rh, radio_p, radio_ws, radio_wd

# =============================================================================
# Netcdf Datasets
# =============================================================================

def read_netcdf(file):
    """
    Read netcdf datasets (with maximum of 2 dimension variables)
    """
    # Define the file
    data = Dataset(file)

    # Get the time vector
    try:
        time = num2date(data['time'][:].data, units=data['time'].units,
                            calendar='gregorian')
    # In case the netcdf stars in year 0000 (not possible in netcdf4 module)
    except ValueError:
        # to unidata about this
        tunits = data['time'].units
        since_yr_idx = tunits.index('since ') + 6
        year = int(tunits[since_yr_idx:since_yr_idx+4])
        year_diff = year - 1

        new_units = tunits[:since_yr_idx] + '0001-01-01 00:00:00'
        time = num2date(data['time'][:].data, new_units, calendar='gregorian')
        time = [datetime(d.year + year_diff, d.month, d.day, 
                  d.hour, d.minute, d.second) for d in time]    

    # Get the variable names and dimensions
    var_name = []
    var_dim = []
        
    buffer = {}    
    for var in data.variables:
        var_name = np.append(var_name, var)
        var_dim = np.append(var_dim, len(data[var].shape))
        # Save the variable
        if var == 'level':
            buffer[var] = data[var][:].data
        elif len(data[var].shape) == 1:
            buffer[var] = pd.DataFrame(data[var][:].data, index = time, columns = [var])
        elif len(data[var].shape) == 2:
            buffer[var] = pd.DataFrame(data[var][:,:].data, index = time, columns = data['level'][:].data)
        
    data.close()
    return buffer

# =============================================================================
###############################################################################
################################ ALL LIDAR ####################################
###############################################################################
# =============================================================================


# =============================================================================
# Zephir 300 continuous wave Lidar
# =============================================================================

def read_zephir(path, delimiter, zephir_levels = [10, 20, 30, 38, 50, 60, 80, 100, 125, 150, 200], rot = 0, month = '_'):
    """
    Read the 3 dimentional wind speed components from the Zephir Lidar dataset (internally processed). 
    path = '/scratch/Data/Zephir/Wind_328@Y2020_M02_D20.ZPH.csv'
    delimiter = ','

    Parameters
    ==========
    
    path: str
        path to directory, where zephire files are stored
        
    delimiter: str (';',',')
        delimiter used in file (should be ',', however under certain conditions can also be ';'). Check in file.

    zephir_levels: list, default= [10, 20, 30, 38, 50, 60, 80, 100, 125, 150, 200]
        Levels choosen for the zephir Lidar to focus
    
    Returns
    =======
    
    uh: pandas dataframe
        dataframe containing horizontal wind speed at different heights
        
    wd: pandas dataframe
        dataframe containing wind direction at different heights
        
    w: pandas dataframe
        dataframe containing vertical wind speed at different heights 
        
    met: pandas dataframe
        dataframe containing all variables measured by the small attached weather station 
    
    """
    origin_dir = os.getcwd()        
    # Change to directory that includes the files to be read                                      
    os.chdir(path)   

    # Scan list fo all dates of selected period (Must be slightly altered from original syntax)
    filenames = sorted(glob.glob('*M'+month+'*.csv'))      
    

    # Get the column names
    uh_cols  = ['Horizontal Wind Speed (m/s) at '+str(h)+'m' for h in zephir_levels]    
    wd_cols  = ['Wind Direction (deg) at '+str(h)+'m' for h in zephir_levels]  
    w_cols   = ['Vertical Wind Speed (m/s) at '+str(h)+'m' for h in zephir_levels]
    met_cols = ['Met Tilt (deg)', 'Met Compass Bearing (deg)',  
                'Met Air Temp. (C)', 'Met Pressure (mbar)', 'Met Humidity (%)', 
                'Met Wind Speed (m/s)', 'Met Wind Direction (deg)']    
    pos_col = ['GPS']
    
    zephir = pd.DataFrame()
    for file in filenames:
        zephir_buf = pd.read_csv(file,delimiter=delimiter,skiprows=1)
        del zephir_buf[zephir_buf.columns[-1]]

        if delimiter == ';':
            # Replace all "," with "."
            for col in zephir_buf.columns[zephir_buf.columns.str.contains('Speed|Direction')]:
                zephir_buf[col] = zephir_buf[col].str.replace(",",".").astype(float, errors = 'ignore')

            for col in met_cols[1:-2]:    
                zephir_buf[col] = zephir_buf[col].str.replace(",",".").astype(float, errors = 'ignore')

            time_stamp = pd.to_datetime(zephir_buf['Time and Date'], format = '%d.%m.%Y %H:%M:%S')
        else:
            time_stamp = pd.to_datetime(zephir_buf['Time and Date'])
        zephir_buf.index = time_stamp
        zephir = pd.concat([zephir, zephir_buf], axis=0)

    uh = zephir[uh_cols].copy() 
    uh[uh>1000] = np.nan
    wd = zephir[wd_cols].copy() 
    wd[wd>1000] = np.nan
    w = zephir[w_cols].copy() 
    w[w>1000] = np.nan
    met = zephir[met_cols].copy()
    met[met>1000] = np.nan
    
    # Rotate the wind direction
    wd = wd + rot
    wd[wd>360] = wd[wd>360] - 360
    wd[wd<0] = wd[wd<0] +360
    
#    lat = []
#    lon = []
#    for i in zephir.index:
#        try:
#            lat = np.append(lat, float(zephir['GPS'].str.split(' ')[i][0]))
#            lon = np.append(lon, float(zephir['GPS'].str.split(' ')[i][1]))
#        except ValueError:
#            lat = np.append(lat, np.nan)
#            lon = np.append(lon, np.nan)
#    
#    position = pd.DataFrame({'lat':lat, 'lon':lon}, index = zephir.index)
    
    os.chdir(origin_dir)   
    
    return uh, wd, w, met#, position

def read_zephir_spectra(directory, filename):
    """
    Some test data:
    directory = '/scratch/Data/Zephir/Spectra/'
    filename = 'spectra_test.zph.csv'

    """
    
    spectra = pd.read_csv(directory+filename)
    
    # Seperate the Bins and get the Radial velocities
    bin_names = spectra.columns[spectra.columns.str.contains('FFT Bin ')]
    spectra_bins = np.array(spectra[bin_names])
    max_data = np.nanmax(spectra_bins,axis=1)
    
    new_spectra = spectra[spectra.columns[spectra.columns.str.contains('FFT Bin ')]].copy()
    new_spectra_index = pd.to_datetime(spectra['Time and Date'], format='%m/%d/%Y %I:%M:%S %p')
    
    bin_pos = []
    for i in range(len(spectra_bins)):
        bin_pos.append(np.where(spectra_bins[i,:]== max_data[i])[0][0])
    
    # Estimate the corresponding doppler frequency  
    doppler_freq = 195.31*np.array(bin_pos) *1e3
    
    # Estimate the radial velocities
    radial_vel_temp = 1.575 *1e-6 * doppler_freq/2.
    
    # Save the Radial velocities (corresponding to azimuth bin, height bin and time step)
    radial_vel = pd.DataFrame({'Timestamp':pd.to_datetime(spectra['Time and Date'], format='%m/%d/%Y %I:%M:%S %p'),
                               'Reference': spectra['Reference'],
                              'Height (m)': spectra['Height (m)'],
                              'Phase (rad)': spectra['Phase (rad)'],
                              'Radial velocities (m/s)':radial_vel_temp})
      
    ## Check the maximum estimate
#    plt.figure()
#    plt.pcolormesh(np.log(spectra[bin_names][100:150].transpose()))
#    plt.plot(np.array(bin_pos)[100:150],'r')  
    
    return radial_vel
      
# =============================================================================
# Windcube V2   
# =============================================================================

def get_WindcubeV2_header(filename):
    """
    Get the information of the Windcube V2 file header 
    """

    fil = open(filename,'rb')   
    lines = fil.readlines()
        
    header1 = lines[0].decode('latin-1')
    header1 = header1.replace('\r\n','')
    header1 = header1.split('=')
    HeaderLength = int(header1[1])
        
    header = [i.decode('latin-1') for i in lines[0:HeaderLength+1]]    
    header = [i.replace('\n','') for i in header]
    header = [i.replace('\t',' ') for i in header]
        
    # Build dictionary for the header 
    header_dic = {}
    for lin in header:
        if '=' in lin:
            splt = lin.split('=')           
            if splt[0] == 'InitialLD1(mA)' or splt[0] == 'InitialLD2(mA)':
                header_dic[splt[0]] = splt[2]
            elif len(splt)>2:
                print('manual add required, add -elif- statement')  
                print(splt)
            else:
                header_dic[splt[0]] = splt[1]   
                    
    # Get the column names from header
    column_names = lines[HeaderLength+1].decode('latin-1') 
    column_names = column_names.split('\t')                 # split where there was originally a tab (\t)
    column_names.remove('\n')                               # remove all \n (case for last enterence)
        
    # Get the height/altitude levels from header
    height_level = header_dic['Altitudes (m)'].split(' ')
    height_level = [int(i) for i in list(filter(None, height_level))]

    header     = header_dic 
    header_len = HeaderLength
    col_names  = column_names
    level      = height_level # Altitude level
    
    return header, header_len, col_names, level
        
def read_raw_WindcubeV2(filenames):
    """
    Read the raw data of the Windcube V2 dataset
    """
       
    for file in filenames:
            
        # get the header info
        header, header_len, col_names, level = get_WindcubeV2_header(file)
        buffer = pd.read_csv(filepath_or_buffer=file,
                             sep='\t',
                             header = None,
                             skiprows = header_len+2,
                             names = col_names,
                             usecols = range(len(col_names)),
                             index_col = False)
            
        # Convert index column to datetime object
        buffer.index = pd.to_datetime(buffer[col_names[0]].tolist(),
                                      format='%Y/%m/%d %H:%M:%S.%f')
        try:
            data
        except NameError:
            data = buffer
            
            
        # Accumulate read data in one DataFrame 
        data = pd.concat([data,buffer])  
        
    # Check if the right data location was defined
    try:
        data
    except UnboundLocalError:
        return print('No data found \nPlease enter a different data location in order to read raw data')

    # Remove possible duplicated rows
    data = data[~data.index.duplicated()]
    
    return data

def read_Windcube_processed_netcdf(directory,identifier):
    """
    """
    # Get the path of current (origin) directory
    origin_dir = os.getcwd()        
    # Change to directory that includes the files to be read                                      
    os.chdir(directory) 
      
    # Get filenames corresponding to ending .nc from current directory
    names = sorted(glob.glob('*'+identifier+'*.nc'))

    time  = {}
    W     = {} # vertical wind speed
    U   = {} # u wind speed
    V   = {} # v wind speed

    data_all = pd.DataFrame()      
    for name in names:
        dataset = Dataset(name, 'r')
        W[name] = dataset['z_wind_speed'][:,:].data
        W[name][W[name]<-10] = np.nan
        U[name] = dataset['x_wind_speed'][:,:].data
        U[name][U[name]<-90] = np.nan
        V[name] = dataset['y_wind_speed'][:,:].data
        V[name][V[name]<-90] = np.nan      
            
        time[name] = dataset['time'][:].data

        data = pd.DataFrame(index = pd.to_datetime(num2date(time[name],units = 'seconds since 1970-01-01 00:00:00')))
        for i in range(W[name].shape[1]):
            data['z_wind_speed_'+str(i)]     = W[name][:,i]    
            data['x_wind_speed_'+str(i)]     = U[name][:,i]
            data['y_wind_speed_'+str(i)]     = V[name][:,i]
                  
            # Estimate the horizontal wind speed and wind direction
            data['wind_speed_'+str(i)], data['wind_direction_'+str(i)] = get_wind_from_vector(u=U[name][:,i],v= V[name][:,i])
                  
        data_all = pd.concat([data_all,data],axis=0)
        dataset.close()
    os.chdir(origin_dir)      
    return data_all

# =============================================================================
# =============================================================================
# =============================================================================
########### Other remote sensing instrumentation ##############################
# =============================================================================
# =============================================================================
# =============================================================================

# =============================================================================
# Hatpro Radiometer
# =============================================================================

def read_Hatpro(directory,identifier):
    """
    """
    # Get the path of current (origin) directory
    origin_dir = os.getcwd()        
    # Change to directory that includes the files to be read                                      
    os.chdir(directory)     
    
    filenames = sorted(glob.glob('*'+identifier+'*.nc'))    
    
    data = pd.DataFrame()
    temp = pd.DataFrame()

    for file in filenames:
        buffer = pd.DataFrame()
        buffer_dict = {}
        dataset = Dataset(file, 'r')
        # Read the variables
        if identifier == 'iwv-lwp':
            buffer['liquid_water_path'] = dataset['liquid_water_path'][:].data
            buffer['integrated_water_vapour'] = dataset['integrated_water_vapour'][:].data
            buffer.index = num2date(dataset['time'][:].data, units = dataset['time'].units)  
            buffer['integrated_water_vapour'][buffer['integrated_water_vapour']<0] = np.nan
            buff_temp = pd.DataFrame()
        else:  
            for variable in dataset.variables.keys():
                if len(dataset[variable].shape) == 1:
                    buffer[variable] = dataset[variable][:]
                elif len(dataset[variable].shape) == 2:
                    buffer_dict[variable] = dataset[variable][:,:].data
                if 'time' in buffer.columns:
                    buffer.index = num2date(buffer.time, units = dataset['time'].units)  
            if identifier == 'boundary-layer-temperature-profiles':
                buff_temp = pd.DataFrame(buffer_dict['air_temperature'],
                                         index = buffer.index,
                                         columns = buffer_dict['altitude'][0,:])  
            elif identifier == 'moisture-profiles':
                 buff_temp = pd.DataFrame(buffer_dict['relative_humidity'],
                                          index = buffer.index,
                                         columns = buffer_dict['altitude'][0,:])    

        data = pd.concat([data,buffer], axis =0)
        temp = pd.concat([temp,buff_temp], axis =0)
        dataset.close()

    os.chdir(origin_dir)     
    return data, temp

def read_MRR(directory):
    """
    """
    origin_dir = os.getcwd()        
    # Change to directory that includes the files to be read                                      
    os.chdir(directory)     
    
    filenames = sorted(glob.glob('*.nc'))  

    v_t = pd.DataFrame()
    Ze  = pd.DataFrame()
    for file in filenames:
        dataset = Dataset(file)

        raw_time_buf = dataset['time'][:].data
        time = num2date(raw_time_buf, units = dataset['time'].units)
        spectral_vel_bin = dataset['velocity'][:].data
        height = dataset['height'][:].data

        # mean (integrated) velocity of most significant peak
        v_t_buf = dataset['W'][:].data
        v_t_buf[v_t_buf<=-9999] = np.nan
        v_t_buf = pd.DataFrame(v_t_buf, index=time, columns = height[0,:])
    
        # Get the equivalent Radar Reflectivity
        Ze_buf = dataset['Ze'][:].data
        Ze_buf[Ze_buf<=-9999] = np.nan
        Ze_buf = pd.DataFrame(Ze_buf, index=time, columns = height[0,:])

#        # Get the doppler spectral density
#        dsd = dataset['eta'][:].data

        dataset.close()
    
        # Combine the datasets
        v_t = pd.concat([v_t, v_t_buf], axis=0)
        Ze  = pd.concat([Ze, Ze_buf], axis=0)
    os.chdir(origin_dir)        
    return v_t, Ze

# =============================================================================
###############################################################################
################################ SATELLITE ####################################
###############################################################################
# =============================================================================
    
def read_sst_from_sat(filename, lon_lim = [-180,180], lat_lim = [-90,90]):
    """
    Some test data:
    directory = '/scratch/Data/SST_global_EC/'
    filename = '20180226120000-CMC-L4_GHRSST-SSTfnd-CMC0.1deg-GLOB-v02.0-fv03.0.nc'
    """
    
    # open the netcdf dataset
    dataset = Dataset(filename)

    # get all variable names from the dataset
    variables = [i for i in dataset.variables]
    
    # Get the dimension name of the dataset
    dim = [i for i in dataset.dimensions]    
    
    # Get the time vector of the dataset 
    time = num2date(dataset[dim[0]][:].data, units=dataset[dim[0]].units)    
    
    latitude  = dataset[variables[1]][:].data
    longitude = dataset[variables[2]][:].data
    
    sst       = dataset[variables[3]][0,:,:].data
    error     = dataset[variables[4]][0,:,:].data
    sea_ice   = dataset[variables[5]][0,:,:].data
    mask      = dataset[variables[6]][0,:,:].data
    
    # Define the longitude and longitude limitations
    lon_limits = np.where((longitude>lon_lim[0]) & (longitude < lon_lim[1]))[0]
    lat_limits = np.where((latitude>lat_lim[0]) & (latitude < lat_lim[1]))[0]
    
    dataset.close()
    # Return the part wanted for the analysis
    return time, latitude[lat_limits], longitude[lon_limits], \
           sst[:,lon_limits][lat_limits,:], sea_ice[:,lon_limits][lat_limits,:], \
           error[:,lon_limits][lat_limits,:], mask[:,lon_limits][lat_limits,:]
    
