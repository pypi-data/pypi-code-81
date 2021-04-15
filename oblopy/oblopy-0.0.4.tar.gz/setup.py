from distutils.core import setup

setup(
  name = 'oblopy',        
  packages = ['oblopy'],   # Chose the same as "name"
  version = '0.0.4',      # Start with a small number and increase it with every change you make
  license='bsd-3-clause',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python toolbox for reading, analysing and processing profiling Lidar observations.',   # Give a short description about your library
  author = 'Christiane Duscha',                   # Type in your name
  author_email = 'christiane.duscha@uib.no',      # Type in your E-Mail
  url = 'https://github.com/cdu022/oblopy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/cdu022/oblopy/archive/refs/tags/v0.0.4.tar.gz',   
  keywords = ['Offshore Boundary Layer Observatory (OBLO)','Marine Boundary Layer', 'Lidar','Retrieval','Motion correction','meteorology', 'bergen'],   # Keywords that define your package best
  install_requires=['matplotlib','numpy','scipy','pandas','netCDF4','cartopy','sklearn'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
