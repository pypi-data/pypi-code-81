from inspect import stack
from pathlib import Path
from typing import Optional, Type

PACKAGE_DIRECTORY = str(Path(__file__).resolve().parent)


class DeferredInfo:
    def __init__(self, exception: Type[Exception], fail_desc: str, msg: Optional[str]):
        self.exception_name = exception.__name__
        self.fail_desc = fail_desc
        self.msg = msg

        try:
            s = stack()
            # strip frames within assertion package
            while len(s) >= 2 and s[0].filename.startswith(PACKAGE_DIRECTORY):
                s.pop(0)
            self.file_path = s[0].filename
            self.line_num = s[0].lineno
            self.func_name = s[0].function
            if s[0].code_context and s[0].index is not None:
                self.source_code = s[0].code_context[s[0].index].strip()
            else:
                self.source_code = "<code unavailable>"  # pragma: no cover
        finally:
            del s

    def __str__(self) -> str:
        s = (
            f'{self.exception_name}[File "{self.file_path}", line {self.line_num}, '
            f'in {self.func_name}, "{self.source_code}"]: '
        )
        if self.msg:
            s += f"{self.msg}: "
        s += self.fail_desc
        return s

    def __repr__(self) -> str:
        return str(self)
