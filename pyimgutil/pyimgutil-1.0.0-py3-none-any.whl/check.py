"""Check the parsed arguments to make sure they are valid.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import argparse
import logging
from pathlib import Path
import textwrap
from typing import Tuple, Union

from PIL import Image

from pyimgutil import commands


logger = logging.getLogger(__name__)


def check_arguments(args: argparse.Namespace) -> None:
    """Determine if a given set of arguments are valid.

    Parameters
    ----------
    args : :obj:`argparse.Namespace`
        A Namespace object of parsed arguments.

    Returns
    -------
    None

    Raises
    -----
    ValueError
        If an argument is considered invalid.

    """
    logger.debug("Entering 'check_arguments'.")
    logger.debug(f"Parameter values: {locals()}")
    numerical_attributes = [
        "left",
        "upper",
        "right",
        "bottom",
        "height",
        "width",
        "scale",
    ]
    if args.command is None:
        logger.error("No command was provided.")
        raise ValueError
    if not is_valid_input(args.input):
        logger.error("The input path provided is not valid.")
        print(
            textwrap.dedent(
                """\
                The input path provided is not valid.
                Check to make sure the path:
                    - exists
                    - is a supported image file, or
                    - is a directory containing a supported image file\
                """
            )
        )
        raise ValueError
    logger.debug("Input path is valid.")

    if args.output and not is_valid_output(args.input, args.output):
        logger.error("The output path provided is not valid.")
        print(
            textwrap.dedent(
                """\
                The output path provided is not valid.
                If the input path is a directory, the output path must
                also be a directory.\
                """
            )
        )
        raise ValueError
    logger.debug("Output path is valid.")

    for attribute in numerical_attributes:
        if not hasattr(args, attribute) or getattr(args, attribute) is None:
            logger.debug(f"Attribute '{attribute}' is not defined.")
            continue
        if not is_valid_argument_value(getattr(args, attribute)):
            logger.error(
                f"The '{attribute}' argument provided is not valid."
            )
            print(
                textwrap.dedent(
                    f"""\
                    The '{attribute}' argument provided is not valid.
                    All arguments that specify numbers must zero or greater.\
                    """
                )
            )
            raise ValueError
        logger.debug(f"Argument '{attribute}' is valid.")
    logger.debug("All arguments are considered valid.")


def is_valid_argument_value(value: Union[int, float]) -> bool:
    """Determine if a given value is a valid argument.

    Parameters
    ----------
    value : int or float
        The value of the argument to be checked.

    Returns
    -------
    bool
        True if value is valid, False if not.

    """
    logger.debug("Entering 'is_valid_argument_value'.")
    logger.debug(f"Parameter values: {locals()}")
    if value >= 0:
        logger.debug("Value is greater than zero.")
        return True
    else:
        logger.error("Value is less than zero.")
        return False


def is_valid_crop_box(image: Image, box: Tuple[int, int, int, int]) -> Image:
    """Determine if the specified crop dimensions are valid.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image object to be cropped.
    box : tuple of int
        Four coordinates representing the left, upper, right, and
        bottom edges, respectively, of the crop box.

    Returns
    -------
    bool
        True if box is valid, False if not.

    Notes
    -----
    An image can be cropped to be larger than it originally was, but
    this is not intended functionality here.

    """
    logger.debug("Entering 'is_valid_crop_box'.")
    logger.debug(f"Parameter values: {locals()}")
    for index, coord in enumerate(box):
        # An unspecified coordinate is always valid.
        if not coord:
            continue
        if coord < 0:
            logger.error(f"Coordinate cannot be less than zero: {coord}")
            return False
        if (index == 0 or index == 2) and coord > image.width:
            logger.error(f"Coordinate '{coord}' is greater than image width.")
            return False
        if (index == 1 or index == 3) and coord > image.height:
            logger.error(f"Coordinate '{coord}' is greater than image height.")
            return False
    if (box[0] and box[2]) and box[0] > box[2]:
        logger.error(f"Left '{box[0]}' is greater than right '{box[2]}'.")
        return False
    if (box[1] and box[3]) and box[1] > box[3]:
        logger.error(f"Upper '{box[1]}' is greater than bottom '{box[3]}'.")
        return False
    return True


def is_valid_input(path: Path) -> bool:
    """Determine if a given input path is valid.

    Parameters
    ----------
    path : pathlib.Path
        The path being checked.

    Returns
    -------
    bool
        True if path is valid, False if not.

    Notes
    -----
    A valid input path is one of the following:
    - a file whose extension matches a supported image format.
    - a directory that contains at least one file whose extension
    matches a supported image format.

    """
    logger.debug("Entering 'is_valid_input'.")
    logger.debug(f"Parameter values: {locals()}")
    if not path.exists():
        logger.error("Input path does not exist.")
        return False
    elif path.is_file() and path.suffix.lower() in commands.VALID_SUFFIXES:
        logger.debug("Input path is a valid image file.")
        return True
    elif path.is_file() and path.suffix.lower() not in commands.VALID_SUFFIXES:
        logger.error("Input path is not a valid image file.")
        return False
    else:
        logger.debug("Input path is a directory.")
        if len(commands.get_input_files(path)) > 0:
            logger.debug("At least one image file found.")
            return True
        else:
            logger.error("Input path does not contain any image files.")
            return False


def is_valid_output(input_path: Path, output_path: Path) -> bool:
    """Determine if a given output path is valid.

    Parameters
    ----------
    input_path : pathlib.Path
        The chosen input path.
    output_path : pathlib.Path
        The output path being checked.

    Returns
    -------
    bool
        True if output path is valid, False if not.

    Notes
    -----
    If the input path is a directory, the output path must also be a
    directory. Otherwise, multiple files could be found in the input
    path, but only one of the files would have a location in which to
    be saved.

    """
    logger.debug("Entering 'is_valid_output'.")
    logger.debug(f"Parameter values: {locals()}")
    if input_path.is_dir() and output_path.suffix != "":
        logger.error("Input path is a directory, but output path is a file.")
        return False
    else:
        return True
