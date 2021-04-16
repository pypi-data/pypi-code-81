# UDFT: Unitary Discrete Fourier Transform and related tools
# Copyright (C) 2021 François Orieux <francois.orieux@universite-paris-saclay.fr>

# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

"""UDFT
====

Unitary discrete Fourier transform (and related)

This module implements unitary discrete Fourier transforms, which are
orthonormal. It is just a thin wrapper around Numpy or pyFFTW (maybe others in
the future), mainly done for my personal usage. They are useful for convolution
[1]: they respect the Perceval equality, the value of the null frequency is
equal to

 1
-- ∑ₙ xₙ.
√N

If the pyFFTW module is present, his functions are used.

The transforms are always applied on the last axes for performances (C-order
array). For more flexible usage, you must use the numpy.fft functions directly.

"""

import logging
import multiprocessing as mp
from typing import Tuple

import numpy as np  # type: ignore
from numpy import ndarray as array

try:
    import pyfftw  # type: ignore

    LIB = "pyFFTW"
    from pyfftw.interfaces.numpy_fft import (fftn, ifftn,  # type: ignore
                                             irfftn, rfftn)

    pyfftw.config.NUM_THREADS = mp.cpu_count()
except ImportError:
    logging.warning("Installation of the pyFFTW package improves performance.")
    LIB = "numpy"
    from numpy.fft import fftn, ifftn, irfftn, rfftn  # type: ignore


__author__ = "François Orieux"
__copyright__ = "2011, 2021, F. Orieux <francois.orieux@universite-paris-saclay.fr>"
__credits__ = ["François Orieux"]
__license__ = "WTFPL"
__version__ = "1.0.0"
__maintainer__ = "François Orieux"
__email__ = "francois.orieux@universite-paris-saclay.fr"
__status__ = "stable"
__url__ = "https://github.com/forieux/udft"
__keywords__ = "fft, Fourier"


def dftn(inarray: array, ndim: int = None) -> array:
    """ND unitary discrete Fourier transform

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    ndim : int, optional
        The `ndim` last axis along which to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.

    """
    if ndim is None:
        ndim = inarray.ndim

    return fftn(inarray, axes=range(-ndim, 0), norm="ortho")


def idftn(inarray: array, ndim: int = None) -> array:
    """ND unitary inverse discrete Fourier transform

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    ndim : int, optional
        The `ndim` last axis along wich to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : array-like
        The IDFT of `inarray` with same shape.
    """
    if ndim is None:
        ndim = inarray.ndim

    return ifftn(inarray, axes=range(-ndim, 0), norm="ortho")


def rdftn(inarray: array, ndim: int = None) -> array:
    """ND real unitary discrete Fourier transform

    Consider the Hermitian property of output with real input.

    Parameters
    ----------
    inarray : array-like
        The array of real values to transform.

    ndim : int, optional
        The `ndim` last axis along which to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray` (the last axe as N // 2 + 1 length).

    """
    if ndim is None:
        ndim = inarray.ndim

    return rfftn(inarray, axes=range(-ndim, 0), norm="ortho")


def irdftn(inarray: array, shape: Tuple[int]) -> array:
    """ND real unitary inverse discrete Fourier transform

    Consider the Hermitian property of input and return real values.

    Parameters
    ----------
    inarray : array-like
        The array to transform of complex values.

    shape : tuple of int
        The output shape of the `len(shape)` last axes.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray`.

    """
    return irfftn(inarray, s=shape, axes=range(-len(shape), 0), norm="ortho")


def dft2(inarray: array) -> array:
    """2D unitary discrete Fourier transform

    Compute the unitary discrete Fourier transform on the last 2 axes.

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.
    """
    return dftn(inarray, 2)


def idft2(inarray: array) -> array:
    """2D unitary inverse discrete Fourier transform

    Compute the unitary IDFT on the last 2 axes.

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    Returns
    -------
    outarray : array-like
        The IDFT of `inarray` with same shape.
    """
    return idftn(inarray, 2)


def rdft(inarray: array) -> array:
    """1D real unitary discrete Fourier transform

    Compute the unitary real DFT on the last axis. Consider the Hermitian
    property when the input is real.

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray`, where the last dim as length N//2+1.
    """
    return rdftn(inarray, 1)


def rdft2(inarray: array) -> array:
    """2D real unitary discrete Fourier transform

    Compute the unitary real DFT on the last 2 axes. Consider the Hermitian
    property when the input is real.

    Parameters
    ----------
    inarray : array-like
        The array to transform.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray`, where the last dim as length N//2+1.

    """
    return rdftn(inarray, 2)


def norm(inarray: array, real: bool = True) -> float:
    """Return l2-norm of array in discrete Fourier space

    Parameters
    ----------
    inarray : array-like
        The input array.

    real : boolean, optional
        If True, `array` is supposed to contain half of the frequency plane.

    Returns
    -------
    norm : float

    """
    if real:
        return 2 * np.sum(np.abs(inarray) ** 2) - np.sum(np.abs(inarray[..., 0]) ** 2)
    return np.sum(np.abs(inarray) ** 2)


def crandn(shape: Tuple[int]) -> array:
    """Draw from white complex Normal

    Draw unitary DFT of real white Gaussian field of zero mean and variance
    unity. Does not consider hermitian property, `shape` is supposed to consider
    half of the frequency plane already.
    """
    return np.sqrt(0.5) * (
        np.random.standard_normal(shape) + 1j * np.random.standard_normal(shape)
    )


def ir2fr(
    imp_resp: array, shape: Tuple[int], origin: Tuple[int] = None, real: bool = True
) -> array:
    """Compute the frequency response from impulse responses

    This function makes the necessary correct zero-padding, zero convention,
    correct DFT etc.

    The Fourier transform is performed on the last `len(shape)` dimensions for
    efficiency (C-order array).

    Parameters
    ----------
    imp_resp : array-like
        The impulse responses.

    shape : tuple of int
        A tuple of integer corresponding to the target shape of the frequency
        responses, without hermitian property. The DFT is performed on the
        `len(shape)` last axis of ndarray.

    origin : tuple of int, optional
        The index of the origin (0, 0) of the impulse response. The center by
        default (shape[i] // 2).

    real : boolean, optional
        If True, `imp_resp` is supposed real, and read DFT is used.

    Returns
    -------
    y : array-like
      The frequency responses of shape `shape` on the last `len(shape)`
      dimensions.

    Notes
    -----
    - The output is returned as C-contiguous array.
    - For convolution, the result has to be used with unitary discrete Fourier
      transform for the signal (udftn or equivalent).
    """
    if len(shape) > imp_resp.ndim:
        raise ValueError(
            "length of `shape` must be inferior or equal to `imp_resp.ndim`"
        )

    if not origin:
        origin = [length // 2 for length in imp_resp.shape[-len(shape) :]]

    if len(origin) != len(shape):
        raise ValueError("`origin` and `shape` must have the same length")

    # Place the IR at the beginning of irpadded
    # ┌────────┬──────────────┐
    # │        │              │
    # │   IR   │              │
    # │        │              │
    # │        │              │
    # ├────────┘              │
    # │            0          │
    # │                       │
    # │                       │
    # │                       │
    # └───────────────────────┘
    irpadded = np.zeros(imp_resp.shape[: -len(shape)] + shape)  # zeros of target shape
    irpadded[tuple([slice(0, s) for s in imp_resp.shape])] = imp_resp

    # Roll (circshift in Matlab) to move the origin at index 0 (DFT hypothesis)
    # ┌────────┬──────────────┐     ┌────┬─────────────┬────┐
    # │11112222│              │     │4444│             │3333│
    # │11112222│              │     │4444│             │3333│
    # │33334444│              │     ├────┘             └────┤
    # │33334444│              │     │                       │
    # ├────────┘   0          │ ->  │           0           │
    # │                       │     │                       │
    # │                       │     ├────┐             ┌────┤
    # │                       │     │2222│             │1111│
    # │                       │     │2222│             │1111│
    # └───────────────────────┘     └────┴─────────────┴────┘
    for axe, shift in enumerate(origin):
        irpadded = np.roll(irpadded, -shift, imp_resp.ndim - len(shape) + axe)

    # Perform the DFT on the last axes
    if real:
        return np.ascontiguousarray(
            rfftn(irpadded, axes=list(range(imp_resp.ndim - len(shape), imp_resp.ndim)))
        )
    return np.ascontiguousarray(
        fftn(irpadded, axes=list(range(imp_resp.ndim - len(shape), imp_resp.ndim)))
    )


def fr2ir(
    freq_resp: array, shape: Tuple[int], origin: Tuple[int] = None, real: bool = True
) -> array:
    """Return the impulse responses from frequency responses

    This function makes the necessary correct zero-padding, zero convention,
    correct DFT etc. to compute the impulse responses from frequency responses.

    The IR array is supposed to have the origin in the middle of the array.

    The Fourier transform is performed on the last `len(shape)` dimensions for
    efficiency (C-order array).

    Parameters
    ----------
    freq_resp : array-like
       The frequency responses.

    shape : tuple of int
       Output shape of the impulse responses.

    origin : tuple of int, optional
        The index of the origin (0, 0) of output the impulse response. The center by
        default (shape[i] // 2).

    real : boolean, optional
       If True, imp_resp is supposed real, and real DFT is used.

    Returns
    -------
    y : array-like
       The impulse responses of shape `shape` on the last `len(shape)` axes.

    Notes
    -----
    - The output is returned as C-contiguous array.
    - For convolution, the result has to be used with unitary discrete Fourier
      transform for the signal (udftn or equivalent).
    """
    if len(shape) > freq_resp.ndim:
        raise ValueError(
            "length of `shape` must be inferior or equal to `imp_resp.ndim`"
        )

    if not origin:
        origin = [int(np.floor(length / 2)) for length in shape]

    if len(origin) != len(shape):
        raise ValueError("`origin` and `shape` must have the same length")

    if real:
        irpadded = irfftn(
            freq_resp, axes=list(range(freq_resp.ndim - len(shape), freq_resp.ndim))
        )
    else:
        irpadded = ifftn(
            freq_resp, axes=list(range(freq_resp.ndim - len(shape), freq_resp.ndim))
        )

    for axe, shift in enumerate(origin):
        irpadded = np.roll(irpadded, shift, freq_resp.ndim - len(shape) + axe)

    return np.ascontiguousarray(irpadded[tuple([slice(0, s) for s in shape])])


def diff_ir(ndim, axe):
    """Return the impulse response of first order differences

    Parameters
    ----------
    ndim : int
        The number of dimensions.

    axe : int
        The axe where the diff operates.

    Returns
    -------
    out : array_like
        The impulse response
    """
    assert ndim > 0, "The number of dimensions `ndim` must be strictly positive."
    assert axe < ndim, "The `axe` argument must be inferior to `ndim`."

    return np.reshape(
        np.array([0, -1, 1], ndmin=ndim), [1] * axe + [3] + [1] * (ndim - axe - 1)
    )


def Laplacian(ndim: int) -> array:
    """Return the Laplacian impulse response

    The second-order difference in each axis.

    Parameters
    ----------
    ndim : int
        The dimension of the Laplacian.

    Returns
    -------
    out : array_like
        The impulse response
    """
    imp = np.zeros([3] * ndim)
    for dim in range(ndim):
        idx = tuple(
            [slice(1, 2)] * dim + [slice(None)] + [slice(1, 2)] * (ndim - dim - 1)
        )
        imp[idx] = np.array([-1.0, 0.0, -1.0]).reshape(
            [-1 if i == dim else 1 for i in range(ndim)]
        )
    imp[tuple([slice(1, 2)] * ndim)] = 2.0 * ndim
    return imp
