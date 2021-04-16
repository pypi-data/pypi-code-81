"""
This module contains all the function which allows to compute hierarchical quantifier value
using a pitch class distribution.
"""
import numpy as np
from hierarchical_quantifier.utils import read_pickle, write_pickle, check_pickle_argument
from multiprocessing import Pool

__NBR_PITCH = 12  # number of pitch class.
from itertools import repeat
import functools


def __check_corpus_count_input(counts: np.ndarray) -> np.ndarray:
    if (type(counts) != np.ndarray):
        raise TypeError('Wrong input types.')

    if counts.shape[2] != __NBR_PITCH:
        raise ValueError('Wrong number of pitch classes')

    if counts.ndim != 3:
        raise ValueError('Wrong number of dimension of the array.')

    if counts.shape[0] < 2:
        raise ValueError('Input is not a corpus.')

    if (counts < 0).any():
        raise ValueError('Corpus contains at least  one negative count')


def __check_scape_input(scape: np.ndarray) -> np.ndarray:
    if (type(scape) != np.ndarray):
        raise TypeError('Wrong input types.')

    if scape.ndim != 2:
        raise ValueError('Wrong number of dimension of the array.')

    if scape.shape[0] != scape.shape[1]:
        raise ValueError('scape array must be equal dimension.')


def get_mi_scape(counts: np.ndarray, set_zero_diagonal: bool = True, pickle=False, force_reset=False) -> np.ndarray:
    """
    Given a sampled pitchscape representation of each piece in a corpus, this function computes the Mutual
    Information value for each pair of time index.

    :param counts: Pitch class distribution of each piece in the corpus. The corpus contains m pieces. The number
    of time bins is n.
    :param set_zero_diagonal: By default is True, set to 0 the Mutual information value for the same time index.
    :type counts: numpy.ndarray (m, n, 12)
    :type set_zero_diagonal: bool
    :return: 2D array of the Mutual information value indexes by time indexes.
    :rtype: numpy.ndarray of shape (n,n)
    """
    if (type(set_zero_diagonal) != bool):
        raise TypeError('Wrong input types.')

    __check_corpus_count_input(counts)

    mutual_info = read_pickle(pickle)
    if not mutual_info is None:
        return mutual_info

    pcd = get_pcd(counts)
    jpcd = get_join_pcd(counts)

    # == Mutual information
    h_pcd = __compute_entropy_pdc(pcd)
    h_jpcd = __compute_entropy_jpdc(jpcd)

    mutual_info = (h_pcd + h_pcd[:, None]) - h_jpcd
    n = mutual_info.shape[0]
    if set_zero_diagonal:
        mutual_info[np.diag_indices(n)] = 0

    write_pickle(force_reset, mutual_info)

    return mutual_info


def get_pcd(counts: np.ndarray) -> np.ndarray:
    """
    Given a sampled pitchscape representation of each piece in a corpus, this function computes the pitch class distribution
    for each time index.

    :param counts: Pitch class distribution of each piece in the corpus. The corpus contains m pieces. The number
    of time bins is n.
    :type counts: numpy.ndarray (m, n, 12)
    :return: Pitch class distribution of a corpus.
    :rtype: numpy.ndarray of shape (n,12)
    """
    __check_corpus_count_input(counts)

    # == Pitch class distribution
    normalize = np.sum(counts, axis=2)[:, :, None]
    count = np.ma.divide(counts, normalize).filled(0)  # normalize
    # add the silence
    count[(np.sum(counts, axis=2) == 0), :] = 1 / __NBR_PITCH

    count = np.sum(count, axis=0)[None]
    norm2 = np.sum(count, axis=2)[:, :, None]

    return np.ma.divide(count, norm2).filled(0)[0]


def get_join_pcd(counts: np.ndarray) -> np.ndarray:
    """
    Given a sampled pitchscape representation of each piece in a corpus, this function computes the join pitch class distribution
    for each pair og time index.

    :param counts: Pitch class distribution of each piece in the corpus. The corpus contains m pieces. The number
    of time bins is n.
    :type counts: numpy.ndarray (m, n, 12)
    :return: Join pitch class distribution of a corpus.
    :rtype: numpy.ndarray of shape (n,n,12)
    """
    __check_corpus_count_input(counts)

    pcd = get_pcd(counts)  # check if it can be given as argument.

    # == Join pitch class distribution
    normalize = np.sum(counts, axis=2)[:, :, None]
    count = np.ma.divide(counts, normalize).filled(0)  # normalize
    # thread the silence
    count[(np.sum(count, axis=2) == 0), :] = 1 / __NBR_PITCH  # silence note

    y = count[:, None, :, None, :] * count[:, :, None, :, None]  # count the occurences

    y = np.sum(y, axis=0)  # aggregate the pieces
    jpcd = np.ma.divide(y, np.sum(y, axis=(2, 3))[:, :, None, None]).filled(0)

    index_time = list(range(0, jpcd.shape[0]))
    jpcd[index_time, index_time, :, :] = 0

    for i in index_time:
        jpcd[i, i, :, :] = np.diag(pcd[i, :])

    return jpcd


def get_pitch_scape(counts: np.ndarray, pickle=False, force_reset=False) -> np.ndarray:
    """
    Given the pitch class distribution(PCD) of a piece, this function return the pitchscape representation of it.

    :param counts: Pitch class distribution of a piece. The number
    of time bins is n.
    :type counts: numpy.nparray of shape (n, 12).
    :return: Return the Pitchscape representation of the piece. It allows to compute the pitch class
    distribution given a time interval. Note that the PDC of negative time interval is set to zero.
    :rtype: numpy.ndarray of shape (n, n, 12).

    """
    if (type(counts) != np.ndarray):
        raise TypeError('Wrong input types.')

    if counts.shape[1] != __NBR_PITCH:
        raise ValueError('Wrong number of pitch classes')

    if counts.ndim != 2:
        raise ValueError('Wrong number of dimension of the array.')

    if (counts < 0).any():
        raise ValueError('Piece contains at least one negative count')

    res = read_pickle(pickle)
    if not res is None:
        return res

    normalize = np.sum(counts, axis=1)[:, None]
    count = np.ma.divide(counts, normalize).filled(0)  # normalize
    # thread the silence
    count[(np.sum(count, axis=1) == 0), :] = 1 / __NBR_PITCH  # silence note

    size = counts.shape[0]

    res = np.zeros((size, size, __NBR_PITCH))
    for i in np.arange(size):
        for j in np.arange(size):
            if j >= i:
                res[i, j, :] = np.sum(count[i:j + 1, :], axis=0)

    # normalize
    norm2 = np.sum(res, axis=2)[:, :, None]
    res = np.ma.divide(res, norm2).filled(0)

    write_pickle(force_reset, res)

    return res


def get_kld_scape(pitch_scape: np.ndarray) -> np.ndarray:
    """
    Given a pitch scape representation of a piece, this function return the Kullback-Leibler
    divergence(KLD) value from the hole piece to any subsection of the piece.

    :param pitch_scape: Pitchscape representation of a piece. The number of time bins of the piece is n.
    :type pitch_scape: numpy.ndarray of shape (n, n, 12).
    :return: Return the KLD value from the hole piece to any subsection of the piece
    :rtype: numpy.ndarray of shape (n, n).
    """
    if (type(pitch_scape) != np.ndarray):
        raise TypeError('Wrong input types.')

    if pitch_scape.ndim != 3:
        raise ValueError('Wrong number of dimension of the array.')

    if pitch_scape.shape[2] != __NBR_PITCH:
        raise ValueError('Wrong number of pitch classes')

    if (pitch_scape < 0).any():
        raise ValueError('pitch scape contains at least one negative count')

    full_piece_prob_dist = pitch_scape[0, -1, :]
    # print(self.__k_l_divergence(full_piece_prob_dist,self.prob_density[0,10,:]
    res = pitch_scape
    map_func = lambda x: __k_l_divergence(full_piece_prob_dist, x)
    res = map_func(res)
    res = np.sum(res, axis=2)

    return res


def __compute_entropy_pdc(prob_density: np.ndarray) -> np.ndarray:
    """
    Given a Pitch class distribution, this function computes the entropy value.

    :param prob_density: The pitch class distribution. The sample size is n.
    :type prob_density: numpy.ndarray of shape (n, 12).
    :return: Entropy value array indexed by time index.
    :rtype: numpy.ndarray of shape (n,).
    """
    ret = prob_density * (-1 * np.ma.log2(prob_density).filled(0))
    return np.sum(ret, axis=1)


def __compute_entropy_jpdc(prob_density: np.ndarray) -> np.ndarray:
    """
    Given a Join Pitch class distribution, this function computes the join entropy value.

    :param prob_density: The join pitch class distribution. The sampe size is n.
    :type prob_density: numpy.ndarray of shape (n, n, 12).
    :return: Join entropy value array indexed by pair of time indexes.
    :rtype: numpy.ndarray of shape (n, n).
    """
    ret = prob_density * (-1 * np.ma.log2(prob_density).filled(0))
    return np.sum(ret, axis=(2, 3))


def reduce_scape_2d(scape: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Given a scape representation weighted by a quantifier, this function computes the center of gravity
    point of the scape. It also computes the covariance matrix of the sampled points.

    :param scape: Scape representation of a quantifier. The scape is computed over pieces sampled at length n.
    :type scape: numpy.ndarray of shape (n, n).
    :return: tuple formed with the Center of gravity of the scape representation and the covariance matrix.
    The coordinate of the center of gravity is express using the horitzontal time index and vertical time index.
    :rtype: (numpy.ndarray, numpy.ndarray) center of gravity is of shape (2,) and the covariance matrix is of
    shape (2,2).
    """
    __check_scape_input(scape)

    scape = np.triu(scape, k=0)
    non_zero = scape.nonzero()

    scape_nonzero = scape[non_zero]
    sum_scape_non_zero = sum(scape[non_zero])
    (t_s, t_e) = ((sum(scape_nonzero * non_zero[0]) / sum_scape_non_zero),
                  (sum(scape_nonzero * non_zero[1]) / sum_scape_non_zero))

    # compute the covariance matrix
    X = np.asarray(non_zero).transpose()
    # change the index
    Y = np.asarray([__convert_to_scape_axis(x) for x in X])

    weight = scape[non_zero]
    weight = weight / np.linalg.norm(weight)

    return (__convert_to_scape_axis(np.asarray([t_s, t_e])), np.cov(Y, rowvar=False, aweights=weight, bias=False))


def reduce_scape_horizontale(scape: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Given a scape representation weighted by a quantifier value, this function computes the mean quantifier value
    over the distance time index. It also computed the variance value over the time index distance.
    :param scape: Scape representation of a quantifier. The scape is computed over pieces sampled at length n.
    :type scape: numpy.ndarray of shape (n, n).
    :return: The mean value and the variance of the quantifier for each distance time index.
    :rtype: (numpy.ndarray, numpy.ndarray) the mean  and the variance are of shape  (n,)
    """
    __check_scape_input(scape)

    scape = np.triu(scape, k=0)
    dist = []
    variance = []
    for i in range(0, scape.shape[0]):
        dist.append(scape.diagonal(i).mean())
        variance.append(np.var(scape.diagonal(i)))

    dist = np.asarray(dist)
    variance = np.asarray(variance)

    return (dist, variance)


def reduce_1d(arr: np.ndarray) -> (float, float):
    """
    Given a horizonzal reduction of a scape, this function compute the center of gravity 1D (with variance) of
    scape.
    :param arr: Mean value of the horizontal reduction of a scape.The scape are computed on piece of length n.
    :type arr: numpy.ndarray of shape (n,)
    :return: tuple of the center of gravity and the variance of the two-way reduction of the scape.
    :rtype: (float, float)
    """
    if (type(arr) != np.ndarray):
        raise TypeError('Wrong input types.')

    if arr.ndim != 1:
        raise ValueError('Wrong number of dimension of the array.')

    index = np.arange(0, arr.shape[0])
    c = (sum(index * arr) / sum(arr))

    # variance
    norm_arr = arr / np.linalg.norm(arr)
    c_var = sum((index - c) * (index - c) * norm_arr)
    return (c, c_var)


def get_mean_var(arr: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Given a horizontale reduction of a scape, this function compute the average quantifier value (with variance).
    :param arr: Mean value of the horizontal reduction of a scape.The scape are computed on piece of length n.
    :type arr: numpy.ndarray of shape (n,)
    :return: Tuple of the average mean and variance value of the quantifier.
    :rtype: (float, float)
    """
    return (np.mean(arr), np.var(arr))


def __convert_to_scape_axis(cog: np.ndarray) -> np.ndarray:
    """
    Given a 2D point express using a start and end time index, this function express the point
    using horizontal and vertical time axes.
    :param cog: a 2D point express in start and end time axes.
    :type cog: numpy.ndarray of shape (2,)
    :return: expression of the point using horizontal and vertical time axes.
    :rtype: numpy.ndarray of shape (2,)
    """
    (t_s, t_e) = cog
    (t_h, t_v) = ((t_s + t_e) / 2, (t_e - t_s))
    return np.asarray([t_h, t_v])


def __k_l_divergence(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """
    Given two probability distributions q and p, this function computes the KLD value from q to p.

    :param q: Prior probability distribution
    :param p: Posterior probability distribution
    :type q: numpy.ndarray
    :type p: numpy.ndarray
    :return: KLD value terms indexed by time index.
    :rtype: numpy.nparray
    """
    temp = np.ma.divide(p, q).filled(0)
    return p * (np.ma.log2(temp).filled(0))


# *
def bootstrap(data: np.ndarray, func=None, n: int = 100, pickle=False, force_reset=False) -> list:
    """
    This function allows to perform bootstraping on hierarchical quantifier data.

    :param data: Hierarchical quantifer data.
    :param func: Transformation function applied to data. The return type of this function is bootstrapted.
    :param n: Bootstrap size. By default is 100.
    :type data: numpy.ndarray
    :type n: int
    :return: List of return value of the transformation function func. Each element of the list represent an
    iteration of the bootstrap.
    :rtype: list

    """

    if (type(data) != np.ndarray and type(data) != list):
        raise TypeError('Wrong input types. data')

    if type(n) != int:
        raise TypeError('Wrong input types.')

    if func is None:
        raise ValueError('no  bootstrap function is given.')
    if n <= 0:
        raise ValueError('bootstrap iteration must be hiher than 0.')

    res = read_pickle(pickle)

    if not res is None:
        return res

    res = []

    for i in range(0, n):
        temp = data[np.random.choice(data.shape[0], size=(
            data.shape[0],))]

        res.append(func(temp))

    '''
    for i in range(0, n):
        temp = data[np.random.choice(data.shape[0], size=(
            data.shape[0],))]

        res.append(temp)

    with Pool(5) as p:

        #foo = functools.partial(func)
        res = p.starmap(func,res)
        #ret = p.map(func, res)
        print(res)
    '''

    write_pickle(force_reset, res)

    return res


def global_function(x, func):
    return func(x)
