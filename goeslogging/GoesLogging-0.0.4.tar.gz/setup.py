from distutils.core import setup
setup(
  name = 'GoesLogging',
  packages = ['GoesLogging'],
  version = '0.0.4',
  license='MIT',
  description = 'First version of logging for GOES.',
  author = 'Kieran Schubert',
  author_email = 'kieran.schubert@hesge.ch',
  url = 'https://framagit.org/K-Schubert/goeslogging',
  download_url = 'https://framagit.org/K-Schubert/goeslogging/-/archive/v_004/goeslogging-v_004.tar.gz',
  keywords = ['GOES', 'Logging'],
  install_requires=[
          'elasticsearch'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)