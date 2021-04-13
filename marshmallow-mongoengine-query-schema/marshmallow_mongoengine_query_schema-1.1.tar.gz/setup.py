from distutils.core import setup
setup(
  name = 'marshmallow_mongoengine_query_schema',
  packages = ['marshmallow_mongoengine_query_schema'],
  version = '1.1',
  license='MIT',
  description = 'Marshmallow schema for generating mongoengine filters in url query.',
  author = 'Damian Komorowski',
  author_email = 'verdequar@gmail.com',
  url = 'https://github.com/VerdeQuar/marshmallow_mongoengine_query_schema',
  download_url = 'https://github.com/VerdeQuar/marshmallow_mongoengine_query_schema/archive/refs/tags/v1.1.tar.gz',
  keywords = ['mongoengine', 'marshmallow', 'schema'],
  install_requires=[
          'marshmallow',
          'mongoengine',
          'webargs'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)