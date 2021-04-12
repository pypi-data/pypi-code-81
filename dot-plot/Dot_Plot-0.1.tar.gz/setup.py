from setuptools import setup

setup(
    name='Dot_Plot',
    version='0.1',
    description="Dot plot is a tool for creating svg images of chord and scale diagrams for fretboard instruments like guitar, bass, ukulele, viola da gamba.  and / or scale diagrams including guitar, bass, ukulele, viola da gamba etc.",
    author="Nicola A. Cappellini",
    author_email='nicola.cappellini@gmail.com',
    url='',
    license='Private, non-commercial, no distribution',
    packages=['Dot_Plot', 'Dot_Plot.library'],
    install_requires=['drawSvg'],
    python_requires='>=3',
)
