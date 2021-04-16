from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .._path_utils import PathLike
from ._utils import Configuration


@dataclass(frozen=True)
class LoggingConfiguration(Configuration):

    file_path: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        data_dict = dict(data)

        return create_logging_config(**data_dict)


def create_logging_config(
    *,
    file_path: PathLike,
) -> LoggingConfiguration:
    """Create a logging configuration.

    Args:
        file_path: The path of the file where the session logs will be written.

    Note:
        The rolling policy is:

            * A maximum file size of ``10MB``.
            * A maximum history of 7 days.

        Once the maximum size is reached, logs are archived following the pattern ``f"{file_path}.{date}.{i}.gz"`` where ``date`` is the creation date of the file in the ``yyyy-MM-dd`` format and ``i`` an integer incremented during the day.

    Example:
        >>> python_config = tt.config.create_config(
        ...     logging=tt.config.create_logging_config(
        ...         file_path="./atoti/server.log",
        ...     )
        ... )
        >>> yaml_config = '''
        ... logging:
        ...   file_path: ./atoti/server.log
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return LoggingConfiguration(file_path=str(Path(file_path).absolute()))
