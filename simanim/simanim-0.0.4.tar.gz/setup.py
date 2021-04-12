import io
import re
import setuptools
import sys

import shutil 
  

REQUIREMENTS_FLAG = True

with open("README.md", "rt", encoding='utf8') as fh:
    long_description = fh.read()


if "--pyodide" in sys.argv:
    R_FLAG  = False 
    shutil.copyfile('MANIFEST-PYODIDE.in','MANIFEST.in')
    sys.argv.remove("--pyodide")
else:
    R_FLAG  = True 
    shutil.copyfile('MANIFEST-QT.in','MANIFEST.in')


install_requires= []
if R_FLAG:
    with open('requirements-qt.txt', 'rt', encoding='utf8') as fh:
        for l in fh:
            install_requires.append(l.strip())
else:
    with open('requirements-pyodide.txt', 'rt', encoding='utf8') as fh:
        for l in fh:
            install_requires.append(l.strip())


with io.open('simanim/__init__.py', 'rt', encoding='utf8') as f:
    src = f.read()
m = re.search(r'\_\_version\_\_\s*=\s*\"([^"]*)\"', src)
version = m.group(1)

setuptools.setup(
    python_requires=">=3.6",
    name="simanim",
    version=version,
    author="Fondacija Petlja",
    author_email="team@petlja.org",
    description="Python framework for simple simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Petlja/simanim",
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    packages=["simanim"],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        
    ]
)
