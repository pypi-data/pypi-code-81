from sys import maxsize as max_int
import numpy as np
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from kpLib.lib import KPointLattice, KPointLatticeGenerator, INCLUDE_GAMMA


def get_kpoints(
    structure,
    include_gamma=None,
    symprec=1e-5,
    use_scale_factor=False,
    minDistance=0.1,
    minTotalKpoints=1,
):
    """
    Gets KPoints using the C++ kpLib

    Args:
        structure (Structure): pymatgen structure object to compute
        include_gamma (bool): include Gamma point in KPoints
            default is to auto-detect if None
        symprec (float): symmetry finding precision for spglib
        use_scale_factor (bool): enables using a scaling factor
            to find the best grid for a small grid size and then scaling up
            this improves the speed for finding very dense grids
        minDistance(float): minimum distance between K-points
        minTotalKpoint(int): minimum number of k-points in the optimized grid
    """

    spg_analyzer = SpacegroupAnalyzer(structure, symprec=symprec)
    spacegroup = spg_analyzer.get_space_group_number()
    conventional_lattice = (
        spg_analyzer.get_conventional_standard_structure().lattice.matrix
    )
    rotations = np.array(
        [op.rotation_matrix for op in spg_analyzer.get_point_group_operations()]
    ).astype(int)
    is_conventional_hex = 143 <= spacegroup <= 194

    # The monoclinic system (2/m Laue class) should use the 2-fold axis
    # as the 3rd-vector in the conventional lattice.
    if 3 <= spacegroup <= 15:
        # Make the e_pri direction in spglib the 3rd vector.
        # We do this by swapping the column vectors: 1->2; 2->3; 3->1
        # to keep determinant positive.
        conventional_lattice = np.roll(conventional_lattice, 1)

    # Ensure there is an inversion operator in the set
    inv_op = np.array([[-1.0, 0, 0], [0, -1.0, 0], [0, 0, -1.0]])
    if not any(np.allclose(rot, inv_op) for rot in rotations):
        inv_rotations = np.zeros((rotations.shape[0], 3, 3)).astype(int)
        for i, rot in zip(range(rotations.shape[0]), rotations):
            inv_rotations[i] = rotations[i].dot(inv_op)
        rotations = np.concatenate((rotations, inv_rotations)).astype(int)

    kpt_gen = KPointLatticeGenerator(
        structure.lattice.matrix,
        conventional_lattice,
        rotations.transpose(0, 2, 1),
        is_conventional_hex,
    )

    if include_gamma:
        kpt_gen.includeGamma(INCLUDE_GAMMA.TRUE)
    elif include_gamma is False:
        kpt_gen.includeGamma(INCLUDE_GAMMA.FALSE)
    else:
        kpt_gen.includeGamma(INCLUDE_GAMMA.AUTO)

    if use_scale_factor:
        kpt_gen.useScaleFactor(spacegroup)

    lattice = kpt_gen.getKPointLattice(minDistance, minTotalKpoints)

    if lattice.getNumDistinctKPoints() == max_int:
        raise Exception(
            "Error: There is a problem generating k-point grid based "
            "on your input. If you have activated scale factor, please "
            "check your request doesn't exceed the maximum allowed "
            "number of k-points."
        )

    periodic_distance = lattice.getMinPeriodicDistance()
    num_distinct_kpts = lattice.getNumDistinctKPoints()
    num_total_kpts = lattice.numTotalKPoints()
    kpt_coords = lattice.getKPointCoordinates()
    kpt_weights = lattice.getKPointWeights()

    return {
        "min_periodic_distance": periodic_distance,
        "num_distinct_kpts": num_distinct_kpts,
        "num_total_kpts": num_total_kpts,
        "coords": kpt_coords,
        "weights": kpt_weights,
    }
