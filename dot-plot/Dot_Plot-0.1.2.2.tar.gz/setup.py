from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='Dot_Plot',
    version='0.1.2.2',
    description="Dot plot is a tool for creating svg images of chord and scale diagrams for fretboard instruments like guitar, bass, ukulele, viola da gamba etc",
    long_description=readme(),
    long_description_content_type='text/x-rst',
    author="Nicola A. Cappellini",
    author_email='nicola.cappellini@gmail.com',
    url='',
    license='Private, non-commercial, no distribution',
    packages=['Dot_Plot', 'Dot_Plot.library'],
    install_requires=['drawSvg'],
    python_requires='>=3',
)
