from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

_ASSIGNMENT_TYPES = {
    1: "Практическая работа",
    2: "Тематическая работа",
    3: "Домашнее задание",
    4: "Контрольная работа",
    5: "Самостоятельная работа",
    6: "Лабораторная работа",
    7: "Проект",
    8: "Диктант",
    9: "Реферат",
    10: "Ответ на уроке",
    11: "Сочинение",
    12: "Изложение",
    13: "Зачёт",
    14: "Тестирование",
    16: "Диагностическая контрольная работа",
    17: "Диагностическая работа",
    18: "Контрольное списывание",
    21: "Работа на уроке",
    22: "Работа в тетради",
    23: "Ведение рабочей тетради",
    24: "Доклад/Презентация",
    25: "Проверочная работа",
    26: "Чтение наизусть",
    27: "Пересказ текста",
    29: "Предметный диктант",
    31: "Дифференцированный зачет",
    32: "Работа с картами",
    33: "Экзамен",
    34: "Изложение с элементами сочинения",
    35: "Контроль аудирования",
    36: "Контроль грамматики",
    37: "Контроль лексики",
    38: "Устный развернутый ответ",
}


class Assignment(BaseModel):
    id: int
    type: str = Field(alias="typeId")
    name: str = Field(alias="assignmentName")
    weight: int
    mark: Optional[int]
    deadline: Optional[datetime] = Field(alias="dueDate")

    @validator("type", pre=True)
    def validate_type(cls, type_id):
        return _ASSIGNMENT_TYPES[type_id]

    @validator("mark", pre=True)
    def validate_mark(cls, mark):
        return mark["mark"] if mark else None


class Assignments(BaseModel):
    __root__: List[Assignment]


class Lesson(BaseModel):
    number: int
    subject: str = Field(alias="subjectName")
    start: str = Field(alias="startTime")
    end: str = Field(alias="endTime")
    room: Optional[str]
    assignments: Optional[list[Assignment]]


class Day(BaseModel):
    date: datetime = Field(alias="date")
    lessons: list[Lesson]


class Diary(BaseModel):
    start: datetime = Field(alias="weekStart")
    end: datetime = Field(alias="weekEnd")
    days: list[Day] = Field(alias="weekDays")


# TODO:
# * авторы
# * файлы
class Attachment(BaseModel):
    id: int
    name: Optional[str]


class Attachments(BaseModel):
    __root__: List[Attachment]


class DetailedAssignment(BaseModel):
    id: int
    assignment_name: str = Field(alias="assignmentName")
    activity_name: Optional[str]
    problem_name: Optional[str]
    subject_group: dict = Field(alias="subjectGroup")
    teachers: list[dict]
    weight: int
    date: datetime
    description: Optional[str]
    attachments: Attachments


class Announcement(BaseModel):
    id: int
    name: str
    description: str
    post_date: Optional[datetime] = Field(alias="postDate")
    delete_date: Optional[datetime] = Field(alias="deleteDate")
    attachments: Optional[list[Attachment]]


class Announcements(BaseModel):
    __root__: List[Announcement]
