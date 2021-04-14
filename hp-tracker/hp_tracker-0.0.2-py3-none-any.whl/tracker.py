import requests
from bs4 import BeautifulSoup

from hp_tracker.exceptions import TrackingNetworkError, TrackingStatusError


class HPTracker:
    """Main tracking class."""

    def __init__(self):
        self.base_url = "https://posiljka.posta.hr/tracking/trackingdata"
        self.target = "event__status__item-content d-flex flex-column justify-content-center align-content-start"
        self.allowed_classes = [
            "mr-5 mb-2 Text-Style-20-md-6",
            "mr-5 mb-2 text-style-19-md-12",
            "text-style-52-md-4",
        ]

    def track(self, track_no):
        return self._get_response(track_no)

    def _get_response(self, track_no):
        param = {"barcode": track_no}

        try:
            page = requests.get(self.base_url, params=param)
        except requests.exceptions.RequestException:
            raise TrackingNetworkError

        soup = BeautifulSoup(page.content, "html.parser")
        target = soup.find("div", class_=self.target)

        if not target:
            raise TrackingStatusError(track_no)

        track_status = {}
        times = []
        events = []
        for list_element in soup.find_all(
            "div", class_="col-6 col-lg-4 d-flex flex-column justify-content-start"
        ):
            elements = [
                e
                for e in list(list_element.children)
                if any(x in str(e) for x in self.allowed_classes)
            ]
            if len(elements) < 1:
                continue
            time_text = " - ".join([el.get_text() for el in elements])
            time = " ".join(
                time_text.replace("\n", "")
                .replace("\t", "")
                .replace("\r", "")
                .strip()
                .split()
            )
            times.append(time)

        for list_element in soup.find_all(
            "div", class_="col-6 col-lg-8 d-flex flex-column justify-content-start"
        ):
            elements = [
                e
                for e in list(list_element.children)
                if any(x in str(e) for x in self.allowed_classes)
            ]
            if len(elements) < 1:
                continue
            event_text = " - ".join([el.get_text() for el in elements])
            event = " ".join(
                event_text.replace("\n", "")
                .replace("\t", "")
                .replace("\r", "")
                .strip()
                .split()
            )
            events.append(event)

        i_len = min(len(times), len(events))
        for i in range(i_len):
            track_status[times[i]] = events[i]

        return track_status
