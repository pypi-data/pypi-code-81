import requests

from bs4 import BeautifulSoup

from mangakatana.chapter import Chapter


def chapters_from_url(url: str):
	page_soup = BeautifulSoup(requests.get(url=url).content, "html.parser")

	return [Chapter(tr) for tr in page_soup.find_all("tr")][::-1]
