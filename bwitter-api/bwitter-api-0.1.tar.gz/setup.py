from distutils.core import setup
setup(
  name = 'bwitter-api',         # How you named your package folder (MyLib)
  packages = ['bwitter-api'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='lgpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An API to post to bwitter.',   # Give a short description about your library
  author = 'Hiew Jun Ian',                   # Type in your name
  author_email = 'wokintosh@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/pixdoet/bwitter-api',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/pixdoet/bwitter-api/archive/refs/tags/1.0a.tar.gz',    # I explain this later on
  keywords = ['bwitter','bwitter-api','bwitter api'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)   