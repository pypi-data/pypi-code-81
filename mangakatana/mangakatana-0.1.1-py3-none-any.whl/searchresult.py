import functools as ft

from mangakatana import utils


class SearchResult:
	def __init__(self, soup):
		self._soup 		= soup
		self._page_soup = None

	@ft.cached_property
	def title(self) -> str: return self._soup.find("h3", class_="title").find("a").text

	@ft.cached_property
	def status(self) -> str: return self._soup.find("div", class_="status completed uk-hidden-small").text.strip()

	@ft.cached_property
	def url(self) -> str: return self._soup.find("h3", class_="title").find("a")["href"]

	@ft.lru_cache()
	def chapter_list(self): return utils.chapters_from_url(self.url)
