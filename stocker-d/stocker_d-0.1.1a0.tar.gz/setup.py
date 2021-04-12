from setuptools import setup

with open('README.md') as f:
    readme = f.read()

requires = [
    "Flask==1.1.2",
    "yfinance==0.1.59",
    "pandas==1.2.3",
    "numpy==1.20.2"
]

setup(
    name='stocker_d',
    version='0.1.1a',
    packages=['stocker_d'],
    description="Stocker D",
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='david.woodruff@coxautoinc.com',
    install_requires=requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='stocker'
)
