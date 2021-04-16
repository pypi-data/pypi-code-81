# This library will be used for making charts easier
# for system performance engineers
#
# To update the package on PyPI:
# 1. Update version number in setup.py then go to Tools > Run Setup.py task
# 2. Type sdist. Enter.
# 3. Hit OK (no command-line options)
# 4. Make sure Twine is installed
#   a. File > Settings > Project > Project Interpreter > add Twine
# 5. Open terminal (Alt+F12)
# 6. Run "twine upload dist/*"
# 7. Enter username and password for PyPI. Done!
# NOTE: these instructions came from here:
# https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/
#
# To install the package. Do this from the terminal:
# python3 -m pip install "hallred-chart"

def test():
    print('this is a placeholder')
