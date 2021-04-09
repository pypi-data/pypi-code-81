"""Perform the actual command specified by the user.

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
import logging
import os
from pathlib import Path
import re
from typing import List, Tuple

from PIL import Image


logger = logging.getLogger(__name__)
VALID_SUFFIXES = [
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".ppm",
]


def attach_message(filename: Path, message: str, location: int) -> Path:
    """Attach a message to the beginning or end of a filename.

    Parameters
    ----------
    filename : :obj:`pathlib.Path`
        The name of the file being modified.
    message : str
        The message to be attached.
    location : int
        The location on the filename to attach the message.
        0 to prepend, 1 to append.

    """
    logger.debug("Entering 'attach_message'.")
    logger.debug(f"Parameter values: {locals()}")
    if not location:
        logger.debug("Message will be prepended.")
        return Path(message + filename.name)
    else:
        logger.debug("Message will be appended.")
        return Path(filename.stem + message + filename.suffix)


def crop_image(image: Image, box: Tuple[int, int, int, int]) -> Image:
    """Remove unwanted portions of an image.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image object to be cropped.
    box : tuple of int
        Four coordinates representing the left, upper, right, and
        bottom edges of the crop box.

    Returns
    -------
    cropped_image : :obj:`PIL.Image`
        The cropped image object.

    Notes
    -----
    If a box coordinate is None, the corresponding image coordinate
    will be used for the crop.

    """
    logger.debug("Entering 'crop_image'.")
    logger.debug(f"Parameter values: {locals()}")
    temp_box = []
    # Do not crop unspecified coordinates.
    for index, coord in enumerate(box):
        if (index == 0 or index == 1) and not coord:
            temp_box.append(0)
        elif index == 2 and not coord:
            temp_box.append(image.width)
        elif index == 3 and not coord:
            temp_box.append(image.height)
        else:
            temp_box.append(coord)
    final_box = tuple(temp_box)
    logger.debug(f"Final crop box: {final_box}")
    logger.debug(f"Image before crop: {image}")
    cropped_image = image.crop(final_box)
    logger.debug(f"Image after crop: {cropped_image}")
    return cropped_image


def get_input_files(path: Path) -> List[Path]:
    """Find supported files located in the input path.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        A validated input path.

    Returns
    -------
    image_files : list of `pathlib.Path`
        The paths to the supported files that were found.

    Notes
    -----
    This function assumes the input path has already been validated.
    No exceptions will be raised should a file not be found.

    """
    logger.debug("Entering 'get_input_files'.")
    logger.debug(f"Parameter values: {locals()}")
    image_files: List[Path] = []
    for suffix in VALID_SUFFIXES:
        logger.debug(f"Checking for suffix: {suffix}")
        # Glob is more succinct, but doesn't handle mixed-case.
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if re.search(rf"{suffix}$", filename, re.IGNORECASE):
                    image_path = Path(dirpath) / filename
                    image_files.append(image_path)
                    logger.debug(f"Found a '{suffix}' file.")
    logger.debug(f"Found '{len(image_files)}' image files.")
    return image_files


def resize_image(
    image: Image,
    width: int,
    height: int,
    ratio: bool,
    scale: float,
) -> Image:
    """Resize an image.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be resized.
    width : int
        The width, in pixels, of the resulting image.
    height : int
        The height, in pixels, of the resulting image.
    ratio : bool
        Whether or not to retain the original image's aspect ratio.
    scale : float
        The amount to scale the image (respects aspect ratio).

    Returns
    -------
    :obj:`PIL.Image`
        The image that has been resized.

    """
    logger.debug("Entering 'resize_image'.")
    logger.debug(f"Parameter values: {locals()}")
    pre_ratio = image.width / image.height
    logger.debug(f"Pre-command width: {image.width}")
    logger.debug(f"Pre-command height: {image.height}")
    logger.debug(f"Pre-command aspect ratio: {round(pre_ratio, 6)}")
    if scale:
        width = int(image.width * scale)
        height = int(image.height * scale)
    elif ratio:
        if width and not height:
            height = int(width / pre_ratio)
        if height and not width:
            width = int(pre_ratio * height)
    else:
        if width is None:
            width = image.width
        if height is None:
            height = image.height
    resized_image = image.resize((width, height))
    post_ratio = resized_image.width / resized_image.height
    logger.debug(f"Post-command width: {resized_image.width}")
    logger.debug(f"Post-command height: {resized_image.height}")
    logger.debug(f"Post-command aspect ratio: {round(post_ratio, 6)}")
    return resized_image


def save_output(image: Image, path: Path, name: Path, force: bool) -> None:
    """Save the modified image to the specified name and path.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The modified image to be saved.
    path : :obj:`pathlib.Path`
        The directory into which output shall be placed.
    name : :obj:`pathlib.Path`
        The name under which the image shall be saved.
    force : bool
        Whether to raise exceptions in the case of file conflicts.

    """
    logger.debug("Entering 'save_output'.")
    logger.debug(f"Parameter values: {locals()}")
    full_path = path / name
    if full_path.exists():
        logger.debug("Conflict found.")
        if force:
            logger.debug("Force was specified so ignoring conflict.")
            image.save(full_path)
        else:
            logger.debug("Force was not specified so exiting due to conflict.")
            logger.error(
                f"The path '{full_path}' already exists. "
                "Use '--force' if you would like to overwrite it."
            )
            raise FileExistsError
    else:
        logger.debug("No conflict found.")
        image.save(full_path)


def set_up_output(path: Path, filename: Path) -> Tuple[Path, Path]:
    """Set the path to the output and base filename to use.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The output argument specified by the user.
    filename : :obj:`pathlib.Path`
        The path to an input image file.

    Returns
    -------
    out_path : :obj:`pathlib.Path`
        The directory in which output should be placed.
    out_filename : :obj:`pathlib.Path`
        The unmodified name of the file to output.

    Notes
    -----
    The default location for output is always the current working
    directory.

    """
    logger.debug("Entering 'set_up_output'.")
    logger.debug(f"Parameter values: {locals()}")
    if path is None:
        out_path = Path.cwd()
        out_filename = Path(filename.stem + filename.suffix.lower())
    elif path.suffix == "":
        out_path = path
        out_path.mkdir(parents=True, exist_ok=True)
        out_filename = Path(filename.stem + filename.suffix.lower())
    else:
        out_path = path.parent
        out_path.mkdir(parents=True, exist_ok=True)
        out_filename = Path(path.name)
    logger.debug(f"Output path is '{out_path}'. Filename is '{out_filename}'.")
    return (out_path, out_filename)
