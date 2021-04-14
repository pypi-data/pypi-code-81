from distutils.core import setup
setup(
  name = 'pysecretlayer',
  packages = ['pysecretlayer'],
  version = '0.2',
  license='MIT', 
  description = 'Lambda layer that allows for easily loading Environment variables as secrets',
  author = 'Devin Collins',
  author_email = 'me@imdevinc.com',
  url = 'https://github.com/ImDevinC/secretlayer',
  download_url = 'https://github.com/ImDevinC/pysecretlayer/archive/refs/tags/v_02.tar.gz',    # I explain this later on
  keywords = ['aws', 'lambda', 'secretmanager'],
  install_requires=[            # I get to this in a second
          'boto3',
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
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)