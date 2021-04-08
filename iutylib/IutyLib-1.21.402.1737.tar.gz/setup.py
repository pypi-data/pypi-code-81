from setuptools import setup

version = "1.0"
try:
    from IutyLib.commonutil.config import Config
    config = Config("./Config.conf")
    ver = config.get("Version","ver")
    subver = config.get("Version","subver")
    version= "{}.{}".format(ver,subver)
except ImportError:
    print("Import Error")

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
    packages=packages,
    install_requires = install_requires
)