import setuptools
from setuptools.command.build_ext import build_ext as hookBuild_ext
from setuptools import setup, Extension

from subprocess import check_call, check_output
import os
from sys import platform

try:
    from stdeb.command.sdist_dsc import sdist_dsc
    from stdeb.command.bdist_deb import bdist_deb
except ImportError:
    sdist_dsc = None
    bdist_deb = None

try:
    os.environ['SOURCE_DATE_EPOCH'] = (
    check_output("git log -1 --pretty=%ct", shell=True).decode().strip())
except:
    os.environ['SOURCE_DATE_EPOCH'] = "1617737253"

if os.path.exists('vula_libnss/__version__.py'):
    with open("vula_libnss/__version__.py", "r") as obj:
        version = str(obj.readline().strip())
        version = version.split('"')[1]

if os.path.exists('requirements.txt'):
    with open("requirements.txt", "r") as obj:
        requirements = obj.read().splitlines()
else:
    # this makes stdeb work
    requirements = []

with open("README.md", "r") as obj:
    long_description = obj.read()

linux_data_files = [
    ("/lib/", ["nss-altfiles/libnss_vula.so.2"]),
]

our_data_files = linux_data_files

class print_version(hookBuild_ext):
    def run(self):
        print(version)

def buildNSS():
    if platform.startswith("linux"):
        check_call(("cd nss-altfiles && make distclean"), shell=True)
        check_call(
            (
                "cd nss-altfiles && ./configure "
                + "--with-types=hosts "
                + "--with-module-name='vula' "
                + "--datadir=/var/lib/vula-organize/",
            ),
            shell=True,
        )
        check_call(("cd nss-altfiles && make"), shell=True)


class buildHook(hookBuild_ext):
    def build_extensions(self):
        print("Building NSS shared object")
        buildNSS()
        print("Building miminal ext_module object")
        hookBuild_ext.build_extensions(self)

setuptools.setup(
    name="vula_libnss",
    version=version,
    ext_modules = [Extension("vula_libnss", ["dummy.c"], optional=True)],
    author="Vula Authors",
    author_email="git@vula.link",
    description=(
        "nss-altfiles for vula"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://codeberg.org/vula/vula_libnss",
    packages=setuptools.find_packages(),
    keywords="WireGuard, mDNS, encryption, libnss",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    data_files=our_data_files,
    include_package_data=True,
    zip_safe=False,
    tests_require=["pytest"],
    cmdclass=dict(
        build_ext=buildHook,
        bdist_deb=bdist_deb,
        sdist_dsc=sdist_dsc,
        version=print_version,
    ),
)
