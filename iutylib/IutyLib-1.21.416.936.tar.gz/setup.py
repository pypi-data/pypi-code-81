from setuptools import setup

version = '1.21.0416.0936'

author = "Iuty"
author_email = "dfdfggg@126.com"


packages = [
        #"IutyLib",
        "IutyLib.commonutil",
        "IutyLib.coding",
        "IutyLib.database",
        "IutyLib.file",
        "IutyLib.stock",
        "IutyLib.tensor",
        "IutyLib.monitor",
        "IutyLib.notice",
        "IutyLib.framework",
        "IutyLib.encription",
        "IutyLib.show",
        "IutyLib.mutithread",
        "IutyLib.useright",
        "IutyLib.method",
        ]

install_requires = ['pyDes',]

setup(
    name="IutyLib",
    version= version,
    #version = ver,
    author = author,
    author_email = author_email,
    packages=packages,
    install_requires = install_requires
)