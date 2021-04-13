from setuptools import setup
import sys

msg="""
********************************************************************
Since the perceptilabs package now includes GPU support, this
package has been discontinued.

Please install the perceptilabs package instead of perceptilabs-gpu.
********************************************************************
"""
if not 'sdist' in sys.argv:
    print(msg)
    sys.exit(1)


setup(name = "perceptilabs-gpu", version="0.11.13")
