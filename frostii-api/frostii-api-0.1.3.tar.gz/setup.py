from setuptools import setup
import re

with open('frostiiapi/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md", "r") as f:
	long_desc = f.read()

setup(
name="frostii-api",
author="Alex Hutz",
author_email="frostiiweeb@gmail.com",
keywords=["image", "image api"],
version=version,
packages=['frostiiapi'],
license='MIT',
long_description=long_desc,
long_description_content_type="text/markdown",
description="An API wrapper for frostii api.",
install_requires=['aiohttp>=3.7.3'],
python_requires='>=3.5.3',
classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)