import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup

package_name = "leadguru_jobs"

def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


try:
    version_parts = versions()[0].split(".")
except:
    version_parts = "0.0.0".split(".")

version_parts[1] = f'{float(version_parts[1]) + 1}'
last_version = ".".join(version_parts[0:-1])

setup(name=package_name,
      version=f'{last_version}',
      description='LGT jobs builds',
      packages=['lgt_jobs'],
      include_package_data=True,
      install_requires=[
          'loguru',
          'leadguru-common>=0.37.0',
          'leadguru-data>=0.36.0',
          'pydantic==1.8.1'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'Environment :: Console',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet',
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
