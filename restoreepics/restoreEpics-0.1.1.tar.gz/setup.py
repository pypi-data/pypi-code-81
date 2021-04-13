from distutils.core import setup
setup(
  name = 'restoreEpics',         # How you named your package folder (MyLib)
  packages = ['restoreEpics'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple package that gives wrapped caput and writeMatrix functions for writing EPICS channels which save previous values and a restoreEpics function can be used later to restore all values in case of error, interrupt, or as a final restore.',   # Give a short description about your library
  author = 'Anchal Gupta',                   # Type in your name
  author_email = 'anchal@caltech.edu',      # Type in your E-Mail
  url = 'https://git.ligo.org/anchal.gupta/restoreepics',   # Provide either the link to your github or to your website
  download_url = 'https://git.ligo.org/anchal.gupta/restoreepics/-/archive/0.1.1/restoreepics-0.1.1.tar.gz',    # I explain this later on
  keywords = ['EPICS', 'RESTORE', 'MATRIX'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'epics',
          'argparse',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
