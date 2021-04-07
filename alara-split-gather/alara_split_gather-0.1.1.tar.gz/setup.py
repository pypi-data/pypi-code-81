from setuptools import setup, find_packages
 
setup(name='alara_split_gather',
      version='0.1.1',
      url='https://github.com/zxkjack123/alara_split_gather',
      license='MIT',
      author='Xiaokang Zhang',
      author_email='zxkjack123@163.com',
      description='Python package to split and gather ALARA tasks',
      packages=find_packages(exclude=['tests']),
      package_dir={'alara_split_gather':'alara_split_gather'},
      include_package_data=True,
      package_data={'alara_split_gather':[
                        ],
                    },
      long_description=open('README.md').read(),
      entry_points={
          "console_scripts":["alara_split_task = alara_split_gather.alara_split_task:alara_split_task",
                             "alara_tasks_status = alara_split_gather.check_tasks_status:alara_tasks_status",
                             "alara_gather_tasks = alara_split_gather.alara_gather_tasks:alara_gather_tasks"
                             ]
          },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Environment :: Console",
          ],
      python_requires='>=3.6',
      zip_safe=False)
