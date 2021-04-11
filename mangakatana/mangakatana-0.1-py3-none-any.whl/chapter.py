import re
import functools as ft


class Chapter:
	def __init__(self, soup):
		self._soup = soup

	@ft.cached_property
	def title(self): return self._soup.find("a").text

	@ft.cached_property
	def url(self): return self._soup.find("a")["href"]

	@ft.cached_property
	def num(self): return float(re.search("[0-9]+", self.title).group())
