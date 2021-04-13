from setuptools import setup
setup(
    name="rattools",
    version="0.4.1",
    description="Este es un paquete de ejemplo",
    author="Ldog",
    author_email="domgutluis@gmail.com",
    url="",
    packages=['rattools'],
    install_requires=[            # I get to this in a second
          'finviz',
          'pandas',
          'sklearn',
          'matplotlib']
)