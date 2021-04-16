from setuptools import setup

setup(
    name='glowseeds',
    version='0.1.2',
    packages=['glowseeds'],
    url='https://github.com/TeamMacLean/glowseeds',
    license='LICENSE.txt',
    author='Dan MacLean',
    author_email='dan.maclean@tsl.ac.uk',
    description='Counting glowing seeds',
    python_requires='>=3.7',
    install_requires=[
        "scikit-image>=0.18.1",
        "pandas"
    ],
)