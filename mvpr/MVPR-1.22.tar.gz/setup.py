from setuptools import setup


setup(
  name = 'MVPR',
  packages = ['MVPR'],
  version = '1.22',
  license='MIT',
  description = 'Multi-variable polynomial regression for curve fitting.',
  author = 'Joel Hampton',
  author_email = 'joelelihampton@outlook.com',
  url = 'https://github.com/Joel-H-dot/MVPR',
  download_url = 'https://github.com/Joel-H-dot/MVPR/archive/refs/tags/1.1.tar.gz',
  keywords = ['Machine Learning', 'Regression', 'polynomial'],
  install_requires=[
          'numpy',
          'sklearn',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research ',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)