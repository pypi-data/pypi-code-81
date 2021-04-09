# -*- coding: utf-8 -*-
"""Functions for multiparite entanglement purification on graph states.

See README.md for an overview of the functionality.
"""
# All states are assumed to be diagonal in the graph state basis corresponding to
# the graph state considered.
# The noise should work for arbitrary graph states, while the purification
# protocol only makes sense for two-colorable graph states.
#
# Make sure the variables input follow the conventions given in the docstrings,
# since not many sanity checks are included.
#
# This should run reasonably well even for bigger states (ca. 10 qubits) if
# cythonized.

import numpy as np
from itertools import product
from functools import lru_cache


# ====Graph definitions==== #


def adj_matrix(N, E):
    """Calculates the adjacency matrix from vetices and edges.

    The graph has `N` vertices (labeled 0 to N-1) and edges `E`.

    Parameters
    ----------
    N : int
        Number of vertices.
    E : list (or tuple) of tuples
        Should contain 2-tuples with the edges of the graph. Each pair
        (i,j) indicates a connection between vertices i and j. Only
        simple, unweighted, undirected graphs are supported. Note that
        the `N` vertices are labeled 0...N-1

    Returns
    -------
    adj : np.ndarray
        Adjacency matrix of the graph specified. Is a symmetric `N` x `N` matrix
        with N_{ij}=1 if (i,j) is in `E` and 0 otherwise.

    """
    adj = np.zeros((N, N), dtype=int)
    for i, n in product(range(N), repeat=2):
        if (i, n) in E:
            adj[i, n] = 1
            adj[n, i] = 1
    return adj


class Graph(object):
    """A graph object consisting of vertices and edges.

    Other functions that need to know in which graph state basis a state is
    given expect a `Graph` object to specify the associated graph.
    The properties are read-only on purpose to make this hashable. This is
    desirable because some functions in this module profit heavily from caching.

    Parameters
    ----------
    N : int
        Number of vertices.
    E : list of tuples of ints
        Should contain 2-tuples with the edges of the graph. Each pair
        (i,j) indicates a connection between vertices i and j. Only
        simple, unweighted, undirected graphs are supported. Note that
        the `N` vertices are labeled 0...N-1
    sets : list of list of ints, optional
        Optionally define subsets of vertices, e.g. coloring of the graph
        as expected for the entanglement purification protocols. Default: []

    Attributes
    ----------
    adj : np.ndarray
        Adjacency matrix of the graph.
    N
    E
    sets
    a : tuple of ints
        the first subset of vertices (e.g. one color)
    b : tuple of ints
        the second subset of vertices (e.g. one color)

    """

    def __init__(self, N, E, sets=[]):
        self._N = N
        self._E = tuple(sorted(tuple(sorted(edge)) for edge in E))
        self._sets = tuple(tuple(sorted(set)) for set in sets)
        self._adj = tuple(tuple(row) for row in adj_matrix(N, E))

    def __repr__(self):
        return f"gg.Graph(N={self.N}, E={self.E}, sets={self.sets})"

    def __hash__(self):
        return hash((self._N, self._sets, self._adj))

    def __eq__(self, other):
        if isinstance(other, Graph):
            return (
                self.N == other.N
                and self.sets == other.sets
                and np.all(self.adj == other.adj)
            )
        else:
            return NotImplemented

    @property
    def N(self):
        return self._N

    @property
    def E(self):
        return self._E

    @property
    def sets(self):
        return self._sets

    @property
    def adj(self):
        return np.array(self._adj, dtype=int)

    @property
    def a(self):
        # subset a is the first color
        try:
            return self.sets[0]
        except IndexError:
            return None

    @property
    def b(self):
        # subset b is the first color
        try:
            return self.sets[1]
        except IndexError:
            return None


# ====Noise functions==== #


def noisy(rho, subset, graph=None):
    """Template to generate noise patterns.

    In physical terms this is correlated sigma_z noise on all particles in `subset`.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    subset : list of int
        The list of which qubits are affected, counting starts at 0.
        Indices are expected to be in order
        012...(N-1) regardless of coloring of the vertices.
    graph : Graph, optional
        Specifies in which graph state basis rho is given.
        This function does not use it - only included for consistency. Default: None

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.
    """
    N = int(np.log2(len(rho)))
    rho = rho.reshape((2,) * N)
    rho = np.flip(rho, axis=subset)
    rho = rho.reshape((2 ** N,))
    return rho


#     # if there is only one int in subset, the following is actually faster
#     # than np.flip for some reason
#     for n in subset:
#         rho = np.swapaxes(np.swapaxes(rho, 0, n)[::-1], 0, n)

#    #old, slow implementation
#    j=0
#    for n in nn:
#        k=int(np.log2(len(rho)))-1-n
#        j=j^(1<<k) # + would be slightly faster than ^ but can lead to weird behaviour
#    mu=np.zeros(len(rho))
#    for i in range(len(mu)):
#        mu[i]=rho[i^j]
#    return mu


def znoisy(rho, qubit_index, graph=None):
    """Applies sigma_z noise on the specified qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    graph : Graph, optional
        Specifies in which graph state basis rho is given.
        This function does not use it. Included only so znoisy can be called
        the same way as xnoisy and ynoisy. Default: None

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.
    """
    return noisy(rho, [qubit_index])


def xnoisy(rho, qubit_index, graph):
    """Applies sigma_x noise on the specified qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.
    """
    nn = []
    for i in range(graph.N):
        if graph.adj[qubit_index, i]:
            nn += [i]
    return noisy(rho, nn)


def ynoisy(rho, qubit_index, graph):
    """Applies sigma_y noise on the specified qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.
    """
    nn = [qubit_index]
    for i in range(graph.N):
        if graph.adj[qubit_index, i]:
            nn += [i]
    return noisy(rho, nn)


def znoise(rho, qubit_index, p, graph=None):
    """Apply Pauli-Z noise channel with error parameter `p` on a qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph, optional
        Specifies in which graph state basis rho is given. Default: None

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    return p * rho + (1 - p) * znoisy(rho, qubit_index, graph)


def xnoise(rho, qubit_index, p, graph):
    """Apply Pauli-X noise channel with error parameter `p` on a qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    return p * rho + (1 - p) * xnoisy(rho, qubit_index, graph)


def ynoise(rho, qubit_index, p, graph):
    """Apply Pauli-Y noise channel with error parameter `p` on a qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    return p * rho + (1 - p) * ynoisy(rho, qubit_index, graph)


def wnoise(rho, qubit_index, p, graph):
    """Apply local white noise channel with error parameter `p` on a qubit.

    Note: local white noise is often also called local depolarizing noise

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `qubit_index`-th qubit is affected, counting starts at 0. Indices
        are expected to be in order 012...(N-1) regardless of coloring of
        the vertices.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    return p * rho + (1 - p) / 4 * (
        rho
        + xnoisy(rho, qubit_index, graph)
        + ynoisy(rho, qubit_index, graph)
        + znoisy(rho, qubit_index, graph)
    )


def noise_pattern(rho, qubit_index, ps, graph):
    """Applies a local pauli-diagonal noise channel on the specified qubit.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    qubit_index : int
        The `n`-th qubit is affected, counting starts at 0. Indices are
        expected to be in order
        012...(N-1) regardless of coloring of the vertices.
    ps : list of scalars
        The coefficients of the noise channel.
        Should have 4 entries p_0 p_x p_y p_z that sum to 1.
    graph : Graph
        Specifies in which graph state basis rho is given.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.
    """
    return (
        ps[0] * rho
        + ps[1] * xnoisy(rho, qubit_index, graph)
        + ps[2] * ynoisy(rho, qubit_index, graph)
        + ps[3] * znoisy(rho, qubit_index, graph)
    )


def wnoise_all(rho, p, graph):
    """Apply local white noise with the same error parameter to all qubits.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph
        Specifies the graphstate considered.

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    for i in range(int(np.log2(len(rho)))):
        rho = wnoise(rho, i, p, graph)
    return rho


def noise_global(rho, p, graph=None):
    """Apply a global white noise channel to the state.

    Parameters
    ----------
    rho : np.ndarray
        Is the state acted on. Should be a 2**N-dimensional vector
        with the diagonal entries of the density matrix in the graph
        state basis.
    p : scalar
        Error parameter of the channel should be in interval [0, 1].
    graph : Graph, optional
        Specifies in which graph state basis rho is given.
        This function does not use it - only included for consistency. Default: None

    Returns
    -------
    np.ndarray
        The state after the action. Same shape as `rho`.

    """
    k = len(rho)
    return p * rho + (1 - p) * np.ones(k) / k


# ====Functions related to distance measures==== #


def fidelity(rho, mu):
    """Calculate fidelity of two states given in the same graph state basis.

    This is a special case of the general definition of the fidelity:
    F(rho, mu) = (tr(sqrt(sqrt(rho), mu, sqrt(rho))))**2
    Note that the term "fidelity" has been used ambiguously in quantum
    information theory, either referring to F or sqrt(F). F as defined here is
    the square of the fidelity as defined in Nielsen and Chuang.

    sqrt(1 - F(rho, mu)) is a distance measure.
    (1 - sqrt(F(rho, mu))) is a distance measure.

    Parameters
    ----------
    rho, mu : np.ndarray
        Diagonal entries of quantum states given in the same graph state basis.

    Returns
    -------
    scalar
        The fidelity F.

    """
    a = np.sqrt(rho)
    b = np.sqrt(mu)
    return np.dot(a, b) ** 2


def fid_alternative(rho, mu):
    """Alternative fidelity function.

    Calculates sqrt(F) instead of F (as defined in the `fidelity` fucntion).

    Parameters
    ----------
    rho, mu : np.ndarray
        Diagonal entries of quantum states given in the same graph state basis.

    Returns
    -------
    scalar
        sqrt(F)

    """
    a = np.sqrt(rho)
    b = np.sqrt(mu)
    return np.dot(a, b)


def trace_distance(rho, mu):
    """Calculate the trace distance between to states in the same graph state basis.

    Parameters
    ----------
    rho, mu : np.ndarray
        Diagonal entries of quantum states given in the same graph state basis.

    Returns
    -------
    scalar
        The trace distance.

    """
    sigma = np.abs(rho - mu)
    return 1 / 2 * np.sum(sigma)


# ====Auxiliary Functions==== #


def normalize(rho):
    """Normalize the state to trace = 1.

    Also catches numerical phenomena with entries < 0.

    Parameters
    ----------
    rho : np.ndarray
        The state to be normalized.

    Returns
    -------
    np.ndarray
        The normalized state. Same shape as `rho`.

    """
    if np.any(rho < 0):
        rho = np.copy(rho)
        rho[rho < 0] = 0
    return rho / np.sum(rho)


def local_complementation(n, graph):
    """Return the new graph after local complementation.

    Careful: Subsets are just copied so the coloring is not updated!

    Parameters
    ----------
    n : int
        Local complementation around the `n`-th vertex.
    graph : Graph
        The original graph.

    Returns
    -------
    Graph
        The graph after local complementation.

    """
    # note that Graph is only a simple graph!
    # crude implementation - surely this can be done better.

    # get neighbourhood of n
    Nn = []
    for i in range(graph.N):
        if graph.adj[i, n]:
            Nn += [i]
    new_adjmatrix = np.copy(graph.adj)
    for i in Nn:
        for k in Nn:
            if k == i:
                continue
            new_adjmatrix[i, k] = (graph.adj[i, k] + 1) % 2
    # get new edges from adjmatrix
    new_edges = []
    for i in range(graph.N):
        for k in range(i + 1, graph.N):
            if new_adjmatrix[i, k]:
                new_edges += [(i, k)]
    return Graph(
        N=graph.N, E=new_edges, sets=graph.sets
    )  # just copies sets without thinking


# ====EPP functions for two-colorable states==== #


@lru_cache(maxsize=None)  # this will be getting called a lot with the same input
def _mask_a(j, graph):
    """Spread a bit string on set a to the whole bitstring.

    Takes an int representing a bit string of length size of set a
    and spreads it to a length graph.N bit string with the bits set at the
    correct places.

    Example: graph.N = 4, graph.a = [0, 2], j=3 (bitstring "11")
             will return 10 (bitstring "1010")

    Example: graph.N = 4, graph.a = [0, 2], j=1 (bitstring "01")
             will return 2 (bitstring "0010")

    Parameters
    ----------
    j : int
        Representing a bit string of length len(graph.a).
    graph : Graph
        The graph containing information about the set.

    Returns
    -------
    int
        Representing a bit string of length graph.N, i.e. `j` spread out over
        the appropriate positions in the bit string.

    """
    m = ["0"] * graph.N
    short_string = format(j, "0" + str(len(graph.a)) + "b")
    for bit, idx in zip(short_string, graph.a):
        m[idx] = bit
    long_string = "".join(m)
    return int(long_string, base=2)


@lru_cache(maxsize=None)  # this will be getting called a lot with the same input
def _mask_b(j, graph):
    """Spread a bit string on set b to the whole bitstring.

    Takes an int representing a bit string of length size of set b
    and spreads it to a length graph.N bit string with the bits set at the
    correct places.

    Example: graph.N = 4, graph.b = [1, 3], j=3 (bitstring "11")
             will return 10 (bitstring "0101")

    Example: graph.N = 4, graph.b = [1, 3], j=1 (bitstring "01")
             will return 2 (bitstring "0001")

    Parameters
    ----------
    j : int
        Representing a bit string of length len(graph.b).
    graph : Graph
        The graph containing information about the set.

    Returns
    -------
    int
        Representing a bit string of length graph.N, i.e. `j` spread out over
        the appropriate positions in the bit string.

    """
    m = ["0"] * graph.N
    short_string = format(j, "0" + str(len(graph.b)) + "b")
    for bit, idx in zip(short_string, graph.b):
        m[idx] = bit
    long_string = "".join(m)
    return int(long_string, base=2)


# Note: np.fromfunction does not help with speeding up p1p2, but cythonizing does!
def p1(rho, graph):
    """Perform protocol P1 of the ADB protocol for two-colorable graph states.

    Implements equation (17) of Phys. Rev. A 71, 012319 (2005)
    Preprint: https://arxiv.org/abs/quant-ph/0405045

    Comment on the implementation:
    The integers used here correspond to the bit strings in the publication
    as follows:
    i ~ γ_A,γ_B
    j ~ 0,γ_B
    k ~ ν_B
    m ~ 0,ν_B
    and therefore:
    i^j     ~ γ_A,0
    (i^j)^m ~ γ_A,ν_B
    i^m     ~ γ_A,(γ_B ⊕ ν_B)
    So the loop over k iterates over all possible ν_B. While equation (17)
    suggests another loop over μ_B, there is only one μ_B = (γ_B ⊕ ν_B) that
    fulfils the specified condition ν_B ⊕ μ_B = γ_B so another nested loop is
    not necessary.

    Parameters
    ----------
    rho : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        Two copies of this state will be used to perform the protocol.
    graph : Graph
        Graph of the target graph state to be purified. rho is given in this
        graph state basis. Must contain coloring information of the
        two-colorable graph state.

    Returns
    -------
    np.ndarray
        The output state of the protocol, assuming the purification step was
        successful.

    """
    mu = np.zeros(len(rho))
    for i in range(2 ** graph.N):
        j = i & (_mask_b((1 << len(graph.b)) - 1, graph))
        for k in range(2 ** len(graph.b)):
            m = _mask_b(k, graph)
            mu[i] += rho[(i ^ j) ^ m] * rho[i ^ m]
    mu = normalize(mu)
    return mu


def p2(rho, graph):
    """Perform protocol P2 of the ADB protocol for two-colorable graph states.

    Implements equation (19) of Phys. Rev. A 71, 012319 (2005)
    Preprint: https://arxiv.org/abs/quant-ph/0405045

    See docstring of p1 for comment on the iterations and bit strings.

    Parameters
    ----------
    rho : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        Two copies of this state will be used to perform the protocol.
    graph : Graph
        Graph of the target graph state to be purified. rho is given in this
        graph state basis. Must contain coloring information of the
        two-colorable graph state.

    Returns
    -------
    np.ndarray
        The output state of the protocol, assuming the purification step was
        successful.

    """
    mu = np.zeros(len(rho))
    for i in range(2 ** graph.N):
        j = i & (_mask_a((1 << len(graph.a)) - 1, graph))
        for k in range(2 ** len(graph.a)):
            m = _mask_a(k, graph)
            mu[i] += rho[(i ^ j) ^ m] * rho[i ^ m]
    mu = normalize(mu)
    return mu


def p1_var(rho, sigma, graph):
    """P1 but with two different input states instead of two copies of the same.

    Parameters
    ----------
    rho : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        First input state.
    sigma : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        Second input state.
    graph : Graph
        Graph of the target graph state to be purified. rho and mu are
        given in this graph state basis. Must contain coloring information
        of the two-colorable graph state.

    Returns
    -------
    np.ndarray
        The output state of the protocol, assuming the purification step was
        successful.

    """
    mu = np.zeros(len(rho))
    for i in range(2 ** graph.N):
        j = i & (_mask_b((1 << len(graph.b)) - 1, graph))
        for k in range(2 ** len(graph.b)):
            m = _mask_b(k, graph)
            mu[i] += rho[(i ^ j) ^ m] * sigma[i ^ m]
    mu = normalize(mu)
    return mu


def p2_var(rho, sigma, graph):
    """P2 but with two different input states instead of two copies of the same.

    Parameters
    ----------
    rho : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        First input state.
    sigma : np.ndarray
        Diagonal entries of a density matrix in the graph state basis.
        Second input state.
    graph : Graph
        Graph of the target graph state to be purified. rho and mu are
        given in this graph state basis. Must contain coloring information
        of the two-colorable graph state.

    Returns
    -------
    np.ndarray
        The output state of the protocol, assuming the purification step was
        successful.

    """
    mu = np.zeros(len(rho))
    for i in range(2 ** graph.N):
        j = i & (_mask_a((1 << len(graph.a)) - 1, graph))
        for k in range(2 ** len(graph.a)):
            m = _mask_a(k, graph)
            mu[i] += rho[(i ^ j) ^ m] * sigma[i ^ m]
    mu = normalize(mu)
    return mu


# ====EPP functions for arbitrary graph states==== #


@lru_cache(maxsize=None)
def _mask_k(j, graph, subset):
    """Spread a bit string on a subset to the whole bitstring.

    Takes an int representing a bit string of length len(myset)
    and spreads it to a length graph.N bit string with the bits set at the
    correct places.

    Example: graph.N = 4, myset = (0, 2), j=3 (bitstring "11")
             will return 10 (bitstring "1010")

    Example: graph.N = 4, myset = (0, 2), j=1 (bitstring "01")
             will return 2 (bitstring "0010")

    Parameters
    ----------
    j : int
        Representing a bit string of length len(subset).
    graph : Graph
        The graph, basically just here for graph.N
    subset : tuple of ints
        A subset of vertices of the graph. Ideally use a tuple not a list to
        allow caching to work.

    Returns
    -------
    int
        Representing a bit string of length graph.N, i.e. `j` spread out over
        the appropriate positions in the bit string.

    """
    m = ["0"] * graph.N
    short_string = format(j, "0" + str(len(subset)) + "b")
    for bit, idx in zip(short_string, subset):
        m[idx] = bit
    long_string = "".join(m)
    return int(long_string, base=2)


def pk(rho, sigma, graph1, graph2, subset):
    """Perform sub-protocol P_k.

    A sub-protocol of the entanglement purification protocol for all graph
    states. Implements equation (8) of Phys. Rev. A 74, 052316 (2006)
    Preprint: https://arxiv.org/abs/quant-ph/0606090

    See docstring of p1 for comment on the iterations and bit strings.

    Parameters
    ----------
    rho : np.ndarray
        Diagonal entries of a density matrix in the graph state basis
        corresponding to `graph1`. Main input state.
    sigma : np.ndarray
        Diagonal entries of a density matrix in the graph state basis
        corresponding to `graph2`. Auxiliary input state. Make sure it
        has the same number of qubits as `rho` (expand with unconnected
        vertices if needed).
    graph1 : Graph
        The main graph of the protocol.
    graph2 : Graph
        The auxiliary graph for the k-th subset for the k-th sub-protocol P_k.
        Make sure it has the same number of vertices as `graph1`
        (expand with unconnected vertices if needed).
    subset : tuple of ints
        A subset of vertices, corresponding to the k-th subset.

    Returns
    -------
    np.ndarray
        The output state of the protocol, assuming the purification step was
        successful.

    """
    mu = np.zeros(len(rho))
    other_set = tuple(i for i in range(graph1.N) if i not in subset)
    for i in range(2 ** graph1.N):
        j = i & (_mask_k((1 << len(other_set)) - 1, graph1, other_set))
        for k in range(2 ** len(other_set)):
            m = _mask_k(k, graph1, other_set)
            mu[i] += rho[(i ^ j) ^ m] * sigma[i ^ m]
    mu = normalize(mu)
    return mu
