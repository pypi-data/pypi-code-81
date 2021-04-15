# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

from .base import *


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key = True)
    title = Column(String(255, collation = "utf8_bin"), index = True)
    text = Column(Text(4294000000, collation = "utf8_bin"))
