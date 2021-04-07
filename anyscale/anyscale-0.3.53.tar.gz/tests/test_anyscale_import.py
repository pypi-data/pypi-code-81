import subprocess

import anyscale


# Make sure anyscale is using the vendored Ray
def test_use_vendored_ray_in_cli() -> None:
    # Make sure to use vendored ray when anyscale is used in the CLI.
    assert b"anyscale_ray" in subprocess.check_output(  # noqa: B1
        ["python", "-c", "import anyscale; import ray; print(ray.__path__)"],
        env=anyscale.ANYSCALE_ENV,
    )
    # Make sure to not use vendored ray when anyscale is used as a
    # package (e.g. if we use anyscale.connect).
    assert b"anyscale_ray" not in subprocess.check_output(  # noqa: B1
        ["python", "-c", "import anyscale; import ray; print(ray.__path__)"],
    )
