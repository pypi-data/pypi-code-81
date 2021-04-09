from setuptools import setup, find_packages
 
setup(name='natf',
      version='1.4.3',
      url='https://github.com/zxkjack123/NATF',
      license='MIT',
      author='Xiaokang Zhang',
      author_email='zxkjack123@163.com',
      description='Nuclear Analysis toolkit wit coupling of MCNP and FISPACT',
      packages=find_packages(exclude=['tests']),
      package_dir={'natf':'natf'},
      include_package_data=True,
      package_data={'natf':[
                        'radwaste_standards/CHN2018/*',
                        'radwaste_standards/USNRC/*',
                        'radwaste_standards/USNRC_FETTER/*',
                        'data/*',
                        ],
                    },
      long_description=open('README.md').read(),
      entry_points={
          "console_scripts":["natf_run = natf.natf_functions:natf_run",
                             "nonvoid_cells_to_tally = natf.mcnp_input:nonvoid_cells_to_tally",
                             "cell_vol_to_tally = natf.mcnp_input:cell_vol_to_tally",
                             "part_cell_list = natf.mcnp_input:part_cell_list",]
          },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Environment :: Console",
          ],
      python_requires='>=3.6',
      zip_safe=False)
