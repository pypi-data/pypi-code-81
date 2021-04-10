
from datetime import datetime
from io import StringIO
import warnings

import pandas as pd
import requests

from . import offline

# change to have different age_groups
def _group5_to_range(group):
    return int(group * 5), int(group * 5 + 4)
def _age_to_group5(age):
    try:
        group = int(age) // 5
    except:
        return "UNK"
    group_range = _group5_to_range(group)
    return "%d_%d" % group_range

age_to_group = _age_to_group5
def covid_deaths(level = 1, usecache = False):
    """Returns deaths for COVID-19 in Czechia.
    
    The deaths are aggregated by week, age group (by 5 years) and sex.
    Setting of parameter *level* sets granularity of administrative unit.
    
    Args:
        level (int, optional): Granularity of administrative unit.
            * by country (level = 1) = default
            * by region (level = 2)
            * by district (level = 3)
    """
    # fallback
    if level > 3 or level < 1:
        warnings.warn("invalid level")
        return None
    
    # download
    x = offline.read_deaths() if usecache else None
    if x is None:
        mzcr_deaths_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv'
        mzcr_deaths_response = requests.get(mzcr_deaths_url)
    
        # read csv
        x = pd.read_csv( StringIO(mzcr_deaths_response.text) )
        x.columns = ["date","age","sex","region","district"]
        x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        x["sex"] = x["sex"].apply(lambda s: {"M":"M", "Z":"F"}[s])
        # alter values
        x["age_group"] = x["age"].apply(age_to_group)
        x["week"] = x["date"].apply(lambda dt: dt.isocalendar()[1])

        offline.write_deaths(x) # cache write back
    else:
        try:
            x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        except:
            pass
        
    # country level
    if level == 1:
        x = x.groupby(["date","week","age","age_group","sex"]).size().reset_index(name = 'deaths')
    # region level
    elif level == 2:
        x = x.groupby(["date","week","age","age_group","sex","region"]).size().reset_index(name = 'deaths')
    # district level
    elif level == 3:
        x = x.groupby(["date","week","age","age_group","sex","region","district"]).size().reset_index(name = 'deaths')
    
    return x

def covid_confirmed_cases(usecache = False):
    """Returns confirmed cases for COVID-19 in Czechia.
    
    Args:
        usecache (bool): True to use cache otherwise from source. By default False.
    """
    # download
    x = offline.read_cases() if usecache else None
    if x is None:
        mzcr_tests_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv'
        mzcr_tests_response = requests.get(mzcr_tests_url)

        # read csv
        x = pd.read_csv( StringIO(mzcr_tests_response.text) )
        x.columns = ["date","age","sex","region","district",'infected_abroad','country_of_infection']
        x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        x["age"] = x.age.apply(float)
        x["sex"] = x["sex"].apply(lambda s: {"M":"M", "Z":"F"}[s])
        # alter values
        x["age_group"] = x["age"].apply(age_to_group)
        x["week"] = x["date"].apply(lambda dt: dt.isocalendar()[1])
        # remove columns
        x = x[['date','age','sex','region','district','age_group','week']]\
            .sort_values(['date','region','district','age','sex'])
        
        offline.write_cases(x) # cache write back
    else:
        try:
            x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        except:
            pass
    return x\
        .reset_index(drop = True)

def covid_confirmed(level = 1, usecache = False):
    """Returns tests for COVID-19 in Czechia.
    
    The tests are aggregated by week.
    Setting of parameter *level* sets granularity of administrative unit.
    
    Args:
        level (int, optional): Granularity of administrative unit.
            * by country (level = 1) = default
            * by region (level = 2)
            * by district (level = 3)
        usecache (bool): True to use cache otherwise from source. By default False.
    """
    # fallback
    if level > 3 or level < 1:
        warnings.warn("invalid level")
        return None
    
    # fetch cases
    x = covid_confirmed_cases(usecache = usecache)
    
    # country level
    if level == 1:
        x = x.groupby(["date","week","age","age_group","sex"]).size().reset_index(name = 'confirmed')
    # region level
    elif level == 2:
        x = x.groupby(["date","week","age","age_group","sex","region"]).size().reset_index(name = 'confirmed')
    # district level
    elif level == 3:
        x = x.groupby(["date","week","age","age_group","sex","region","district"]).size().reset_index(name = 'confirmed')
    
    return x

def covid_tests(level = 1, usecache = False):
    """Returns tests for COVID-19 in Czechia.
    
    The tests are aggregated by week.
    Setting of parameter *level* sets granularity of administrative unit.
    
    Args:
        level (int, optional): Granularity of administrative unit.
            * by country (level = 1) = default
            * by region (level = 2)
            * by district (level = 3)
        usecache (bool): True to use cache otherwise from source. By default False.
    """
    # fallback
    if level > 3 or level < 1:
        warnings.warn("invalid level")
        return None
    
    # country level
    if level == 1:
        mzcr_tests_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy.csv'
        mzcr_tests_response = requests.get(mzcr_tests_url)
        # read csv
        x = pd.read_csv( StringIO(mzcr_tests_response.text) )
        x.columns = ['date','tests','cumtests','tests_new','cumtests_new']
        x['date'] = x.date.apply(lambda d: datetime.strptime(d,'%Y-%m-%d'))
        x = x[['date','tests']]
        return x
    
    # download
    x = offline.read_tests() if usecache else None
    if x is None:
        mzcr_tests_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-testy.csv'
        mzcr_tests_response = requests.get(mzcr_tests_url)
        # read csv
        x = pd.read_csv( StringIO(mzcr_tests_response.text) )
        x.columns = ["date","region","district",
                     "district_tests","district_cumtests","region_tests","region_cumtests",
                     "district_tests_first","district_cumtests_first","region_tests_first","region_cumtests_first"]
        x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        x["week"] = x["date"].apply(lambda dt: dt.isocalendar()[1])

        offline.write_tests(x) # cache write back
    else:
        try:
            x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        except:
            pass
            
    # region level
    if level == 2:
        x = x\
            .drop_duplicates(subset = ['date','week','region','region_tests',"region_tests_first"])\
            .groupby(['date','week','region'])\
            .aggregate({'region_tests': 'sum', 'region_tests_first': 'sum'})\
            .rename({'region_tests': 'tests', 'region_tests_first': 'tests_first'}, axis=1)\
            .reset_index()
        
    # district level
    elif level == 3:
        x = x\
            .drop_duplicates(subset = ['date','week','region','district','district_tests',"district_tests_first"])\
            .groupby(['date','week','region','district'])\
            .aggregate({'district_tests': 'sum', 'district_tests_first': 'sum'})\
            .rename({'district_tests': 'tests', 'district_tests_first': 'tests_first'}, axis=1)\
            .reset_index()
    
    return x

def covid_recovered_cases(usecache = False):
    """Returns recovered cases for COVID-19 in Czechia.
    
    Args:
        usecache (bool): True to use cache otherwise from source. By default False.
    """
    # download
    x = offline.read_recovered() if usecache else None
    if x is None:
        mzcr_recovered_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/vyleceni.csv'
        mzcr_recovered_response = requests.get(mzcr_recovered_url)

        # read csv
        x = pd.read_csv( StringIO(mzcr_recovered_response.text) )
        x.columns = ["date","age","sex","region","district"]
        x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        x["age"] = x.age.apply(float)
        x["sex"] = x["sex"].apply(lambda s: {"M":"M", "Z":"F"}[s])
        # alter values
        x["age_group"] = x["age"].apply(age_to_group)
        x["week"] = x["date"].apply(lambda dt: dt.isocalendar()[1])
        # remove columns
        x = x[['date','age','sex','region','district','age_group','week']]\
            .sort_values(['date','region','district','age','sex'])
        
        offline.write_recovered(x) # cache write back
    else:
        try:
            x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
        except:
            pass
    return x\
        .reset_index(drop = True)

def covid_recovered(level = 1, usecache = False):
    """Returns recovered for COVID-19 in Czechia.
    
    Setting of parameter *level* sets granularity of administrative unit.
    
    Args:
        level (int, optional): Granularity of administrative unit.
            * by country (level = 1) = default
            * by region (level = 2)
            * by district (level = 3)
        usecache (bool): True to use cache otherwise from source. By default False.
    """
    # fallback
    if level > 3 or level < 1:
        warnings.warn("invalid level")
        return None
    
    # fetch cases
    x = covid_recovered_cases(usecache = usecache)
    
    # country level
    if level == 1:
        x = x.groupby(["date","week","age","age_group","sex"]).size().reset_index(name = 'recovered')
    # region level
    elif level == 2:
        x = x.groupby(["date","week","age","age_group","sex","region"]).size().reset_index(name = 'recovered')
    # district level
    elif level == 3:
        x = x.groupby(["date","week","age","age_group","sex","region","district"]).size().reset_index(name = 'recovered')
    
    return x

def set_age_groups(callback):
    global age_to_group
    age_to_group = callback

__all__ = ["covid_deaths","covid_tests",
           "covid_confirmed_cases","covid_confirmed",
           "covid_recovered_cases","covid_recovered",
           "set_age_groups","age_to_group"]
