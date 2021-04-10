from distutils.core import setup
setup(
  name = 'pyteeth',         # How you named your package folder (MyLib)
  packages = ['pyteeth'],   # Chose the same as "name"
  version = '0.12',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package is design for detectiong top 6 teeth for designing a beautiful smile',   # Give a short description about your library
  author = 'Ali Saadati',                   # Type in your name
  author_email = 'alibalaei76@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/alisaadati97/Pyteeth',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['teeth', 'smile', 'detect'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'numpy',
          'dlib',
          'imutils',

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)