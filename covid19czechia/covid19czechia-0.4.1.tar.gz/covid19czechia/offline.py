
import pandas as pd

# cache
import pkg_resources
DEATHS = pkg_resources.resource_filename(__name__, "data/deaths.csv")
CASES = pkg_resources.resource_filename(__name__, "data/cases.csv")
TESTS = pkg_resources.resource_filename(__name__, "data/tests.csv")
RECOVERED = pkg_resources.resource_filename(__name__, "data/recovered.csv")
_cache = {}

def read_deaths():
    """Read cache."""
    global _cache
    try:
        if 'deaths' not in _cache:
            _cache['deaths'] = pd.read_csv(DEATHS)
    except:
        return None
    else:
        return _cache['deaths']

def write_deaths(deaths):
    """Write cache."""
    global _cache
    deaths.to_csv(DEATHS, index = False)
    _cache['deaths'] = deaths
    
def read_cases():
    """Read cache."""
    global _cache
    try:
        if 'cases' not in _cache:
            _cache['cases'] = pd.read_csv(CASES)
    except:
        return None
    else:
        return _cache['cases']

def write_cases(cases):
    """Write cache."""
    global _cache
    cases.to_csv(CASES, index = False)
    _cache['cases'] = cases
    
def read_tests():
    """Read cache."""
    global _cache
    try:
        if 'tests' not in _cache:
            _cache['tests'] = pd.read_csv(TESTS)
    except:
        return None
    else:
        return _cache['tests']

def write_tests(cases):
    """Write cache."""
    global _cache
    cases.to_csv(TESTS, index = False)
    _cache['tests'] = cases
    
def read_recovered():
    """Read cache."""
    global _cache
    try:
        if 'recovered' not in _cache:
            _cache['recovered'] = pd.read_csv(RECOVERED)
    except:
        return None
    else:
        return _cache['recovered']

def write_recovered(cases):
    """Write cache."""
    global _cache
    cases.to_csv(RECOVERED, index = False)
    _cache['recovered'] = cases

__all__ = ["read_deaths","write_deaths",
           "read_cases","write_cases",
           "read_tests","write_tests",
           "read_recovered","write_recovered"]