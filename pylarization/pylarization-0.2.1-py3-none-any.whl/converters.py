"""
Module with converters for different polarization notations.
"""
import numpy as np
from pylarization.vectors import JonesVector, StokesVector
from pylarization.matrices import CoherencyMatrix


def jones_to_stokes(jones: JonesVector) -> StokesVector:
    """
    Converts a single JonesVector instance to a StokesVector
    """
    Ex, Ey = jones.vector
    phase = jones.phase
    mx = (Ex).real
    my = np.sqrt(Ey * np.conj(Ey)).real

    I = 1
    M = np.square(mx) - np.square(my)
    C = 2 * mx * my * np.cos(phase)
    S = 2 * mx * my * np.sin(phase)

    return StokesVector(I, M, C, S)

def stokes_to_jones(stokes: StokesVector) -> JonesVector:
    """
    Converts a single StokesVector instance to a JonesVector

    :Note:
    Please note that due to nature of this conversion, the phase may be off.
    """
    I, Q, U, V = stokes.vector
    polarization_degree = np.sqrt(Q**2+U**2+V**2)/I
    stokes.normalize()
    _, Q, U, V = stokes.vector
    mx = np.sqrt((1+Q)/2)
    my = 1 if np.isclose(mx, 0) else U/(2*mx) + 1j*V/(2*mx)
    tmp_array = np.array([mx, my], dtype=complex)
    np.sqrt(I*polarization_degree) * tmp_array
    return JonesVector.from_matrix(tmp_array)

def stokes_to_coherency(stokes: StokesVector) -> CoherencyMatrix:
    """
    Converts a single StokesVector instance to a CoherencyMatrix
    """
    # I, M, C, S = stokes.vector
    # Ixx = I + M
    # Ixy = C + 1j * S
    # Iyx = C - 1j * S
    # Iyy = I - M
    jones = stokes_to_jones(stokes)
    return jones_to_coherency(jones)

def coherency_to_stokes(coherency: CoherencyMatrix) -> StokesVector:
    """
    Converts a single CoherencyMatrix isntance to a StokesVector
    """
    Ixx, Ixy, Iyx, Iyy = coherency.matrix.flatten()
    I = Ixx + Iyy
    M = Ixx - Iyy
    C = Ixy + Iyx
    S = 1j * (Ixy - Iyx)
    return StokesVector(I, M, C, S)

def jones_to_coherency(jones: JonesVector) -> CoherencyMatrix:
    """
    Converts a single JonesVector instance to a CoherencyMatrix
    """
    Ex, Ey = jones.vector
    Ixx = Ex * np.conj(Ex)
    Ixy = Ex * np.conj(Ey)
    Iyx = Ey * np.conj(Ex)
    Iyy = Ey * np.conj(Ey)
    return CoherencyMatrix(Ixx, Ixy, Iyx, Iyy)

def coherency_to_jones(coherency: CoherencyMatrix) -> JonesVector:
    """
    Converts a single CoherencyMatrix isntance to a JonesVector
    """
    stokes = coherency_to_stokes(coherency)
    return stokes_to_jones(stokes)
