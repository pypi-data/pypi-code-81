from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt') as file:
        content = file.read()
        req = content.split('\n')
    return req


setup(
    name='virusdata',
    version='1.0',
    description='Get Details about COVID Cases',
    url='https://github.com/GNVageesh/covidata',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable'
    ],
    author='GN Vageesh',
    author_email='vageeshgn2005@gmail.com',
    license='MIT',
    keywords=['python', 'python3', 'virus',
              'corona', 'COVID', 'covid', 'COVID19', 'pandemic', 'cli'],
    download_url='https://github.com/GNVageesh/gnv',
    include_package_data=True,
    install_requires=requirements(),
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['rq=src.main:display_data']
    )
)
