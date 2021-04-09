"""Execute the application.

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
from typing import List, Optional
import sys

from PIL import Image

from pyimgutil import arguments, check, commands


logger = logging.getLogger(__name__)


def main(argv: Optional[List[str]] = None) -> None:
    logger.debug("Entering 'main'.")
    logger.debug(f"Parameter values: {locals()}")
    # Parse args only enough to determine user's logging preference.
    quickparser = arguments.QuickParser()
    preliminary_args = quickparser.parse_args(argv)
    arguments.configure_logging(preliminary_args)

    logger.info("Starting pyimgutil.")
    logger.info("Parsing the provided arguments.")
    formalparser = arguments.FormalParser()
    parsed_args = formalparser.parse_args(argv)
    logger.info("Validating the provided arguments.")
    try:
        check.check_arguments(parsed_args)
    except ValueError:
        sys.exit()

    logger.info("Retrieving files to be processed.")
    files = commands.get_input_files(parsed_args.input)
    for file in files:
        logger.info(f"Processing: {file}")
        if parsed_args.command == "crop":
            logger.info("Cropping image.")
            box = (
                parsed_args.left,
                parsed_args.upper,
                parsed_args.right,
                parsed_args.bottom,
            )
            modified_image = commands.crop_image(
                Image.open(file),
                box,
            )
        if parsed_args.command == "resize":
            logger.info("Resizing image.")
            modified_image = commands.resize_image(
                Image.open(file),
                parsed_args.width,
                parsed_args.height,
                parsed_args.ratio,
                parsed_args.scale,
            )

        logger.info("Determining output location and name.")
        out_path, out_filename = commands.set_up_output(
            parsed_args.output,
            file,
        )
        if parsed_args.prepend:
            out_filename = commands.attach_message(
                out_filename,
                parsed_args.prepend,
                0,
            )
        if parsed_args.append:
            out_filename = commands.attach_message(
                out_filename,
                parsed_args.append,
                1,
            )

        logger.info(f"File will be saved as '{out_filename}' to '{out_path}'.")
        logger.info("Saving image.")
        try:
            commands.save_output(
                modified_image,
                out_path,
                out_filename,
                parsed_args.force,
            )
        except FileExistsError:
            sys.exit()
    logger.info("Exiting pyimgutil.")


if __name__ == "__main__":
    main()
