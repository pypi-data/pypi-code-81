from setuptools import setup

setup(
    name='crypy',
    version='0.1.1',
    packages=['crypy', 'crypy.aes', 'crypy.rsa', 'crypy.hash', 'crypy.utils', 'crypy.random', 'crypy.classic'],
    license='MIT',
    url='https://github.com/petitnau/crypy',
    download_url='https://github.com/petitnau/crypy/archive/refs/tags/v0.1.1-alpha.tar.gz',
    author='petitnau, piier, geladen',
    author_email='roberto.pettinau99@gmail.com, erik.piersante@gmail.com, cuncuemanuele@outlook.it',
    description='',
    install_requires=[
        'sympy',
        'pycryptodome',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ]
)

