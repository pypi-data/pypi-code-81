# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from .base import *


class Redirection(Base):

    __tablename__ = "redirections"

    id = Column(Integer, primary_key = True)
    source = Column(String(255, collation = "utf8_bin"), index = True)
    target = Column(String(255, collation = "utf8_bin"), index = True)
