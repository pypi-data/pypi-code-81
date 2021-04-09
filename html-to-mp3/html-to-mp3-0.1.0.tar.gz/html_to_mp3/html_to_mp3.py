import os
import tempfile
import re
import random
from typing import Optional

# These packages are conveniences.
# Listing builtin packages that will require a few more lines to use
import click  # Alt. argparse
import requests  # Alt. urllib.request
from bs4 import BeautifulSoup  # Alt. html.parser


def text_to_mp3(text: str, outfile: str) -> None:
    """Given some text, generate an mp3 speaking the text.

    Args:
        text (str): Text to speak
        outfile (str): *.mp3 file to write
    """

    # For some reason espeak doesn't find NamedTemporaryFile files to be agreeable...
    _, text_filename = tempfile.mkstemp(suffix=".txt")

    with open(text_filename, "w") as file:
        file.write(text)
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as wav_file:
            os.system(f"espeak -f {text_filename} -w {wav_file.name}")
            os.system(f"lame --preset insane {wav_file.name} {outfile} --silent")
    finally:
        if os.path.exists(text_filename):
            os.remove(text_filename)


def html_to_mp3(html: str, outfile: str, select: str = "body") -> None:
    """Given a string containing html, generate an *.mp3 that speaks the text.

    Args:
        html (str): HTML string
        outfile (str): *.mp3 to generate
        select (str, optional): CSS selector from which to select text. Defaults to "body".

    Raises:
        ValueError: In case the CSS selector is not present in the text.
    """
    soup = BeautifulSoup(html, features="html.parser")
    elements = soup.select(select)
    if not elements:
        raise ValueError(f"No elements found for CSS selector `{select}`")
    text = "\n".join([element.get_text() for element in elements])
    text_to_mp3(text, outfile)


def filename_from_html_title(html: str, suffix: str = "") -> None:
    soup = BeautifulSoup(html, features="html.parser")
    txt = soup.title or soup.h1 or soup.h2 or soup.h3
    filename = re.sub("[^a-zA-Z\s]", "", txt.get_text()).lower().replace(" ", "-") + suffix
    return filename


@click.group()
def html2mp3():
    """Converts text in html to mp3 file"""
    pass


@html2mp3.command(name="file")
@click.argument(
    "infile",
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.argument(
    "outfile",
    type=click.Path(exists=False, dir_okay=False, writable=True),
)
@click.option("-s", "--select", default="body", help="CSS selector for text to use.")
def cli_html_to_mp3(infile: str, outfile: str, select: str):
    """Given an html file, output an mp3 of the text."""

    with open(infile, "r") as file:
        html = file.read()

    html_to_mp3(html, outfile, select)


@html2mp3.command(name="url")
@click.argument("url", type=click.STRING)
@click.option(
    "-o",
    "--outfile",
    default=None,
    type=click.Path(exists=False, dir_okay=False, writable=True),
    help="Output filenme",
)
@click.option("-s", "--select", default="body", help="CSS selector for text to use.")
@click.option("-q", "--quiet", default=False, help="Do not display output information.")
def cli_url_to_mp3(url: str, outfile: Optional[str], select: str, quiet: bool):
    """Given a URL, extract the text and generate a recording."""
    r = requests.get(url)
    r.raise_for_status()

    html = r.text
    if not outfile:
        outfile = filename_from_html_title(html, ".mp3")
    html_to_mp3(html, outfile, select)

    if not quiet:
        click.echo(f"Wrote text to {outfile}")
