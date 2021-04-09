import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
  long_description = fh.read()
setup(
  name = 'ProbotDB',         # How you named your package folder (MyLib)
  packages = ['ProbotDB'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'ProBot embed messages feature based database, :shitoh:',   # Give a short description about your library
  long_description= long_description,
  author = 'Etherl',                   # Type in your name
  author_email = 'None@domain.com',      # Type in your E-Mail
  url = 'https://github.com/Etherll/probot.db',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Etherll/probot.db',    # I explain this later on
  keywords = ['probotdb', 'probot', 'db'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests'
      ],
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
  ],
)
