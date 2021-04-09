"""Parse and handle command-line arguments.

Typical usage of this module involves using QuickParser to determine
logging preferences, set the the logging preferences with the
configure_logging function, and then perform the complete argument
parsing with FormalParser.

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
import sys
import textwrap
from typing import List, Optional

import pyimgutil


logger = logging.getLogger(__name__)


class FormalParser():
    """Command-line arguments parser.

    This parser handles all of the options provided to the user as well
    as checking for options that cause conflicts.

    Attributes
    ----------
    None

    Methods
    -------
    __init__()
        Construct a parser.
    parse_arguments(args)
        Parse the given arguments into a Namespace object.

    """
    def __init__(self) -> None:
        """Construct a parser.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self._logger = logging.getLogger(
            __name__ + "." + f"{self.__class__.__name__}"
        )
        self._logger.debug(f"Creating {self.__class__.__name__} object.")
        self._parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description=(
                textwrap.dedent(
                    """\
                    Perform simple image processing.

                    Supported image formats: BMP, GIF, ICO, JPEG, PNG, PPM
                    """
                )
            ),
            epilog=(
                textwrap.dedent(
                    """\
                    pyimgutil copyright (C) 2021 emerac

                    This program comes with ABSOLUTELY NO WARRANTY. This is
                    free software, and you are welcome to redistribute it
                    under certain conditions.

                    You should have received a copy of the GNU General Public
                    License along with this program.  If not, see:
                    <https://www.gnu.org/licenses/gpl-3.0.txt>.
                    """
                )
            ),
        )
        group_1 = self._parser.add_mutually_exclusive_group()
        group_1.add_argument(
            "-q",
            "--quiet",
            help=(
                textwrap.dedent(
                    """\
                    suppress all log output
                    """
                )
            ),
            action="store_true",
        )
        group_1.add_argument(
            "-v",
            "--verbose",
            help=(
                textwrap.dedent(
                    """\
                    increase log output verbosity (default=CRITICAL)
                    This option is repeatable.
                    (-v=ERROR, -vv=WARNING, -vvv=INFO, -vvvv=DEBUG)
                    """
                )
            ),
            action="count",
            default=0,
        )
        # Methods will be used to add individual commands to subparsers.
        self._subparsers = self._parser.add_subparsers(
            help=(
                textwrap.dedent(
                    """\
                    command to perform on image(s)
                    Run `%(prog)s [command] -h` to view the help
                    for that command.
                    """
                )
            ),
            dest="command",
        )
        self._add_crop_subparser()
        self._add_resize_subparser()

    def parse_args(
        self,
        args: Optional[List[str]] = None,
    ) -> argparse.Namespace:
        """Parse the given arguments into a Namespace object.

        Parameters
        ----------
        args : list, optional
            The arguments to parse.

        Returns
        -------
        parsed_args : :obj:`argparse.Namespace`
            A Namespace object that contains the parsed arguments.

        Notes
        -----
        The parse_args method of the argparse module will parse the
        arguments that are passed to it. If nothing is passed to it,
        it will simply read from sys.argv.

        """
        self._logger.debug("Entering 'parse_args' (formal).")
        self._logger.debug(f"Parameter values: {locals()}")
        self._logger.debug(f"Args via sys.argv: {sys.argv[1:]}")
        if args is None and len(sys.argv[1:]) == 0:
            self._logger.error(
                "Exiting the program because no arguments were given."
            )
            print("For help on using pyimgutil, run `pyimgutil -h`.")
            sys.exit()
        parsed_args = self._parser.parse_args(args)

        try:
            self._check_for_resize_arg_conflict(parsed_args)
        except ResizeRatioError:
            self._logger.critical("A ResizeRatioError exception occurred.")
            print(
                textwrap.dedent(
                    """\
                    pyimgutil: resize: error:
                    --width, --height, and --ratio cannot all be used together

                    If both the width and height are specified, the aspect
                    ratio must change.\
                    """
                )
            )
            sys.exit()
        except ResizeScaleError:
            self._logger.critical("A ResizeScaleError exception occurred.")
            print(
                textwrap.dedent(
                    """\
                    pyimgutil: resize: error:
                    --width/--height, and --scale cannot be used together

                    If either the width or height are specified, the aspect
                    ratio must change.\
                    """
                )
            )
            sys.exit()

        self._logger.debug(f"Parsed args: {parsed_args}")
        return parsed_args

    def _add_crop_subparser(self) -> None:
        self._logger.debug("Adding crop subparser.")
        crop_subparser = self._subparsers.add_parser(
            "crop",
            formatter_class=argparse.RawTextHelpFormatter,
            help=(
                textwrap.dedent(
                    """\
                    remove unwanted outer areas from an image
                    """
                )
            ),
            description=(
                textwrap.dedent(
                    """\
                    Remove unwanted outer areas from an image

                    If no output path is specified, processed files are
                    placed in the current working directory.
                    """
                )
            ),
        )
        crop_subparser.add_argument(
            "input",
            help=(
                textwrap.dedent(
                    """\
                    the path to the file(s) to process
                    If a directory is given, only image files that are of
                    supported formats will be processed.
                    """
                )
            ),
            type=Path,
        )
        crop_subparser.add_argument(
            "-l",
            "--left",
            help=(
                textwrap.dedent(
                    """\
                    the pixel coordinate marking the left boundary of the
                    crop box
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        crop_subparser.add_argument(
            "-u",
            "--upper",
            help=(
                textwrap.dedent(
                    """\
                    the pixel coordinate marking the upper boundary of the
                    crop box
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        crop_subparser.add_argument(
            "-r",
            "--right",
            help=(
                textwrap.dedent(
                    """\
                    the pixel coordinate marking the right boundary of the
                    crop box
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        crop_subparser.add_argument(
            "-b",
            "--bottom",
            help=(
                textwrap.dedent(
                    """\
                    the pixel coordinate marking the bottom boundary of the
                    crop box
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        crop_subparser.add_argument(
            "-o",
            "--output",
            help=(
                textwrap.dedent(
                    """\
                    the directory where processed files shall be placed
                    If the output path would result in a file being
                    overwritten, the program will exit to prevent files
                    from being accidentally overwritten. Use the force option
                    to override this protection.
                    """
                )
            ),
            type=Path,
            metavar="PATH",
        )
        crop_subparser.add_argument(
            "-a",
            "--append",
            help=(
                textwrap.dedent(
                    """\
                    append a custom message to the processed image's filename
                    """
                )
            ),
            metavar="MESSAGE",
        )
        crop_subparser.add_argument(
            "-p",
            "--prepend",
            help=(
                textwrap.dedent(
                    """\
                    prepend a custom message to the processed image's filename
                    """
                )
            ),
            metavar="MESSAGE",
        )
        crop_subparser.add_argument(
            "-f",
            "--force",
            help=(
                textwrap.dedent(
                    """\
                    allow processed images to overwrite the original file
                    """
                )
            ),
            action="store_true",
        )

    def _add_resize_subparser(self) -> None:
        self._logger.debug("Adding resize subparser.")
        resize_subparser = self._subparsers.add_parser(
            "resize",
            formatter_class=argparse.RawTextHelpFormatter,
            help=(
                textwrap.dedent(
                    """\
                    resize an image
                    """
                )
            ),
            description=(
                textwrap.dedent(
                    """\
                    Resize an image.

                    If no output path is specified, processed files are
                    placed in the current working directory.
                    """
                )
            ),
        )
        resize_subparser.add_argument(
            "input",
            help=(
                textwrap.dedent(
                    """\
                    the path to the file(s) to process
                    If a directory is given, only image files that are of
                    supported formats will be processed.
                    """
                )
            ),
            type=Path,
        )
        resize_subparser.add_argument(
            "--height",
            help=(
                textwrap.dedent(
                    """\
                    the new image's height in pixels
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        resize_subparser.add_argument(
            "--width",
            help=(
                textwrap.dedent(
                    """\
                    the new image's width in pixels
                    """
                )
            ),
            metavar="PIXEL",
            type=int,
        )
        resize_subparser.add_argument(
            "-r",
            "--ratio",
            help=(
                textwrap.dedent(
                    """\
                    maintain the image's original aspect ratio
                    """
                )
            ),
            action="store_true",
        )
        resize_subparser.add_argument(
            "-s",
            "--scale",
            help=(
                textwrap.dedent(
                    """\
                    scale the image's dimensions by a factor while maintaining
                    its original aspect ratio
                    For example: 1.0 = original, 2.0 = dimensions are doubled,
                    0.71 = dimensions are 71%% of the original dimensions, etc.
                    """
                )
            ),
            metavar="FACTOR",
            type=float,
        )
        resize_subparser.add_argument(
            "-o",
            "--output",
            help=(
                textwrap.dedent(
                    """\
                    the directory where processed files shall be placed
                    If the output path would result in a file being
                    overwritten, the program will exit to prevent files
                    from being accidentally overwritten. Use the force option
                    to override this protection.
                    """
                )
            ),
            type=Path,
            metavar="PATH",
        )
        resize_subparser.add_argument(
            "-a",
            "--append",
            help=(
                textwrap.dedent(
                    """\
                    append a custom message to the processed image's filename
                    """
                )
            ),
            metavar="MESSAGE",
        )
        resize_subparser.add_argument(
            "-p",
            "--prepend",
            help=(
                textwrap.dedent(
                    """\
                    prepend a custom message to the processed image's filename
                    """
                )
            ),
            metavar="MESSAGE",
        )
        resize_subparser.add_argument(
            "-f",
            "--force",
            help=(
                textwrap.dedent(
                    """\
                    allow processed images to overwrite the original file
                    """
                )
            ),
            action="store_true",
        )

    def _check_for_resize_arg_conflict(
        self,
        args: argparse.Namespace,
    ) -> None:
        """Check the parsed arguments for conflicting resize args.

        While the argparse module does have mutually exclusive groups,
        they do not have much flexibility. These situations need to be
        handled manually:

        --width --height --ratio
        All three cannot be used together, but any combination of the
        three is allowed.

        --width --height --scale
        Scale cannot be used with width or height.

        """
        logger.debug("Checking if the resize commmand was used.")
        if args.command == "resize":
            logger.debug("Checking arguments for 'resize' command conflicts.")
            if args.height and args.width and args.ratio:
                logger.error("Argument conflict found involving 'ratio'.")
                raise ResizeRatioError
            elif (args.height or args.width) and args.scale:
                logger.error("Argument conflict found involving 'scale'.")
                raise ResizeScaleError
            logger.debug("No resize command conflicts found.")


class QuickParser():
    """Simplified parser for quickly determining user preferences.

    This parser only accepts 'quiet' and 'verbose' options and will
    not error or raise any exceptions. Its purpose is to parse for
    logging arguments so that the logger can be configured straight
    away.

    Attributes
    ----------
    None

    Methods
    -------
    __init__()
        Construct a parser.
    parse_arguments(args)
        Parse the given arguments into a Namespace object.

    """
    def __init__(self) -> None:
        """Construct a parser.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self._logger = logging.getLogger(
            __name__ + "." + f"{self.__class__.__name__}"
        )
        self._logger.debug(f"Creating {self.__class__.__name__} object.")
        self._parser = argparse.ArgumentParser(add_help=False)
        self._parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
        )
        self._parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
        )

    def parse_args(
        self,
        args: Optional[List[str]] = None,
    ) -> argparse.Namespace:
        """Parse the given arguments into a Namespace object.

        Parameters
        ----------
        args : list, optional
            The arguments to parse.

        Returns
        -------
        parsed_args : :obj:`argparse.Namespace`
            A Namespace object that contains the parsed known arguments.

        Notes
        -----
        The parse_args method of the argparse module will parse the
        arguments that are passed to it. If None is passed, it will
        simply read from sys.argv.

        """
        self._logger.debug("Entering 'parse_args' (quick).")
        self._logger.debug(f"Parameter values: {locals()}")
        self._logger.debug(f"Args via sys.argv: {sys.argv[1:]}")
        known_args, unknown_args = self._parser.parse_known_args(args)
        self._logger.debug(f"Parsed known args: {known_args}")
        return known_args


class ResizeRatioError(Exception):
    """Custom exception for the 'resize' command-line argument.

    Attributes
    ----------
    None

    Methods
    -------
    None

    """
    pass


class ResizeScaleError(Exception):
    """Custom exception for the 'resize' command-line argument.

    Attributes
    ----------
    None

    Methods
    -------
    None

    """
    pass


def configure_logging(args: argparse.Namespace) -> None:
    """Set the logging level and handler based on user preference.

    Parameters
    ----------
    args : :obj:`argparse.Namespace`
        Arguments that have been parsed by the argparse parser.

    Returns
    -------
    None

    Notes
    -----
    The arguments that this function receives have not been checked for
    conflicts. Therefore, if both quiet mode and verbose mode are set,
    quiet mode will be allowed to take precendence. When formal
    parsing occurs, this conflict will raise an exception.

    """
    logger.debug("Entering 'configure_logging'.")
    logger.debug(f"Parameter values: {locals()}")
    if not args.quiet:
        logger.debug(f"Handler will be set to: {pyimgutil.stream_handler}")
        pyimgutil.logger.addHandler(pyimgutil.stream_handler)
        if args.verbose == 0:
            logger.debug(f"Level will be set to: {logging.CRITICAL}")
            pyimgutil.logger.setLevel(logging.CRITICAL)
        elif args.verbose == 1:
            logger.debug(f"Level will be set to: {logging.ERROR}")
            pyimgutil.logger.setLevel(logging.ERROR)
        elif args.verbose == 2:
            logger.debug(f"Level will be set to: {logging.WARNING}")
            pyimgutil.logger.setLevel(logging.WARNING)
        elif args.verbose == 3:
            logger.debug(f"Level will be set to: {logging.INFO}")
            pyimgutil.logger.setLevel(logging.INFO)
        elif args.verbose >= 4:
            logger.debug(f"Level will be set to: {logging.DEBUG}")
            pyimgutil.logger.setLevel(logging.DEBUG)
    else:
        logger.debug(f"Handler will be set to: {pyimgutil.null_handler}")
        pyimgutil.logger.addHandler(pyimgutil.null_handler)
    logger.debug(f"Handlers: {pyimgutil.logger.handlers}")
    logger.debug(f"Level: {pyimgutil.logger.level}")
