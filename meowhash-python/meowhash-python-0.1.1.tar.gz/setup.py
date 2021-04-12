import sys
from setuptools import setup, Extension


if sys.platform != 'win32':
    COMPILE_ARGS = ['-maes', '-msse', '-msse2', '-msse3', '-mssse3', '-msse4.1']
else:
    COMPILE_ARGS = []  # No need to configure SIMD on Win32

setup(
	name='meowhash-python',
	version='0.1.1',
	author='https://github.com/Pebaz',
    ext_modules=[
        Extension(
            'meow_hash_ext',
            sources=['meow_hash_ext.c'],
            headers=['meow_hash_x64_aesni.h'],
            extra_compile_args=COMPILE_ARGS
        )
    ],
    install_requires=['cpufeature'],
    data_files = [('', ['meow_hash_x64_aesni.h'])],
	py_modules=['meow_hash']
)
