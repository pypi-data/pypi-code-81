from setuptools import setup
setup(
    name='twincharm',
    packages=['twincharm.client.rpc','twincharm.server.rpc','twincharm.response','twincharm.client.objtrans','twincharm.server.objtrans'
    ],
    author='Adam Jenča',
    author_email='jenca.a@gjh.sk',
    version='1.1.1',
    url='https://github.com/jenca-adam',
    description=' RPC and Object Transfer library.',
    long_description='''Simple RPC and Object Transfer library.''',    
      ) 
