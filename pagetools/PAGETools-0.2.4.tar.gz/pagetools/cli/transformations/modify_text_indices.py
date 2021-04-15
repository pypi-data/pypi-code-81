from pagetools.src.Page import Page

from typing import List

import click
from lxml import etree


@click.command("change-text-index", help="Change the text indices of text content.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-m", "--move", multiple=True, nargs=2, required=True)
def change_text_index(xmls, move):
    for xml in xmls:
        page = Page(xml)

        text_regions = page.get_text_regions()
        move_texts(text_regions, move)

        for text_region in text_regions:
            textlines = text_region.findall("./page:TextLine", namespaces=page.get_ns())
            move_texts(textlines, move)


def move_texts(elems: List[etree.Element], rules: List[tuple]):
    for elem in elems:
        print(elem.get("index"))
