import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'pyGRNN',         
  packages = setuptools.find_packages(),   
  version = 'v0.1.2',      
  license='MIT',
  description = 'Python implementation of General Regression Neural Network (Nadaraya-Watson Estimator). A Feature Selection module based on GRNN is also provided',   # Give a short description about your library
  author = 'Federico Amato',                   
  author_email = 'federico.amato@unil.ch',      #
  url = 'https://github.com/federhub/pyGRNN',  
  download_url = 'https://github.com/federhub/pyGRNN/archive/v0.1.2tar.gz',    
  keywords = ['Machine Learning', 'General Regression Neural Network', 'Kernel Regression', 'Feature Selection'],   
  install_requires=[
          'pandas',
          'numpy',
          'seaborn',
          'scikit-learn',
          'matplotlib',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.6',
  ],
  )


