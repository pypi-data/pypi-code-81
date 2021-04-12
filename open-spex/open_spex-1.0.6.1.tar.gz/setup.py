import setuptools
import time

ver = "1.0.6.1"

# Create version file for build date
# -------------------------------------
t = time.gmtime()
f = f"build_date   = '{time.strftime('%Y-%m-%d %H:%M', t)}'\n"
f += f"version  = '{ver}'\n"

file = open('open_spex/version.py', 'w')
file.write(f)
file.close()

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()
    requirements = [r.rstrip() for r in requirements]
setuptools.setup(
    name="open_spex",
    version=f"{ver}",
    author="Anders Ringbom",
    author_email="anders.ringbom@foi.se",
    description="Radioxenon beta-gamma analysis tool",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
         'console_scripts':['openSpex = open_spex:main']
    },
    python_requires='>=3.6.9',
)