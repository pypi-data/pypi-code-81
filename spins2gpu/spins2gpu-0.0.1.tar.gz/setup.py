from setuptools import setup
setup(
    name='spins2gpu',
    version='0.0.1',
    author='lkccrr',
    author_email='luokan@hrbeu.edu.cn',
    url='https://github.com/lkccrr/spins2gpu',
    packages=['spins2gpu'],
    install_requires=[
        'numba',
        'numpy',
        'mpi4py'
    ]
    )
