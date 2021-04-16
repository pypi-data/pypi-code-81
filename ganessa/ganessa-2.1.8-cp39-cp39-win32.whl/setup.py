# -*- coding: utf-8 -*-
'''Build ganessa wheel package from source
Requires C and fortran compilers'''
#
# Building requires the following commands
# for python 2.7 (using Visual Studio 2013 and intel Fortran 2018):
#   call "C:\Program Files (x86)\Intel\Composer XE 2015\bin\compilervars.bat" ia32 vs2013
#   set VS90COMNTOOLS=%VS120COMNTOOLS%
# for python 3.5 - 3.7 (using Visual Studio 2015 and Intel Fortran 2018):
#	call "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2018\windows\bin\compilervars.bat" ia32 vs2015
#	set "PATH=%PATH%;C:\Program Files (x86)\Windows Kits\8.1\bin\x86"
# for python 3.8 (using Visual Studio 2019 and Intel Fortran 2020):
#	call "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020\windows\bin\compilervars.bat" ia32 vs2019
#	set "PATH=%PATH%;C:\Program Files (x86)\Windows Kits\8.1\bin\x86"
#
# python setup.py bdist_wheel
#
from __future__ import (print_function)
from sys import version_info, maxsize
import os.path as OP
from os import walk
from codecs import open as copen
import setuptools
from numpy.distutils.core import setup, Extension
from distutils.command.build_py import build_py

# from setuptools import setup

PY3 = version_info.major == 3
X64 = maxsize > 2**32

try:
    from ganessa import __version__ as version
    # from ganessa.sim import _lang
    print('version is', version) #, _lang
    del ganessa
except:
    print('ganessa not found: rebuilding')

HERE = OP.abspath(OP.dirname(__file__))

def readme():
    '''Get the long description from the README file'''
    with copen(OP.join(HERE, 'README.rst'), encoding='utf-8') as f:
        text = f.read()
    with copen(OP.join(HERE, 'Example', 'Example.py'), encoding='utf-8') as f:
        # text += f.read()
        for line in f:
            text += ' ' + line
    text += '\n'
    return text

DIRF90 = OP.join(HERE, 'gandll')
FOPTIONS = ['/MT']
# foptions = []

# base Ganessa_SIM / Picwin32 API - multiple versions
if X64:
    dll_src_lib = [('_pygansim', 'pyGanSim', 'Ganessa_SIM_x64')]
else:
    dll_src_lib = [('_pygansim', 'pyGanSim', 'Ganessa_SIM'),
                   ('_pygan_th', 'pyGanSim', 'Ganessa_TH'),
                   ('_pygansim2021', 'pyGanSim2021', 'PicWin32-2021'),
                   ('_pygan_th2021', 'pyGanSim2021', 'FrigWin32-2021'),
                   ('_pygansim2020', 'pyGanSim2020', 'PicWin32-2020'),
                   ('_pygansim2018b', 'pyGanSim2018b', 'PicWin32-2018b'),
                   ('_pygansim2018', 'pyGanSim2018', 'PicWin32-2018'),
                   ('_pygan_th2018', 'pyGanSim2018', 'FrigWin32-2018'),
                   ('_pygansim2017b', 'pyGanSim2017b', 'PicWin32-2017b'),
                   ('_pygansim2017', 'pyGanSim2017', 'PicWin32-2017'),
                   ('_pygan_th2017', 'pyGanSim2017', 'FrigWin32-2017'),
                   ('_pygansim2016b', 'pyGanSim2016b', 'PicWin32-2016b'),
                   ('_pygan_th2016b', 'pyGanSim2016b', 'FrigWin32-2016b'),
                   ]
if not PY3:
    dll_src_lib += [
                   ('_pygansim2016a', 'pyGanSim2016a', 'PicWin32-2016a'),
                   ('_pygansim2016', 'pyGanSim2016', 'PicWin32-2016'),
                   ('_pygan_th2016', 'pyGanSim2016', 'FrigWin32-2016'),
                   ('_pygansim2015', 'pyGanSim2015', 'PicWin32-2015'),
                   ('_pygan_th2015', 'pyGanSim2015', 'FrigWin32-2015'),
                   ('_pygansim2014', 'pyGanSim2014', 'PicWin32-2014')]

# API to Flexnet license manager
dll_src_lib.append(('_prot', 'pyProtDLL', 'ProtDLL' + ('_x64' if X64 else '')))

extdlls = [Extension(name='ganessa.' + dll,
                     sources=[OP.join(DIRF90, src + '.f90')],
                     library_dirs=[DIRF90],
                     libraries=[lib],
                     extra_f90_compile_args=FOPTIONS,
                     extra_compile_args=FOPTIONS,
                    ) for dll, src, lib in dll_src_lib]

# Compiled functions
extdlls.append(Extension(name='ganessa._pyganutl',
                         sources=[OP.join(DIRF90, 'pyGanUtil.f90')],
                         extra_f90_compile_args=FOPTIONS,
                         extra_compile_args=FOPTIONS))

# Epanet 2.00.12 DLL
epa20toolfld = OP.join(HERE, 'epanettools-0.4.2')
epa20_srcfld = OP.join(epa20toolfld, 'epanet')
epa20src = [OP.join(p, f) for p, _d, files in walk(epa20_srcfld)
                            for f in files if OP.splitext(f)[1] == '.c']
epa20src.append(OP.join(epa20toolfld, 'epanet2_wrap.c'))
extdlls.append(Extension(name='ganessa._epanet2',
                         sources=epa20src,
                         extra_compile_args=FOPTIONS))

# Epanet 2.2.0 DLL
EN22OPTS = ['/D "epanet_py_EXPORTS"']
EN22OPTS = ['/D "_WIN32"']
epa22toolfld = OP.join(HERE, 'epanettools-2.2.0')
epa22_srcfld = OP.join(epa22toolfld, 'epanet')
epa22src = [OP.join(p, f) for p, _d, files in walk(epa22_srcfld)
                            for f in files if OP.splitext(f)[1] == '.c']
epa22src.append(OP.join(epa22toolfld, 'epanet2_wrap.c'))
# extdlls.append(Extension(name='ganessa._epanet22',
#                          sources=epa22src,
#                          extra_compile_args=FOPTIONS + EN22OPTS))

CLASSIFY = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Win32 (MS Windows)",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "License :: Free To Use But Restricted",
    "License :: Other/Proprietary License",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Fortran",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    ]
NUMPY_RQ = (('1.15.1' if version_info.minor >= 7 else '1.13.1') if PY3 else '1.11')
setup(name='ganessa',
      version=version,
      description='Python interface to Piccolo and Picalor simulation kernel',
      long_description=readme(),
      author='Dr. Pierre Antoine Jarrige',
      author_email='ganessa@safege.fr',
      license='commercial',
      classifiers=CLASSIFY,
      keywords='Piccolo Picalor Ganessa',
      packages=['ganessa'],
      # package_data={'ganessa': ['_epanet2.pyd']},
      include_package_data=True,
      data_files=[('ganessa', ['docs/pyGanessa.html', 'docs/pyGanessa.css'])],
      ext_modules=extdlls,
      install_requires=['numpy>=' + NUMPY_RQ],
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
      # cmdclass = {'build_py': build_py},
      )
