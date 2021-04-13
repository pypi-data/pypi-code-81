from setuptools import setup, find_packages

VERSION = '1.4.9'
DESCRIPTION = 'Athena Utility'
LONG_DESCRIPTION = 'AWS Athena client based on PyAthena'

install_requirements = [
    'pandas',
    'requests',
    'IPython'
]

# Setting up
setup(
    name="athenautility",
    version=VERSION,
    author="KnowledgeLens",
    author_email="karthik.madhamanchi@knowledgelens.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_requirements,
    python_requires=">=3.6",
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: SQL',
        'Topic :: Database',        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

