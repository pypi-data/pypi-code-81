from inspect import cleandoc
from typing import Set


class InvalidMetadata(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(f"Could not parse metadata: {path}")


class InvalidTemplate(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(f"Could not parse template: {path}")


class UnrecognizedFormat(Exception):
    def __init__(self, fmt: str) -> None:
        super().__init__(f"Unrecognized format: {fmt}")


class MissingOutputDir(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Missing output directory from input configuration"
        )


class MissingCollections(Exception):
    def __init__(self, missing_collections: Set[str]) -> None:
        super().__init__(
            cleandoc(
                f"""
                Specified collections were not found when gathering templates:
                {missing_collections}
                """
            )
        )


class MissingIncludes(Exception):
    def __init__(self, missing_includes: Set[str]) -> None:
        super().__init__(
            cleandoc(
                f"""
                Specified includes were not found when gathering templates:
                {missing_includes}
                """
            )
        )


class MissingRenderContext(Exception):
    def __init__(self, missing_context: Set[str]) -> None:
        super().__init__(
            f"Missing required variables: {missing_context}"
        )


class InvalidFolderRename(Exception):
    def __init__(self, rename_token: str) -> None:
        super().__init__(f"{rename_token} is not a non-empty string")
