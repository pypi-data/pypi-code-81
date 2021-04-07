import logging

from datetime import datetime

icon_static_url = "http://openweathermap.org/img/wn/{}@2x.png"


class Weather:
    def __init__(self, d):
        self.time = datetime.fromtimestamp(d["dt"])
        self.pressure = d["pressure"]
        self.humidity = d["humidity"]
        self.clouds = d["clouds"]
        self.wind_speed = d["wind_speed"]

        conditions = [Condition(condition) for condition in d["weather"]]
        if len(conditions) > 1:
            logging.warning(
                "Multiple conditions for %s weather: %s",
                self.time,
                d["weather"],
            )

        self.condition = conditions[0]

    def __str__(self):
        return "{} ({}°C) at {}".format(
            self.condition.description, self.temperature, self.time
        )

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.__dict__)


class CurrentWeather(Weather):
    def __init__(self, d):
        super().__init__(d)
        self.sunrise = datetime.fromtimestamp(d["sunrise"])
        self.sunset = datetime.fromtimestamp(d["sunset"])
        self.temperature = d["temp"]
        self.feels_like = d["feels_like"]


class HourlyWeather(Weather):
    def __init__(self, d):
        super().__init__(d)
        self.temperature = d["temp"]
        self.feels_like = d["feels_like"]


class DailyWeather(Weather):
    def __init__(self, d):
        super().__init__(d)
        self.sunrise = datetime.fromtimestamp(d["sunrise"])
        self.sunset = datetime.fromtimestamp(d["sunset"])
        self.temperature = DailyTemperature(d["temp"])
        self.feels_like = DailyFeelsLike(d["feels_like"])
        self.pop = d["pop"]


class DictClass:
    def __init__(self, d):
        self.__dict__.update(d)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.__dict__)


class DailyTemperature(DictClass):
    pass


class DailyFeelsLike(DictClass):
    pass


class Condition:
    def __init__(self, condition_json):
        self.id = condition_json["id"]
        self.group = condition_json["main"]
        self.description = condition_json["description"].title()
        self.icon_id = condition_json["icon"]
        self.icon_url = icon_static_url.format(self.icon_id)

    def __repr__(self):
        return str(self.__dict__)
