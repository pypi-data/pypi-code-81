# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covsirphy',
 'covsirphy.analysis',
 'covsirphy.cleaning',
 'covsirphy.ode',
 'covsirphy.phase',
 'covsirphy.regression',
 'covsirphy.simulation',
 'covsirphy.trend',
 'covsirphy.util',
 'covsirphy.visualization',
 'covsirphy.worldwide']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'better-exceptions>=0.3.2,<0.4.0',
 'country-converter>=0.7.1,<0.8.0',
 'covid19dh>=2.0.3,<3.0.0',
 'dask[dataframe]>=2020.12.0,<2021.0.0',
 'descartes>=1.1.0,<2.0.0',
 'fsspec[http]>=0.8.5,<0.9.0',
 'geopandas>=0.9.0,<0.10.0',
 'japanmap>=0.0.21,<0.0.25',
 'mapclassify>=2.4.2,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'optuna>=2.3.0,<3.0.0',
 'pandas>=1.1.5,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'ruptures>=1.1.1,<2.0.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tabulate>=0.8.7,<0.9.0',
 'wbdata>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'covsirphy',
    'version': '2.19.1',
    'description': 'COVID-19 data analysis with phase-dependent SIR-derived ODE models',
    'long_description': '| |PyPI version| |Downloads| |PyPI - Python Version| |Build Status|\n| |GitHub license| |Maintainability| |Test Coverage| |Open Source\n  Helpers|\n\nCovsirPhy introduction\n======================\n\n`Documentation <https://lisphilar.github.io/covid19-sir/index.html>`__\n\\|\n`Installation <https://lisphilar.github.io/covid19-sir/INSTALLATION.html>`__\n\\| `Quickest\nusage <https://lisphilar.github.io/covid19-sir/usage_quickest.html>`__\n\\| `API\nreference <https://lisphilar.github.io/covid19-sir/covsirphy.html>`__ \\|\n`GitHub <https://github.com/lisphilar/covid19-sir>`__ \\| `Qiita\n(Japanese) <https://qiita.com/tags/covsirphy>`__\n\nCovsirPhy is a Python library for COVID-19 (Coronavirus disease 2019)\ndata analysis with phase-dependent SIR-derived ODE models. We can\ndownload datasets and analyse them easily. Scenario analysis with\nCovsirPhy enables us to make data-informed decisions.\n\nFunctionalities\n---------------\n\n-  `Data preparation and data\n   visualization <https://lisphilar.github.io/covid19-sir/usage_dataset.html>`__\n-  `Phase setting with S-R Trend\n   analysis <https://lisphilar.github.io/covid19-sir/usage_phases.html>`__\n-  `Numerical simulation of ODE\n   models <https://lisphilar.github.io/covid19-sir/usage_theoretical.html>`__:\n   SIR, SIR-D and SIR-F model\n-  `Phase-dependent parameter estimation of ODE\n   models <https://lisphilar.github.io/covid19-sir/usage_quickest.html>`__\n-  `Scenario\n   analysis <https://lisphilar.github.io/covid19-sir/usage_quick.html>`__:\n   Simulate the number of cases with user-defined parameter values\n-  `Find the relationship of government response and parameter\n   values <https://lisphilar.github.io/covid19-sir/usage_policy.html>`__\n\nInspiration\n-----------\n\n-  Monitor the spread of COVID-19\n-  Keep track parameter values/reproduction number in each\n   country/province\n-  Find the relationship of reproductive number and measures taken by\n   each country\n\nIf you have ideas or need new functionalities, please join this project.\nAny suggestions with `Github\nIssues <https://github.com/lisphilar/covid19-sir/issues/new/choose>`__\nare always welcomed. Questions are also great. Please read `Guideline of\ncontribution <https://lisphilar.github.io/covid19-sir/CONTRIBUTING.html>`__\nin advance.\n\nInstallation\n------------\n\nThe latest stable version of CovsirPhy is available at `PyPI (The Python\nPackage Index): covsirphy <https://pypi.org/project/covsirphy/>`__ and\nsupports Python 3.7 or newer versions. Details are explained in\n`Documentation:\nInstallation <https://lisphilar.github.io/covid19-sir/INSTALLATION.html>`__.\n\n.. code:: bash\n\n    pip install --upgrade covsirphy\n\nUsage\n-----\n\nQuickest tour of CovsirPhy is here. The following codes analyze the\nrecords in Japan, but we can change the country name when creating\n``Scenario`` class instance for your own analysis.\n\n.. code:: python\n\n    import covsirphy as cs\n    # Download and update datasets\n    data_loader = cs.DataLoader("input")\n    jhu_data = data_loader.jhu()\n    population_data = data_loader.population()\n    # Check records\n    snl = cs.Scenario(country="Japan")\n    snl.register(jhu_data, population_data)\n    snl.records()\n    # S-R trend analysis\n    snl.trend().summary()\n    # Parameter estimation of SIR-F model\n    snl.estimate(cs.SIRF)\n    # History of reproduction number\n    _ = snl.history(target="Rt")\n    # History of parameters\n    _ = snl.history_rate()\n    _ = snl.history(target="rho")\n    # Simulation for 30 days\n    snl.add(days=30)\n    _ = snl.simulate()\n\nFurther information:\n\n-  `CovsirPhy\n   documentation <https://lisphilar.github.io/covid19-sir/index.html>`__\n-  `Kaggle: COVID-19 data with SIR\n   model <https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model>`__\n\nRelease notes\n-------------\n\nRelease notes are\n`here <https://github.com/lisphilar/covid19-sir/releases>`__. Titles &\nlinks of issues are listed with acknowledgement.\n\nWe can see the release plan for the next stable version in `milestone\npage of the GitHub\nrepository <https://github.com/lisphilar/covid19-sir/milestones>`__. If\nyou find a highly urgent matter, please let us know via `issue\npage <https://github.com/lisphilar/covid19-sir/issues>`__.\n\nSupport\n-------\n\nPlease support this project as a developer (or a backer). |Become a\nbacker|\n\nDevelopers\n----------\n\nCovsirPhy library is developed by a community of volunteers. Please see\nthe full list\n`here <https://github.com/lisphilar/covid19-sir/graphs/contributors>`__.\n\nThis project started in Kaggle platform. Lisphilar published `Kaggle\nNotebook: COVID-19 data with SIR\nmodel <https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model>`__\non 12Feb2020 and developed it, discussing with Kaggle community. On\n07May2020, "covid19-sir" repository was created. On 10May2020,\n``covsirphy`` version 1.0.0 was published in GitHub. First release in\nPyPI (version 2.3.0) was on 28Jun2020.\n\nLicense: Apache License 2.0\n---------------------------\n\nPlease refer to\n`LICENSE <https://github.com/lisphilar/covid19-sir/blob/master/LICENSE>`__\nfile.\n\nCitation\n--------\n\nWe have no original papers the author and contributors wrote, but please\ncite this library as follows with version number\n(``import covsirphy as cs; cs.__version__``).\n\nCovsirPhy Development Team (2020-2021), CovsirPhy version [version\nnumber]: Python library for COVID-19 analysis with phase-dependent\nSIR-derived ODE models, https://github.com/lisphilar/covid19-sir\n\nIf you want to use SIR-F model, S-R trend analysis, phase-dependent\napproach to SIR-derived models, and other scientific method performed\nwith CovsirPhy, please cite the next Kaggle notebook.\n\nHirokazu Takaya (2020-2021), Kaggle Notebook, COVID-19 data with SIR\nmodel, https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model\n\nWe can check the citation with the following script (version >= 2.18.0).\n\n.. code:: python\n\n    import covsirphy as cs\n    cs.__citation__\n\n.. |PyPI version| image:: https://badge.fury.io/py/covsirphy.svg\n   :target: https://badge.fury.io/py/covsirphy\n.. |Downloads| image:: https://pepy.tech/badge/covsirphy\n   :target: https://pepy.tech/project/covsirphy\n.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/covsirphy\n   :target: https://badge.fury.io/py/covsirphy\n.. |Build Status| image:: https://semaphoreci.com/api/v1/lisphilar/covid19-sir/branches/master/shields_badge.svg\n   :target: https://semaphoreci.com/lisphilar/covid19-sir\n.. |GitHub license| image:: https://img.shields.io/github/license/lisphilar/covid19-sir\n   :target: https://github.com/lisphilar/covid19-sir/blob/master/LICENSE\n.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/eb97eaf9804f436062b9/maintainability\n   :target: https://codeclimate.com/github/lisphilar/covid19-sir/maintainability\n.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/eb97eaf9804f436062b9/test_coverage\n   :target: https://codeclimate.com/github/lisphilar/covid19-sir/test_coverage\n.. |Open Source Helpers| image:: https://www.codetriage.com/lisphilar/covid19-sir/badges/users.svg\n   :target: https://www.codetriage.com/lisphilar/covid19-sir\n.. |Become a backer| image:: https://opencollective.com/covsirphy/tiers/backer.svg?avatarHeight=36&width=600\n   :target: https://opencollective.com/covsirphy\n',
    'author': 'Hirokazu Takaya',
    'author_email': 'lisphilar@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lisphilar/covid19-sir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
