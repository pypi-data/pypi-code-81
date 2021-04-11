
import requests

_ROOT_URL = "http://mangakatana.com/"


def search(*, title: str):
	return requests.get(f"{_ROOT_URL}?search={title}&search_by=book_name")
