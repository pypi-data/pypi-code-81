#!/usr/bin/env python3
from typing import Callable
from codoc.domain.model import Graph

FilterType = Callable[[Graph], Graph]
