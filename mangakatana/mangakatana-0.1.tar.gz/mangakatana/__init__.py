from bs4 import BeautifulSoup

from mangakatana import utils as _utils
from mangakatana import siterequests as _siterequests

from mangakatana.searchresult import SearchResult


def search(*, title: str):
	r = _siterequests.search(title=title)

	soup = BeautifulSoup(r.content, "html.parser")

	entries = soup.find_all("div", class_="item")

	return [SearchResult(e) for e in entries]


def chapter_list(*, url: str):
	return _utils.chapters_from_url(url)

