from olxbrasil.parsers.base import OlxBaseParser
from olxbrasil.utils import format_price


class ItemParser(OlxBaseParser):
    @property
    def title(self) -> str:
        return self.ad_data["subject"].strip()

    @property
    def price(self) -> float:
        return format_price(self.ad_data["price"])

    @property
    def seller(self) -> str:
        return self.ad_data["user"]["name"].strip()

    @property
    def description(self) -> str:
        return self.ad_data["description"].replace("<br>", "\n").strip()

    @property
    def phone(self) -> str:
        return self.ad_data["phone"]["phone"].strip()

    @property
    def location(self) -> dict:
        return self.ad_data["location"]

    @property
    def properties(self) -> dict:
        car_properties = {}
        for item in self.ad_data["properties"]:
            car_properties[item["name"]] = item["value"]
        return car_properties
