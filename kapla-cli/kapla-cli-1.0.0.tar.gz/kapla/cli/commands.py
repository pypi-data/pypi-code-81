from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kapla.cli.projects import Monorepo

from kapla.cli.utils import current_directory, run


def export_packages(repo: Monorepo) -> None:
    """Export packages using poetry and pip for offline usage."""
    export_directory = repo.root / "dist"
    download_directory = export_directory / "_downloads"
    requirements = download_directory / "export.requirements"
    shutil.rmtree(export_directory, ignore_errors=True)
    download_directory.mkdir(parents=True, exist_ok=True)
    requirements.touch()
    for package in repo.get_packages():
        with current_directory(package.root):
            if package.pyproject.packages != []:
                package.build()
            run(f"poetry export >> {requirements}")
            _requirements = requirements.read_text()
            requirements.write_text(
                "\n".join(
                    [
                        requirement
                        for requirement in _requirements.split("\n")
                        if "@" not in requirement
                    ]
                )
            )
            wheels = package.root.glob("dist/*.whl")
            for wheel in wheels:
                shutil.move(str(wheel), download_directory / wheel.name)
            if package.root == repo.root:
                continue
            shutil.rmtree(package.root / "dist")

    with current_directory(download_directory):
        run(f"pip download -r {requirements}")
    out_name = repo.pyproject.name + "-" + repo.pyproject.version
    shutil.make_archive(out_name, format="zip", root_dir=download_directory)
    out_file = repo.root / "dist" / (out_name + ".zip")
    shutil.move(out_name + ".zip", str(out_file))
    shutil.rmtree(download_directory)


def release_version(repo: Monorepo) -> None:

    pass
