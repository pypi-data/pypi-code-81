from distutils.core import setup
setup(
  name = 'FanucToOpc',         
  packages = ['FanucToOpc'],   
  version = '0.2.6',      
  license='lgpl',        
  description = 'Used for communicating with an opc server of an fanuc robot',   
  author = 'WvdL1995',                   
  author_email = '',      
  url = 'https://github.com/WvdL1995',   
  download_url = 'https://github.com/WvdL1995/FanucToOpc.git',   
  keywords = ['OPC', 'Fanuc', 'robot'],   
  install_requires=[           
          'opcua',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',   
    'Programming Language :: Python :: 3.7',      
  ],
)
