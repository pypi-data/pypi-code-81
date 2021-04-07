from bs4 import BeautifulSoup
from tghtml import tghtml

from .aioget import aioget


async def page(name):
    text = await aioget(f"https://memepedia.ru/{name}/")
    parsed = tghtml(text, [
        ["section"],
        ["ul"], ["ol"], ["li"],
        ["div", {"class": "mistape_caption"}]
    ])

    soup = BeautifulSoup(text, "lxml")

    try:
        image = soup.find_all("figure", {"class": "s-post-media-img"})[0].img["src"]
    except IndexError:
        image = ""

    return [image, parsed.replace("•", "")]
