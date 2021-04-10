import json


class OlxBaseParser:
    def __init__(self, soup):
        self.soup = soup
        self.initial_data = self.__get_initial_data()
        self.ad_data = self._get_ad_data()

    def __iter__(self):
        for item in dir(self):
            attr = getattr(self, item)
            if (
                not item.startswith("_")
                and item
                not in (
                    "initial_data",
                    "ad_data",
                    "soup",
                )
                and not callable(attr)
            ):
                yield item, getattr(self, item)

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            return None

    def _get_ad_data(self) -> dict:
        return self.initial_data.get("ad", {})

    def __get_initial_data(self) -> dict:
        tag = "script"
        options = {"id": "initial-data"}
        key = "data-json"
        return json.loads(self.soup.find(tag, options)[key])
