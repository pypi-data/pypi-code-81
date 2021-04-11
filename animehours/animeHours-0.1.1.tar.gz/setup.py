from distutils.core import setup
setup(      
  name = "animeHours",  
  packages = ['animeHours'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Find the amount of hours you took to watch the anime you love.',   # Give a short description about your library
  author = 'Greeny127',                   # Type in your name
  url = 'https://github.com/Greeny127/AnimeHoursFinder',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Greeny127/AnimeHoursFinder/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['ANIME', 'HOURS', 'MYANIMELIST', 'MAL', 'TOTAL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'mal-api'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7'      #Specify which pyhton versions that you want to support
  ],
)