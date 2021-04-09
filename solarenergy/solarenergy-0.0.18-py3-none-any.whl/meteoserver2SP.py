#!/bin/env python3

"""Python script using the Meteoserver module to obtain a prediction for our solar panels."""

import meteoserver as meteo

myKey = 'a123456789'    # My Meteoserver API key - put your OWN key here!
myLocation = 'De Bilt'  # My location


# Weather forecast #################################################################################

# Read weather-forecast data from file:
# data = meteo.read_json_file_weatherforecast('WeatherForecast1.json', full=True)  # Option 1: HARMONIE/HiRLAM (48 (42?) hours)
# data = meteo.read_json_file_weatherforecast('WeatherForecast2.json')  # Option 2: GFS (4/10 days), useful columns only, no location
# data, location = meteo.read_json_file_weatherforecast('WeatherForecast2.json', full=True, loc=True, numeric=False)  # Option 2, with ALL columns and location

# Get weather-forecast data from server:
# data = meteo.read_json_url_weatherforecast(myKey, myLocation, model='HARMONIE')  # Option 1: HARMONIE/HiRLAM
data, location = meteo.read_json_url_weatherforecast(myKey, myLocation, full=True, loc=True)  # Option 2, with ALL columns and location
# data = meteo.read_json_url_weatherforecast(myKey, myLocation)  # Option 2 (default): GFS, useful columns only, no location

# Print the data:
# pd.set_option('display.max_rows', None)  # Print all rows of a Pandas dataframe
print(data)
print()

# print("%10s %22s %6s %6s %4s %5s %5s %7s %7s %5s %8s %4s %5s %6s %7s %6s %6s %6s %10s %10s %3s %4s %4s %3s %3s %4s %8s %4s %3s %6s %7s" %
#       ('UNIX time', 'Date/time CET', 'offset', 'loc', 'temp', 'winds', 'windb', 'windknp', 'windkmh',
#        'windr', 'windrltr', 'gust', 'gustb', 'gustkt', 'gustkmh', 'vis', 'neersl', 'luchtd', 'luchtdmmhg', 'luchtdinhg',
#        'rv', 'gr', 'hw', 'mw', 'lw', 'tw', 'cape', 'cond', 'ico', 'samenv', 'icoon'))
# 
# print(type(data.loc[0].values[2]))
# print("%10i %22s %6i %6s %4i %5i %5i %7i %7i %5i %8s %4i %5i %6i %7i %6i %6i %6i %10i %10i %3i %4i %4i %3i %3i %4i %8i %4i %3i %6s %7s" %
#       tuple(data.loc[0].values) )


# Print numeric values:
# print(tuple(data.loc[0].values))
# print("%10i  %20s    %6.2f  %6.2f    %3i  %4i  %3i   %4i  %4i  %4i  %4i    %6i  %6.1f" % tuple(data.loc[0].values) )

# Write the downloaded data to a json file:
meteo.write_json_file_weatherforecast('WeatherForecast2a.json', location, data)

# exit()


# Sun forecast #####################################################################################

# Print some help:
# meteo.print_help_sunData()

location = 'Test'

# Read a Meteoserver Sun-data JSON file from disc:
# current, forecast = meteo.read_json_file_sunData('SunData.json')
current, forecast, location = meteo.read_json_file_sunData('SunData.json', loc=True, numeric=False)  # Return the location

# Get Meteoserver Sun data from the server for the given location (and key):
# current, forecast = meteo.read_json_url_sunData(myKey, myLocation)
# current, forecast, location = meteo.read_json_url_sunData(myKey, myLocation, loc=True)  # Return the location

# Print the current-weather and forecast dataframes:
print("\nCurrent Sun/weather observation from a nearby station:")
print(current)

print("\nSun/weather forecast for the selected location/region:")
print(forecast)


# print(tuple(current.loc[0].values))
# print("%20s  %10s  %20s    %6s  %6s   %3s  %4s  %3s   %4s  %6s  %6s   %20s  %20s" %
#       ('Location', 'UNIX time', 'Date/time CET',  'Elev', 'Az',  'Temp', 'Rad', 'Sun', 'Cld', 'vis', 'prec',  'sr', 'ss'))
# print("%20s  %10i  %20s    %6.2f  %6.2f    %3i  %4i  %3i   %4i  %6i  %6.1f   %20s  %20s" % tuple(current.loc[0].values) )
# 
# print()
# 
# print(tuple(forecast.loc[0].values))
# print("%10s  %20s    %6s  %6s   %3s  %4s  %3s   %4s  %4s  %4s  %4s    %6s  %6s" % ('UNIX time', 'Date/time CET',  'Elev', 'Az',  'Temp', 'Rad', 'Sun', 'Cld', 'Lcl','Mcl','Hcl', 'vis', 'prec'))
# print("%10i  %20s    %6.2f  %6.2f    %3i  %4i  %3i   %4i  %4i  %4i  %4i    %6i  %6.1f" % tuple(forecast.loc[0].values) )

# Write the downloaded data to a json file:
meteo.write_json_file_sunData('SunData1.json', location, current, forecast)

