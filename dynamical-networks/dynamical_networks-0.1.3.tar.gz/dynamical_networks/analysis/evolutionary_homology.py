"""
Evolutionary homology calculation for dynamical networks.
=======================================================================

This functions calculates the evelutionary homology of a dynamical networks adjacency matrix.
"""

def EveHom(A):
    """This function takes the time varying adjacency matrix and returns the evolutionary homology.

    Args:
       A (array): Time varying adjacency matrix.

    Kwargs:
       plotting (bool): Plotting for user interpretation. defaut is False.

    Returns:
       (array): Statistic array over time.

    """

    import numpy as np
    
    #-------------------Run input data tests--------------------------
    if type(A) != np.ndarray:
        # the data type should be a numpy array of 2d arrays
        raise TypeError("Input must be numpy array.")
    if type(A[0][0]) != np.ndarray:
        # the size of each adjacency matrix should not be empty
        raise TypeError("Input must be numpy array of 2D (nxn) arrays. i.e. Nx(nxn) array.")
        
    statistic = []
    for a in A:
        stat = np.nanmax(a)
        statistic.append(stat)
    
    return np.array(statistic)


# In[ ]:


if __name__ == '__main__':
    
    from dynamical_networks.analysis.evolutionary_homology import EveHom
    from dynamical_networks.simulate.PG_network import PG_network
    A = PG_network()
    S = EveHom(A)



