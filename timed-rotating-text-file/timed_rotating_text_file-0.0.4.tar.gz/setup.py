import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timed_rotating_text_file",
    version="0.0.4",
    description="A ZERO dependency rotating text file handler which rotates when YOU want it to, like TimedRotatingFileHandler provided by Python's logging module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        'Natural Language :: English',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "Intended Audience :: Developers",
    ],
    keywords='custom rotating file handler textfile logger',
    author='bahamut45',
    author_email='njoubert45@gmail.com',
    url='https://github.com/bahamut45/timed-rotating-text-file',
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
