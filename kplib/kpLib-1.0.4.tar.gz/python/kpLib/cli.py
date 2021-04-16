import click
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Kpoints, Kpoints_supported_modes
from kpLib import __version__
from kpLib.interface import get_kpoints


@click.command()
@click.argument("Structure", default="POSCAR", required=False)
@click.option(
    "-t",
    "--type",
    "ktype",
    default="AUTO",
    type=click.Choice(["AUTO", "GAMMA", "SHIFTED"], case_sensitive=False),
    help="Type of Kpoint grid: auto-determined, gamma centered, or shifted"
    "to not include gamma",
)
@click.option(
    "--symprec", default=1e-5, help="Precision for symmetry finding in spglib."
)
@click.option(
    "-s",
    "--use_scale_factor",
    default=False,
    type=bool,
    is_flag=True,
    help="Whether use scale factor for large size grids.",
)
@click.option(
    "-d",
    "--min_distance",
    default=0.1,
    help="Minimum allowed distance of any lattice points on "
    "real-space superlattice.",
)
@click.option(
    "-n",
    "--min_total_kpoints",
    default=1,
    help="Minimum allowed number of total k-points.",
)
@click.option(
    "--version",
    "print_version",
    type=bool,
    is_flag=True,
    help="Prints out the version information for kpGen",
)
def generate(
    structure,
    min_distance,
    min_total_kpoints,
    ktype,
    symprec,
    use_scale_factor,
    print_version,
):
    """
    This script generates a KPOINTs output for a given structure a
    VASP POSCAR, Pymatgen structure JSON, or CIF
    """

    if print_version:
        print(f"v{__version__}")
        return

    struc = Structure.from_file(structure)
    if ktype == "GAMMA":
        include_gamma = True
    elif ktype == "SHIFTED":
        include_gamma = False
    else:
        include_gamma = None

    click.echo(f"Running kpLib on {struc.composition.reduced_formula}")
    kpts = get_kpoints(
        struc,
        minDistance=min_distance,
        minTotalKpoints=min_total_kpoints,
        include_gamma=include_gamma,
    )

    # Get distinct points and weights for KPOINTS file
    distinct_coords, distinct_weights = zip(
        *[
            (coord, weight)
            for (coord, weight) in zip(kpts["coords"], kpts["weights"])
            if weight > 0
        ]
    )

    click.echo(f"Generated {len(distinct_coords)} distinct kpoints")
    click.echo(f"Minimum periodic distance is {kpts['min_periodic_distance']}")

    comment = (
        f"kpLib version: {__version__}. "
        f"K-Point grid has {kpts['num_total_kpts']} total points. "
        "Actual minimum periodic distance is"
        f" {kpts['min_periodic_distance']} Angstroms. "
    )
    if any([np.allclose(d, [0.0, 0.0, 0.0]) for d in distinct_coords]):
        click.echo("Grid includes gamma point.")
        comment += " Grid includes gamma point."
    else:
        click.echo("Grid does not include gamma point.")
        comment += " Grid does not include gamma point."

    kpts_obj = Kpoints(
        comment=comment,
        style=Kpoints_supported_modes.Reciprocal,
        num_kpts=len(distinct_coords),
        kpts=distinct_coords,
        kpts_weights=distinct_weights,
    )

    kpts_obj.write_file("KPOINTS")
