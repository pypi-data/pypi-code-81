# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['philsol']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'scipy>=1.3,<2.0']

setup_kwargs = {
    'name': 'philsol',
    'version': '0.25',
    'description': 'A fully vectorial finite difference waveguide mode solver. Based on the algorithm of Zhu and Brown',
    'long_description': "# philsol\n## Modes for the Masses (Massless?)\nFed up with relying on expensive proprietary software for your electromagnetic waveguide research?  philsol might just be the package for you. In a world where high performance hardware is cheaper than specialist software, philsol throws elegence and sophistication out of the window and replaces it with brute force. \n\nThis is a fully vectorial finite difference waveguide mode solver and a direct Python implimentation of the algorithm found in the paper: \n['Full-vectorial finite-difference analysis of microstructured optical fibres', by Zhu and Brown.](https://doi.org/10.1364/OE.10.000853)\n\nWarning: I haven't thoroughly tested so be wary and check the results are sensible...\n\nNew Warning: Original paper by Zhu and Brown is in gaussian not S. I. units. \nTo correct use conversion table [here](https://en.wikipedia.org/wiki/Gaussian_units).\n\n## Installation\n- Install using pip with command 'pip install philsol'\n- If you can't be bothered, the important part is the function eigenbuild in core.py. \n\n## Examples\n- Commented example projects can be found in the *examples* directory.\n- To run the examples, first install philsol to your Python environment (see above)\n\n## Features\n### Solver\n- Solves vector Maxwell(Helmholtz) equations in 2D for arbitary refractive index profile.\n- Return x and y componants of electric field.\n- philsol can handle anisotropic refractive indices with diagonal tensor.\n- Currently hard coded with conductive boundary.\n- Choice of solving routines: the default scipy.sparse solver or Slepc (slepc4py and petsc4py) this libraries can be fiddly to set up but are very heavily featured including some limited GPU support.  \n- Extra field componants Ez, Hx, Hy, Hz can be calculated from construct module\n- Periodic boundary conditions \n\n### Geometry building\n- The quickest way of importing geometry is with a bitmap image \n- See *examples/example_image.py* for an example in loading .bpm images\n- See *examples/example_build.py* for an example in building geometry using PIL/Pillow\n\n## To do \n- More intelligent geometry aproximation (e.g pixel interpolation on curved boundaries)\n- More boundry condition options Bloch, PML...\n- GPU eigensolving\n\n\n",
    'author': 'Phil Main',
    'author_email': 'philmain28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/philmain28/philsol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
