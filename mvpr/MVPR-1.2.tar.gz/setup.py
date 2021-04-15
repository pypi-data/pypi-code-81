from setuptools import setup


setup(
  name = 'MVPR',         # How you named your package folder (MyLib)
  packages = ['MVPR'],   # Chose the same as "name"
  version = '1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Multi-variable polynomial regression for curve fitting.',   # Give a short description about your library
  author = 'Joel Hampton',                   # Type in your name
  author_email = 'joelelihampton@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/Joel-H-dot/MVPR',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Joel-H-dot/MVPR/archive/refs/tags/1.1.tar.gz',    # I explain this later on
  keywords = ['Machine Learning', 'Regression', 'polynomial'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'sklearn.preprocessing',
          'scipy.linalg'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research ',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)