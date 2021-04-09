"""Dimentional reduction algorithms
"""
import sklearn.manifold as sm
import umap


class MDSManifoldFactory:
    """A Multidimensional Scaling Manifold factory

    Parameters
    ----------
    random_state : int, RandomState instance, default=None
        Determines the random number generator used to initialize the centers.
        Pass an int for reproducible results across multiple function calls.

    See Also
    --------
    sklearn.manifold.MDS
    """

    def __init__(self, random_state=None):
        self.random_state = random_state

    def make(self):
        """Make the MDS manifold

        Returns
        -------
        sklearn.manifold.MDS
            return the MDS manifold object

        See Also
        --------
        sklearn.manifold.MDS
        """
        return sm.MDS(dissimilarity='precomputed', n_jobs=-1,
                      random_state=self.random_state)


class UMAPManifoldFactory:
    """A UMAP Manifold factory

    Parameters
    ----------
    random_state : int, RandomState instance, default=None
        Determines the random number generator used to initialize the centers.
        Pass an int for reproducible results across multiple function calls.

    See Also
    --------
    umap.UMAP
    """

    def __init__(self, random_state=None):
        self.random_state = random_state

    def make(self):
        """Make the UMAP manifold

        Returns
        -------
        umap.UMAP
            return the UMAP manifold object

        See Also
        --------
        umap.UMAP
        """
        return umap.UMAP(random_state=self.random_state)
