def bartlett(args):
    '''
    Modified version of scipy stat's bartlett function to accept a list of arrays. Modification: turn args into a list
    
    Source code: https://github.com/scipy/scipy/blob/v1.5.3/scipy/stats/morestats.py#L2177-L2273
    '''
    import numpy as np
    from collections import namedtuple
    import scipy.stats as stats
    
    # Handle empty input and input that is not 1d
    for a in args:
        if np.asanyarray(a).size == 0:
            return BartlettResult(np.nan, np.nan)
        if np.asanyarray(a).ndim > 1:
            raise ValueError('Samples must be one-dimensional.')

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = np.zeros(k)
    ssq = np.zeros(k, 'd')
    for j in range(k):
        Ni[j] = len(args[j])
        ssq[j] = np.var(args[j], ddof=1)
    Ntot = np.sum(Ni, axis=0)
    spsq = np.sum((Ni - 1)*ssq, axis=0) / (1.0*(Ntot - k))
    numer = (Ntot*1.0 - k) * np.log(spsq) - np.sum((Ni - 1.0)*np.log(ssq), axis=0)
    denom = 1.0 + 1.0/(3*(k - 1)) * ((np.sum(1.0/(Ni - 1.0), axis=0)) -
                                     1.0/(Ntot - k))
    T = numer / denom
    pval = stats.distributions.chi2.sf(T, k - 1)  # 1 - cdf
    
    BartlettResult = namedtuple('BartlettResult', ('statistic', 'pvalue'))
    
    return BartlettResult(T, pval)