import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import typer
import yaml

try:
    from openbabel import pybel
except ImportError:
    import pybel

logger = logging.getLogger(__name__)


def recursive_settings(settings: Dict[str, str], iteration: Union[int, None]) -> str:
    """Recursive function to unpack a settings file.

    If settings is just {foo: bar} then this function will run once and
    return 'foo=bar'
    If settings is a nested dictionary like {foo: {bar: baz}} then the output
    will be foo=(bar=baz) by calling itself on the inner dictionary.
    See https://en.wikipedia.org/wiki/Recursive_function for an explanation.

    non_keywords is a special keyword the value of which gets just inserted into
    the string.

    Parameters:
    settings: A dictonary with key value pairs of settings
    iteration: Number of iteration for list based maxsteps

    Returns
    -------
    route_string_addition: The decoded string to be inserted into the gaussian header
        command
    """
    if not isinstance(settings, dict):
        raise ValueError(f"Expected a dictonary but got: {type(settings)}")
    route_addition = ""
    # capturing one special case where only non_keywords are given so no ', '
    # needs to be applied
    if ("non_keywords" in settings) and len(settings) > 1:
        route_addition += settings["non_keywords"]
        del settings["non_keywords"]
    elif "non_keywords" in settings:
        route_addition += settings["non_keywords"]
        del settings["non_keywords"]

    for k, v in settings.items():
        if isinstance(v, dict):
            route_addition += (
                ", " + "=(".join([k, recursive_settings(v, iteration)]) + ")"
            )
        else:
            if route_addition != "":
                route_addition += ", "
            if (k == "maxstep") and (isinstance(v, list) and (iteration is None)):
                raise TypeError(
                    "maxstep as a list only works with the workflow command."
                )
            elif (k == "maxstep") and (
                isinstance(v, list) and isinstance(iteration, int)
            ):
                if (iteration > (len(v) - 1)) and (len(v) > 0):
                    v = v[-1]
                else:
                    v = v[iteration]
            route_addition += "=".join([k, v])
    return route_addition


def build_gaussian_header(
    settings: Dict[str, Dict], iteration: Union[int, None]
) -> str:
    """Build the Gaussian header section

    Build link_0 and route header for Gaussian input file. Checks if link_0
    exists and adds everything accordingly. Respects non_keywords option of
    config.yaml file.

    Parameters:
        settings: Can include link_0 option but must include route options.

    Returns:
        header: Header section of Gaussian input file.
        iteration: Index for list based dynamic maxsteps
    """
    # check that the Gaussian part of the config is valid
    if None in settings.values():
        raise ValueError("There should be no None values in the config, please check")
    # keywords check for link_0 and route, other keywords are ignored
    if "link_0" not in settings.keys() and "route" not in settings.keys():
        return "#Put Keywords Here, check Charge and Multiplicity."

    # handle link_0
    if "link_0" not in settings.keys():
        link_0 = ""
    else:
        link_0 = "".join(f"%{k}={v}\n" for k, v in settings["link_0"].items())

    # handle route settings
    if "route" not in settings.keys():
        route = "#Put Keywords Here, check Charge and Multiplicity."
    else:
        route = "# "

    # because settings can be nested several layers use a recursive function
    # to unpack them
    route = "# " + recursive_settings(settings["route"], iteration)
    header = link_0 + "\n" + route
    return header


def validate_input_format(input_format: str) -> str:
    if input_format not in pybel.informats:
        logger.error("Not a valid openbabel format.")
        raise typer.BadParameter(
            "Not a valid openbabel format provided. "
            "See https://openbabel.org/wiki/Category:Formats "
            "for correct formats."
        )
    else:
        return input_format


def io(
    input_files: List[str] = typer.Argument(
        ...,
        help="One or more input files for which a gaussian input file should be generated.",
    ),
    input_format: str = typer.Option(
        "mol2",
        help="Input format of the molecule file, must be openbabel compatible.",
        callback=validate_input_format,
    ),
    config_file: Path = typer.Option(
        "config.yaml", help="The project configuration file."
    ),
    output_file_name: str = typer.Option(
        False,
        help=(
            "If only one file is provided, this option can be used to define the output filename. "
            "Will be ignored in the mulitple file case."
        ),
    ),
    force: bool = typer.Option(
        False, help="Force smoothtransitions to overwrite existing gjf files."
    ),
    section: str = typer.Option(None, help="Which section of the config file to use."),
    iteration: Optional[int] = typer.Option(None, hidden=True),
) -> None:
    """
    Function that handles creating gjf files from various input formats.
    If multiple structures are in a specific input file, the application will
    always take the last one.
    """
    ignore_output_filename = False
    logger.info(f"Inputfiles: {input_files}")
    logger.info(f"Configfile {config_file}")
    if len(input_files) > 1:
        logger.info("More than one input file provided, ignoring Outputfilename.")
        ignore_output_filename = True
    else:
        logger.info(f"Outputfile name {output_file_name}")
    with open(config_file, "r") as stream:
        config = yaml.safe_load(stream)
    # when the config defines charge and/or multiplicity then set them here
    if "molecule_properties" in config.keys():
        mol_settings = config["molecule_properties"]
    else:
        mol_settings = {}
    # if a section is provided verify and use it otherwise take the first-stage
    if section:
        assert section in config.keys()
        config = config[section]
    else:
        config = config["first-stage"]

    for mol_file in input_files:
        mol_file_path = Path(mol_file)
        filename = mol_file_path.stem
        mol = list(pybel.readfile(input_format, str(mol_file_path)))
        if len(mol) < 1:
            logger.error(
                "No structure detected in file. "
                "Either faulty format or wrong input format specified?"
            )
            raise ValueError("No structure found, either wrong file or format")
        structure = mol[-1]
        # change molecule properties here according to the settings in the yaml file
        if "charge" in mol_settings:
            structure.OBMol.SetTotalCharge(mol_settings["charge"])
        if "multiplicity" in mol_settings:
            structure.OBMol.SetTotalSpinMultiplicity(mol_settings["multiplicity"])
        gaussian_header = build_gaussian_header(config["gaussian"], iteration)
        if ignore_output_filename or (output_file_name is None):
            output_file_name = f"{filename}.gjf"
        try:
            # usually for constraints we want to fix all bonds
            # Therefore if the section is named constraint we will include
            # all bond information into the outputfile
            if section == "constraint":
                structure.write(
                    "gjf",
                    f"{output_file_name}",
                    opt={"k": gaussian_header, "b": ""},
                    overwrite=force,
                )
            else:
                structure.write(
                    "gjf",
                    f"{output_file_name}",
                    opt={"k": gaussian_header},
                    overwrite=force,
                )
            # additional contraints can be added
            # gaussian is very sensitive to trailing empty lines
            # therefore adding those here is important
            if section == "constraint" and "constraint" in config:
                with open(output_file_name, "a") as f:
                    f.write("\n")
                    for x in config["constraint"]:
                        f.write(f"{x}\n")
            if "pseudoread" in config:
                with open(output_file_name, "a") as f:
                    if section == "constraint":
                        f.write("\n")
                    for x in config["pseudoread"]:
                        f.write(f"{x}\n")
                    f.write("\n")
        except OSError:
            logger.error(
                (
                    "Outputfile could not be written, it might already exist. "
                    "You can force writing by running the script using the "
                    "--force flat"
                )
            )
            raise ValueError("Outputfile already exists")
