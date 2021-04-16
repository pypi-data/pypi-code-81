import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='figurestream',
    version='1.2',
    packages=['figurestream'],

    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',

    download_url='https://github.com/UN-GCPDS/matplotlib-figurestream',

    install_requires=['matplotlib==3.3.4',
                      'Flask==1.1.2',
                      ],

    include_package_data=True,
    license='BSD-2-Clause',
    description="A Matplotlib.Figure fork with real-time plot streaming features.",

    long_description=README,
    long_description_content_type='text/markdown',

    python_requires='>=3.8',


    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],

)



