
from distutils.core import setup
setup(
  name = 'StructuredGraphLearning',
  packages = ['StructuredGraphLearning'],
  version = '0.0.1',
  license='MIT',
  description = 'spectralGraphTopology provides estimators to learn k-component, bipartite, and k-component bipartite graphs from data by imposing spectral constraints on the eigenvalues and eigenvectors of the Laplacian and adjacency matrices. Those estimators leverage spectral properties of the graphical models as a prior information which turn out to play key roles in unsupervised machine learning tasks such as clustering.',   # Give a short description about your library
  author = 'Aditya Bansal',
  author_email = 'aditya510@gmail.com',
  url = 'https://github.com/aditya510',
  download_url = 'https://github.com/Aditya510/StructuredGraphLearning/archive/refs/tags/v0.0.1.tar.gz',
  keywords = ['Graph', 'Learning', 'Spectral'],
  install_requires=[
          'numpy',
          'networkx',
          'scikit-learn',
          'matplotlib',
          'quadprog'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)