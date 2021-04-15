#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M_GetCountry
------------

Returns country codes from GeoCoordinates
"""

import shapefile
import sys
from pathlib  import Path
from shapely.geometry import Point, Polygon
import multiprocessing as mp

#Context Manager for time measurement
import time
import os
import contextlib


#Example for Use:
#    countrypolydict=CountryPolyDict()
#    for i,pipeline in enumerate(OSM.PipeLines):
#        countrys=CountryCheckfromList(pipeline.long,pipeline.lat,countrypolydict)
#        print(i,countrys)


def get_CC_List():
    countrylist = ['BA', 'DE', 'ES', 'FR', 'GB', 'IT', 'NL', 'AT', 'BE', 'CZ', 'DK',
                   'FI', 'GR', 'HU', 'LV', 'LI', 'LT', 'LU', 'NO', 'PL', 'CH', 'PT',
                   'RO', 'IE', 'HR', 'SI', 'SK', 'RS', 'ME', 'MK', 'BG', 'AL', 'CY',
                   'MT', 'SE', 'IS', 'EE', 'TR', 'BY', 'MD', 'AM', 'AZ', 'GE', 'SA',
                   'UA', 'RU', 'XX']
    return countrylist


def get_CC_List_EU27():
    countrylist = [ 'BE', 'BG', 'DK', 'DE', 'EE', 'FI', 'FR', 'GR', 'IE', 'IT',
                   'HR', 'LV', 'LT', 'LU', 'NL', 'AT', 'PL', 'PT', 'RO', 'SK', 'ES',
                   'SE', 'CZ', 'HU', 'CY', 'XX']

         # 'GB',
         #           'LI',  'NO', 'CH',
         #            'SI', 'RS', 'ME', 'MK', 'AL',
         #           'MT', 'IS', 'TR', 'BY', 'MD', 'AM', 'AZ', 'GE', 'SA',
         #           'UA', 'RU']
    return countrylist

def get_CC_List_EU28():
    countrylist = [ 'BE', 'BG', 'DK', 'DE', 'EE', 'FI', 'FR', 'GR', 'IE', 'IT',
                   'HR', 'LV', 'LT', 'LU', 'NL', 'AT', 'PL', 'PT', 'RO', 'SK', 'ES',
                   'SE', 'CZ', 'HU', 'CY', 'XX', 'GB']

         #            'SI', 'RS', 'ME', 'MK', 'AL', 'LI',  'NO', 'CH', 'UA', 'RU'
         #           'MT', 'IS', 'TR', 'BY', 'MD', 'AM', 'AZ', 'GE', 'SA',]
    return countrylist


def get_CC_List_EU28_exXX():
    countrylist = [ 'BE', 'BG', 'DK', 'DE', 'EE', 'FI', 'FR', 'GR', 'IE', 'IT',
                   'HR', 'LV', 'LT', 'LU', 'NL', 'AT', 'PL', 'PT', 'RO', 'SK', 'ES',
                   'SE', 'CZ', 'HU', 'CY', 'GB']
         #            'SI', 'RS', 'ME', 'MK', 'AL', 'LI',  'NO', 'CH', 'UA', 'RU'
         #           'MT', 'IS', 'TR', 'BY', 'MD', 'AM', 'AZ', 'GE', 'SA',]

    return countrylist



def get_CC_List_EU():
    countrylist = [ 'BE', 'BG', 'DK', 'DE', 'EE', 'FI', 'FR', 'GR', 'IE', 'IT',
                   'HR', 'LV', 'LT', 'LU', 'NL', 'AT', 'PL', 'PT', 'RO', 'SK', 'ES',
                   'SE', 'CZ', 'HU', 'CY', 'GB', 'CH', 'NO',  'XX', 'AL', 'LI', 'SI',
                   'RS', 'ME','MK', 'MT', 'IS', 'TR',]

                    #   'BY', 'MD', 'AM', 'AZ', 'GE', 'SA',
                    # 'UA', 'RU',]
    return countrylist




def get_CC_List_XX():
    countrylist = ['BA', 'DE', 'ES', 'FR', 'GB', 'IT', 'NL', 'AT', 'BE', 'CZ',
                   'DK', 'FI', 'GR', 'HU', 'LV', 'LI', 'LT', 'LU', 'NO', 'PL',
                   'CH', 'PT', 'RO', 'IE', 'HR', 'SI', 'SK', 'RS', 'ME', 'MK',
                   'BG', 'AL', 'CY', 'MT', 'SE', 'IS', 'EE', 'TR', 'BY', 'MD',
                   'AM', 'AZ', 'GE', 'SA', 'RU', 'UA', 'DZ', 'TN', 'KZ', 'MA',
                   'EG', 'JO', 'SY', 'IQ', 'IR', 'KW', 'IL', 'LY',]
    return countrylist



@contextlib.contextmanager
def benchmark(name):
    start = time.time()
    yield
    print('{} {:.2f}s'.format(name, time.time() - start))




def CountryPolyDict(FileName_Map,predicted_countrycodes = ''):
    '''Creates and Returns Dictionary {countrycode:list_of_polygons_for_that_country}
    Uses Shapefile
    Only Countries in the list country tested'''

    countrypolydict={}
#    if sys.platform == 'win32':
#       RelDirName      = './TM_World_Borders'
#        dataFolder      = Path.cwd()
#        filename        = dataFolder /  RelDirName
#        FileName_Map    = str(filename / 'TM_WORLD_BORDERS-0.3.shp')
#    else:
#        FileName_Map     = os.path.join(os.getcwd(),'TM_World_Borders/TM_WORLD_BORDERS-0.3.shp')


    #print(os.path.isfile(FileName_Map))

    sf          = shapefile.Reader(FileName_Map, encoding="latin1")
    polygon     = sf.shapes()
    countrylist = get_CC_List()

    #speed up the routine if countrycode is correctly predicted
    countrys=[]
    if predicted_countrycodes!='':
        if isinstance(predicted_countrycodes,str):
            predicted_countrycodes=[predicted_countrycodes]
            for predicted_countrycode in predicted_countrycodes:
                if predicted_countrycode in countrylist:
                    countrys.append(predicted_countrycode)
                    countrylist.remove(predicted_countrycode)
            countrys.extend(countrylist)
    else:
        countrys=countrylist


    for i,poly in enumerate(polygon):
            if sf.record(i)[1] in countrys:
                geoshapelist=[]
                for shape in poly.__geo_interface__['coordinates']:
                    if isinstance(shape, list):
                        geoshape=Polygon(shape[0])
                    else:
                        geoshape=Polygon(shape)
                    geoshapelist.append(geoshape)
                countrypolydict.update({sf.record(i)[1]:geoshapelist})
    return countrypolydict




def GetCountry(TM_World_Borders_file,long, lat, countrypolydict = '', predicted_countrycodes = ''):
    '''Get and return countrycode of the point(long,lat) else returns '??' as countrycode'''

    # get default country codes for europe
    if countrypolydict == '':
        countrypolydict = CountryPolyDict(TM_World_Borders_file,predicted_countrycodes)

    p1          = Point(long,lat)
    res_country = 'XX'
    found       = False

    for country in countrypolydict:
        for shape in reversed(range(len(countrypolydict[country]))):
            if p1.within(countrypolydict[country][shape]):
                res_country = country
                found       = True
                break
        if found:
            break
    return res_country




def GetCountries(long, lat, countrypolydict = '', predicted_countrycodes = ''):
    '''Get and return countrycode of the point(long,lat) else returns '??' as countrycode'''

    # get default country codes for europe
    if countrypolydict == '':
        countrypolydict = CountryPolyDict(TM_World_Borders_file,predicted_countrycodes)

    res_country = []
    N_long      = len(long)

    for idx in range(N_long):
        res_country.append('XX')

    for idx in range(N_long):
        p1          = Point(long[idx], lat[idx])
        found       = False

        for country in countrypolydict:
            for shape in reversed(range(len(countrypolydict[country]))):
                if p1.within(countrypolydict[country][shape]):
                    res_country[idx]    = country
                    found               = True
                    break
            if found:
                break


    return res_country




def GetCountry4List(TM_World_Borders_file,long_list, lat_list, countrypolydict, predicted_countrycodes = ''):
    '''Calls CountryCheck for list of Points (e.g Pipelinepoints)
    Gets the countrypolydict from CountryPolyDict()
    Returns countrycodeslist'''

    countrycodelist=[]
    for long,lat in zip(long_list,lat_list):
        country=GetCountry(TM_World_Borders_file,long,lat,countrypolydict,predicted_countrycodes)
        countrycodelist.append(country)
    return countrycodelist




def GetCountry4Component(component, countrypolydict='',predicted_countrycodes=''):
    '''Get countrycodes 4 all geopoints of a Netclass component e.g. OSM.PipeLines
    Returns list of list with country_codes'''

    if countrypolydict=='':
        countrypolydict=CountryPolyDict()
    with mp.Pool() as pool:
        jobs = [pool.apply_async(GetCountry4List, args=(element.long, element.lat,
                countrypolydict,predicted_countrycodes)) for element in component]
        results=[x.get() for x in jobs]

    return results




#Quicktest of function
if __name__=="__main__":
    import os
    os.chdir('..')
    dicta=CountryPolyDict()
    print(GetCountry(-6.28,53.35,dicta,['IE','ES']))  #IE
    print(GetCountry(-3.2100984,40.3900748,dicta)) #ES

