"""
increment_version.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""


import yaml

# Read in version
with open('version.yml', 'r') as f:
    version = yaml.safe_load(f.read())

# Strip "dev" out of micro
version['micro'] = int(str(version['micro']).replace('dev', ''))

# Update patch
version['micro'] += 1

# Add "dev" back to patch
if version['micro'] != 0:
    version['micro'] = 'dev' + str(version['micro'])

# Output version
with open('version.yml', 'w') as f:
    yaml.safe_dump(version, f, sort_keys=False)

# Transform version dict to string
version = '.'.join([str(version[key]) for key in ['major', 'minor', 'micro']])

# Write version string to uplot/_version.py
with open('uplot/version.py', 'w') as f:
    f.write("__version__ = '{}'\n".format(version))

# Return
print(version)
