from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import md5
from typing import Optional

import httpx

import models
from errors import AuthError, LoginFormError

_DEFINITIONS = {
    "cid": "Страна",
    "sid": "Регион",
    "pid": "Городской округ / Муниципальный район",
    "cn": "Населённый пункт",
    "sft": "Тип ОО",
    "scid": "Образовательная организация",
}

_WEBAPI_BASE_URL = "https://sgo.volganet.ru/webapi"


class Client:
    def __init__(self, state, province, city, func, school_name, user_name, password):
        self.http = httpx.Client(
            base_url=_WEBAPI_BASE_URL, headers={"referer": _WEBAPI_BASE_URL}
        )
        self.school = School(state, province, city, func, school_name)
        self.user_name = user_name
        self.password = password
        self._user_id = None
        self._year_id = None

    def get_diary(
        self, week_start: Optional[date] = None, week_end: Optional[date] = None
    ) -> models.Diary:
        if not week_start:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
        if not week_end:
            week_end = week_start + timedelta(days=5)

        responce = self.http.get(
            "student/diary",
            params={
                "weekStart": week_start.isoformat(),
                "weekEnd": week_end.isoformat(),
                "studentId": self._user_id,
                "yearId": self._year_id,
            },
        )
        return models.Diary.parse_raw(responce.text)

    def get_announcements(self, take: Optional[int] = -1) -> models.Announcements:
        responce = self.http.get("announcements", params={"take": take})
        return models.Announcements.parse_raw(responce.text)

    def get_details(self, assignment: models.Assignment):
        responce = self.http.get(f"student/diary/assigns/{assignment.id}")
        return models.DetailedAssignment.parse_raw(responce.text)

    def get_attachments(
        self, assignments: list[models.Assignment]
    ) -> models.Attachments:
        responce = self.http.post(
            "student/diary/get-attachments",
            params={"studentId": self._user_id},
            json={"assignId": [a.id for a in assignments]},
        )
        return models.Attachments.parse_raw(responce.text)

    def login(self):
        login_form = {"cid": self.http.get("prepareloginform").json()["cid"]}
        queue = list(_DEFINITIONS.keys())
        queue = dict(zip(queue[:-1], queue[1:]))
        for last_name, school_item in zip(queue, self.school):
            form = self.http.get(
                "loginform", params={**login_form, "lastname": last_name}
            ).json()
            name = queue[last_name]

            for item in form["items"]:
                if item["name"] == school_item:
                    login_form[name] = item["id"]
                    break
            else:
                raise LoginFormError(school_item, _DEFINITIONS[name], form["items"])

        responce = self.http.post("auth/getdata")
        self.http.cookies.extract_cookies(responce)
        data = responce.json()
        encoded = md5(self.password.encode()).hexdigest().encode()
        encoded = md5(data.pop("salt").encode() + encoded).hexdigest()

        status = self.http.post(
            "login",
            data={
                "logintype": 1,
                **login_form,
                "un": self.user_name,
                "pw2": encoded,
                "pw": encoded[: len(self.password)],
                **data,
            },
        ).json()

        if "at" not in status:
            raise AuthError(status["message"])
        self.http.headers["at"] = status["at"]

        context = self.http.get("context").json()
        self._user_id = context["userId"]
        self._year_id = context["schoolYearId"]

    def logout(self):
        self.http.post("auth/logout")

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def __repr__(self):
        return f"<NetCity({self.school}, {self.user_name})"


@dataclass
class School:
    state: str
    province: str
    city: str
    func: str
    name: str

    def __iter__(self):
        yield self.state
        yield self.province
        yield self.city
        yield self.func
        yield self.name
