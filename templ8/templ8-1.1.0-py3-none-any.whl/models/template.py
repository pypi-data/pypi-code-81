import os
from dataclasses import dataclass
from typing import Any, Dict

from templ8.services.jinja import template_schema


@dataclass
class Template:
    root: str
    path: str

    def __repr__(self) -> str:
        return self.path

    @property
    def schema(self) -> Dict[str, Any]:
        return template_schema(os.path.join(self.root, self.path))

    @property
    def output_path(self) -> str:
        return self.path[:-3]
