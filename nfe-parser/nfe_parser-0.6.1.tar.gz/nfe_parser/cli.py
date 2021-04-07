"""Console script for nfe_parser."""
import argparse
import pathlib
import sys
import textwrap
import time
from urllib.parse import urlparse

import cv2
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar

from nfe_parser import nfe, nfe_parser


def parse_args():
    description = textwrap.dedent(
        """
        nfe-parser v0.6.1 -- is a simple lib/cli for parsing brazillian nfe
        (Nota Fiscal Eletronica). It can parse both local html files or urls.
        For full documentation check the repo:
        https://github.com/gmagno/nfe-parser
    """
    )

    epilog = r"""
                    /######
                   /##__  ##
         /####### | ##  \__//######           /######   /######   /######   /#######  /######   /######
        | ##__  ##| ####   /##__  ## /###### /##__  ## |____  ## /##__  ## /##_____/ /##__  ## /##__  ##
        | ##  \ ##| ##_/  | ########|______/| ##  \ ##  /#######| ##  \__/|  ###### | ########| ##  \__/
        | ##  | ##| ##    | ##_____/        | ##  | ## /##__  ##| ##       \____  ##| ##_____/| ##
        | ##  | ##| ##    |  #######        | #######/|  #######| ##       /#######/|  #######| ##
        |__/  |__/|__/     \_______/        | ##____/  \_______/|__/      |_______/  \_______/|__/
                                            | ##
                                            | ##
                                            |__/
    """

    epilog += textwrap.dedent(
        """
        return:
            %(prog)s prints a table with the nfe data.

        examples:
            $ %(prog)s http://example.com/path/to/nfe.html

            ┌─────────────────────────────────── NFC-e ───────────────────────────────────┐
            │           1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234            │
            │                              NFC-e no. 123456                               │
            │                     Emission date: 1970-01-01 00:00:00                      │
            │                       Auth. protocol: 123456789012345                       │
            │ ╭──────────────────────────────── Company ────────────────────────────────╮ │
            │ │                        CNPJ: 12.345.678/9012-34                         │ │
            │ │                     State Registration: 1090362886                      │ │
            │ │               1640 Riverside Drive, Hill Valley, California             │ │
            │ ╰─────────────────────────────────────────────────────────────────────────╯ │
            │ ╭─────────────────────────────── Consumer ────────────────────────────────╮ │
            │ │                           CPF: 123.456.789-99                           │ │
            │ ╰─────────────────────────────────────────────────────────────────────────╯ │
            │ ╭─────────────────────────────── Products ────────────────────────────────╮ │
            │ │                                                                         │ │
            │ │   Code       Description             Qty    Unit   Val/unit   Partial   │ │
            │ │  ─────────────────────────────────────────────────────────────────────  │ │
            │ │   12345678    Hover Board            1.0     UN        1000      1000   │ │
            │ │   98765432     DeLorean              1.0     UN        5000      5000   │ │
            │ │                                                                         │ │
            │ │                                                           Total: 6000.0 │ │
            │ │                                                           Discount: 0.0 │ │
            │ ╰─────────────────────────────────────────────────────────────────────────╯ │
            └─────────────────────────────────────────────────────────────────────────────┘


        copyright:
            Copyright © 2020 Gonçalo Magno <goncalo.magno@gmail.com>
            This software is licensed under the MIT License.
    """
    )
    parser = argparse.ArgumentParser(
        prog="nfe-parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog,
    )
    parser.add_argument(
        "-v",
        "--version",
        required=False,
        action="store_true",
        help="shows %(prog)s version",
    )

    parser.add_argument(
        "-c",
        "--camera",
        required=False,
        action="store_true",
        help="reads qr-codes from camera",
    )

    parser.add_argument(
        "uris",
        metavar="URIs",
        nargs=argparse.REMAINDER,
        help=(
            "URI or list of URIs pointing to NFE. Valid examples: "
            "http://path/to/nfe, file:///example.com/path/to/nfe.html, "
            "/path/to/nfe.html."
        ),
    )

    args = vars(parser.parse_args())
    return args


def read_nfe_from_uri(uri):
    parts = urlparse(uri)
    if parts.scheme == "":  # assume it's a path to a file
        if not pathlib.Path(parts.path).is_file():
            print(
                "ERROR: the url must be a valid url or path to an existing "
                "file"
            )
            sys.exit(1)
        try:
            n = nfe_parser.parse_nfe_from_file(pathlib.Path(parts.path))
        except ValueError as e:
            print(f"ERROR: failed to parse the file with error: '{e}'")
            sys.exit(1)
    else:  # assume it's a valid url
        try:
            n = nfe_parser.parse_nfe_from_url(uri)
        except (nfe_parser.RequestFailedError, nfe_parser.ParseError) as e:
            print(f"ERROR: failed to parse the file with error: '{e}'")
            sys.exit(1)
    return n


def read_nfe_from_camera():
    print("Starting capture, press 'q' or 'ESC' to exit...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    csv = open("camera_nfes.txt", "w")
    found = set()
    while True:
        frame = vs.read()  # grab frame
        frame = imutils.resize(frame, width=400)  # resize it to 400px width

        barcodes = pyzbar.decode(frame)  # find barcodes in the image

        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(
                frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                csv.write("{}\n".format(barcodeData))
                csv.flush()
                found.add(barcodeData)

        # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        if key in [ord("q"), 27]:
            break

    # close the output CSV file do a bit of cleanup
    print("Terminating...")
    time.sleep(1)
    csv.close()
    time.sleep(1)
    cv2.destroyAllWindows()
    time.sleep(1)
    vs.stop()
    time.sleep(1)
    print("Terminated!")


def main():
    """Console script for nfe_parser."""

    kwargs = parse_args()
    if kwargs["version"]:
        print("nfe-parser v0.6.1")
        return 0

    if kwargs["camera"]:
        n = read_nfe_from_camera()
        # nfe.print(n)
        return 0

    if not kwargs["uris"]:
        print("ERROR: missing argument uris argument.")
        return 1

    for uri in kwargs["uris"]:
        n = read_nfe_from_uri(uri)
        nfe.print(n)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
