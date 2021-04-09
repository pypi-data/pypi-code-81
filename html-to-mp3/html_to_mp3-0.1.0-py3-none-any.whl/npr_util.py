"""Utils for NPR examples.
"""
import requests
from bs4 import BeautifulSoup  # Alt. html.parser

NPR_URL = "https://text.npr.org"


def get_npr_frontpage_links() -> list[str]:
    r = requests.get(NPR_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text)
    s = soup.select("div.topic-container > ul > li > a")

    return [f"https://text.npr.org/{link.attrs['href']}" for link in s]


def npr_sample_call() -> None:
    links = get_npr_frontpage_links()

    script = " \\\\\n\t & ".join(
        [f'html2mp3 url {link} --select ".paragraphs-container"' for link in links]
    )

    print(script)
