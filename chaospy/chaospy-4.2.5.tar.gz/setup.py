# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaospy',
 'chaospy.descriptives',
 'chaospy.descriptives.correlation',
 'chaospy.descriptives.sensitivity',
 'chaospy.distributions',
 'chaospy.distributions.baseclass',
 'chaospy.distributions.collection',
 'chaospy.distributions.copulas',
 'chaospy.distributions.kernel',
 'chaospy.distributions.operators',
 'chaospy.distributions.sampler',
 'chaospy.distributions.sampler.sequences',
 'chaospy.external',
 'chaospy.orthogonal',
 'chaospy.quadrature',
 'chaospy.quadrature.genz_keister',
 'chaospy.recurrence']

package_data = \
{'': ['*']}

install_requires = \
['numpoly', 'numpy', 'scipy']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['functools32']}

setup_kwargs = {
    'name': 'chaospy',
    'version': '4.2.5',
    'description': 'Numerical tool for perfroming uncertainty quantification',
    'long_description': '.. image:: https://github.com/jonathf/chaospy/raw/master/docs/_static/chaospy_logo.svg\n   :height: 200 px\n   :width: 200 px\n   :align: center\n\n|circleci| |codecov| |readthedocs| |downloads| |pypi| |binder|\n\n.. |circleci| image:: https://img.shields.io/circleci/build/github/jonathf/chaospy/master\n    :target: https://circleci.com/gh/jonathf/chaospy/tree/master\n.. |codecov| image:: https://img.shields.io/codecov/c/github/jonathf/chaospy\n    :target: https://codecov.io/gh/jonathf/chaospy\n.. |readthedocs| image:: https://img.shields.io/readthedocs/chaospy\n    :target: https://chaospy.readthedocs.io/en/master/?badge=master\n.. |downloads| image:: https://img.shields.io/pypi/dm/chaospy\n    :target: https://pypistats.org/packages/chaospy\n.. |pypi| image:: https://img.shields.io/pypi/v/chaospy\n    :target: https://pypi.org/project/chaospy\n.. |binder| image:: https://mybinder.org/badge_logo.svg\n    :target: https://mybinder.org/v2/gh/jonathf/chaospy/master?filepath=docs%2Ftutorials\n\n* `Documentation <https://chaospy.readthedocs.io/en/master>`_\n* `Interactive tutorials with Binder <https://mybinder.org/v2/gh/jonathf/chaospy/master?filepath=docs%2Ftutorials>`_\n* `Code of conduct <https://github.com/jonathf/chaospy/blob/master/CODE_OF_CONDUCT.md>`_\n* `Contribution guideline <https://github.com/jonathf/chaospy/blob/master/CONTRIBUTING.md>`_\n* `Changelog <https://github.com/jonathf/chaospy/blob/master/CHANGELOG.md>`_\n* `License <https://github.com/jonathf/chaospy/blob/master/LICENCE.txt>`_\n\nChaospy is a numerical toolbox for performing uncertainty quantification using\npolynomial chaos expansions, advanced Monte Carlo methods implemented in\nPython. It also include a full suite of tools for doing low-discrepancy\nsampling, quadrature creation, polynomial manipulations, and a lot more.\n\nThe philosophy behind ``chaospy`` is not to be a single tool that solves every\nuncertainty quantification problem, but instead be a specific tools to aid to\nlet the user solve problems themselves. This includes both well established\nproblems, but also to be a foundry for experimenting with new problems, that\nare not so well established. To do this, emphasis is put on the following:\n\n* Focus on an easy to use interface that embraces the `pythonic code style\n  <https://docs.python-guide.org/writing/style/>`_.\n* Make sure the code is "composable", such a way that changing one part of the\n  code with something user defined should be easy and encouraged.\n* Try to support a broad width of the various methods for doing uncertainty\n  quantification where that makes sense to involve ``chaospy``.\n* Make sure that ``chaospy`` plays nice with a large set of of other other\n  similar projects. This includes `numpy <https://numpy.org/>`_, `scipy\n  <https://scipy.org/>`_, `scikit-learn <https://scikit-learn.org>`_,\n  `statsmodels <https://statsmodels.org/>`_, `openturns\n  <https://openturns.org/>`_, and `gstools <https://geostat-framework.org/>`_\n  to mention a few.\n* Contribute all code to the community open source.\n\nInstallation\n============\n\nInstallation should be straight forward from `pip <https://pypi.org/>`_:\n\n.. code-block:: bash\n\n    pip install chaospy\n\nOr if `Conda <https://conda.io/>`_ is more to your liking:\n\n.. code-block:: bash\n\n    conda install -c conda-forge chaospy\n\nThen go over to the\n`tutorial collection <https://chaospy.readthedocs.io/en/master/tutorials>`_\nto see how to use the toolbox.\n\nDevelopment\n===========\n\nChaospy uses `poetry`_ to manage its development installation. Assuming\n`poetry`_ installed on your system, installing ``chaospy`` for development can\nbe done from the repository root with the command::\n\n    poetry install\n\nThis will install all required dependencies and chaospy into a virtual\nenvironment. If you are not already managing your own virtual environment, you\ncan use poetry to activate and deactivate with::\n\n    poetry shell\n    exit\n\n.. _poetry: https://poetry.eustace.io/\n\nTesting\n-------\n\nTo ensure that the code run on your local system, run the following:\n\n.. code-block:: bash\n\n    poetry run pytest --nbval-lax --doctest-modules \\\n        chaospy/ tests/ docs/*/*.{rst,ipynb}\n\nDocumentation\n-------------\n\nThe documentation build assumes that ``pandoc`` is installed on your\nsystem and available in your path.\n\nTo build documentation locally on your system, use ``make`` from the ``docs/``\nfolder:\n\n.. code-block:: bash\n\n    cd docs/\n    make html\n\nRun ``make`` without argument to get a list of build targets.\nThe HTML target stores output to the folder ``doc/.build/html``.\n',
    'author': 'Jonathan Feinberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonathf/chaospy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
