# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybricksdev', 'pybricksdev.cli', 'pybricksdev.resources']

package_data = \
{'': ['*']}

install_requires = \
['aioserial>=1.3.0,<2.0.0',
 'argcomplete>=1.11.1,<2.0.0',
 'asyncssh>=2.2.1,<3.0.0',
 'bleak>=0.11.0,<0.12.0',
 'mpy-cross==1.12',
 'pyusb>=1.0.2,<2.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'validators>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['pybricksdev = pybricksdev.cli:main']}

setup_kwargs = {
    'name': 'pybricksdev',
    'version': '1.0.0a1',
    'description': 'Pybricks developer tools',
    'long_description': 'Pybricks tools & interface library\n-----------------------------------\n\nThis is a package with tools for Pybricks developers. For regular users we\nrecommend the `Pybricks Code`_ web IDE.\n\nThis package contains both command line tools and a library to call equivalent\noperations from within a Python script.\n\nInstallation\n-----------------\n\nRequirements:\n\n- pyenv: Used to locally install another version of Python without touching\n  your system Python.\n- poetry: Used to download and install all Python dependencies with the right\n  versions.\n\nInstallation steps:\n\n::\n\n    git clone https://github.com/pybricks/pybricksdev.git\n    cd pybricksdev\n    pyenv install 3.8.2 # You can skip this if you already have Python >=3.8.2\n    poetry install\n\nLinux USB:\n\nOn Linux, ``udev`` rules are needed to allow access via USB. The ``pybricksdev``\ncommand line tool contains a function to generate the required rules. Run the\nfollowing::\n\n    poetry run pybricksdev udev | sudo tee /etc/udev/rules.d/99-pybricksdev.rules\n\n\nFlashing Pybricks MicroPython firmware\n--------------------------------------------------------------------------\n\nMake sure the hub is off. Press and keep holding the hub button, and run::\n\n    poetry run pybricksdev flash ../pybricks-micropython/bricks/technichub/build/firmware.zip\n\nReplace the example path with the path to the firmware archive. Decrease the\ndelay ``d`` between data packages for faster transfer. Increase the delay if it\nfails.\n\nYou may release the button once the progress bar first appears. \n\nThe SPIKE Prime Hub and MINDSTORMS Robot Inventor Hub do not have a Bluetooth\nbootloader. It is recommended to `install Pybricks using a Python script`_ that\nruns on the hub. You can also flash the firmware manually using `DFU`_.\n\nRunning Pybricks MicroPython programs\n---------------------------------------\n\nThis compiles a MicroPython script and sends it to a hub with Pybricks\nfirmware.\n\n::\n\n    poetry run pybricksdev run --help\n\n    #\n    # ble connection examples:\n    #\n\n    # Run a one-liner on a Pybricks hub\n    poetry run pybricksdev run ble \'Pybricks Hub\' \'print("Hello!"); print("world!");\'\n\n    # Run script on the first device we find called Pybricks hub\n    poetry run pybricksdev run ble \'Pybricks Hub\' demo/shortdemo.py\n\n    # Run script on 90:84:2B:4A:2B:75, skipping search\n    poetry run pybricksdev run ble 90:84:2B:4A:2B:75 demo/shortdemo.py\n\n    #\n    # Other connection examples:\n    #\n\n    # Run script on ev3dev at 192.168.0.102\n    poetry run pybricksdev run ssh 192.168.0.102 demo/shortdemo.py\n\n    # Run script on primehub at\n    poetry run pybricksdev run usb "Pybricks Hub" demo/shortdemo.py\n\nCompiling Pybricks MicroPython programs without running\n--------------------------------------------------------\n\nThis can be used to compile programs. Instead of also running them as above,\nit just prints the output on the screen instead.\n\n::\n\n    poetry run pybricksdev compile demo/shortdemo.py\n\n    poetry run pybricksdev compile "print(\'Hello!\'); print(\'world!\');"\n\n\nThis is mainly intended for developers who want to quickly inspect the\ncontents of the ``.mpy`` file. To get the actual file, just use ``mpy-cross``\ndirectly. We have used this tool in the past to test bare minimum MicroPython\nports that have neither a builtin compiler or any form of I/O yet. You can\npaste the generated ``const uint8_t script[]`` directly ito your C code.\n\n.. _Pybricks Code: https://www.code.pybricks.com/\n.. _DFU: README_dfu.rst\n.. _install Pybricks using a Python script: https://github.com/pybricks/support/issues/167\n',
    'author': 'The Pybricks Authors',
    'author_email': 'dev@pybricks.com',
    'maintainer': 'Laurens Valk',
    'maintainer_email': 'laurens@pybricks.com',
    'url': 'https://pybricks.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
