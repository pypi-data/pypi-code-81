"""Build OCI images using docker buildx"""
from pathlib import Path
from sys import exit
from typing import List, Optional, Union

from loguru import logger
from pydantic.error_wrappers import ValidationError
from python_on_whales import docker
from typer import Context, Typer, echo

from kapla.cli.utils import map_string_to_dict

from .datatypes import BuildContext, Catalog, Image

app = Typer(
    name="builder",
    add_completion=False,
    no_args_is_help=True,
    invoke_without_command=False,
)


@app.command(
    "build", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def build(
    ctx: Context,
    builder_file: Optional[str] = None,
    *,
    context: Optional[Path] = None,
    add_hosts: Optional[List[str]] = None,
    allow: Optional[List[str]] = None,
    build_args: Optional[List[str]] = None,
    builder: Optional[str] = None,
    cache: bool = True,
    cache_from: Optional[str] = None,
    cache_to: Optional[str] = None,
    dump: bool = False,
    file: Optional[Path] = None,
    labels: Optional[List[str]] = None,
    load: bool = False,
    name: Optional[str] = None,
    network: Optional[str] = None,
    output: Optional[str] = None,
    platforms: Optional[List[str]] = None,
    progress: str = "auto",
    pull: bool = False,
    push: bool = False,
    secrets: Optional[List[str]] = None,
    ssh: Optional[str] = None,
    tags: Optional[List[str]] = None,
    target: Optional[str] = None,
) -> None:
    """Build a docker image."""
    if builder_file:
        try:
            images = [Image.from_file(builder_file)]
        except ValidationError as err:
            echo(err, err=True)
            exit(1)
    elif name:
        catalog = Catalog.from_directory(Path.cwd())
        try:
            images = [next(image for image in catalog.images if image.name == name)]
        except StopIteration:
            echo(f"Build config for image {name} does not exist", err=True)
            exit(1)
    else:
        try:
            images = Catalog.from_directory(Path.cwd()).images
        except ValidationError as err:
            echo(err, err=True)
            exit(1)

    _add_hosts = map_string_to_dict(add_hosts)
    _labels = map_string_to_dict(labels or [])
    names = [tag for tag in tags] if tags else []

    is_key = True
    kwargs = {}
    for extra_arg in ctx.args:
        if is_key:
            key = extra_arg
            if key.startswith("--"):
                key = key[2:]
            elif key.startswith("-"):
                key = key[1:]
            if "=" in extra_arg:
                key, value = key.split("=")
                key = key.replace("-", "_").upper()
                kwargs[key] = value
                is_key = True
                continue
            else:
                is_key = False
                continue
        key = key.replace("-", "_").upper()
        kwargs[key] = extra_arg
        is_key = True
    _user_build_args = map_string_to_dict(build_args or [])
    _user_build_args = {**_user_build_args, **kwargs}

    if dump:
        _output = {"type": "local", "dest": "."}
    elif output:
        _output = map_string_to_dict(output)
    else:
        _output = {}

    if progress.lower() in ("0", "false", "no", "n"):
        _progress: Union[bool, str] = False
    else:
        _progress = progress

    # TODO: Is there some order ?
    for image in images:
        _build_args = {
            arg.name.upper(): arg.default
            for arg in image.build.build_args
            if arg.default
        }

        _build_args.update(
            {key.upper(): value for key, value in _user_build_args.items()}
        )
        _names = names or [image.get_name()]

        logger.debug(f"Building image {_names[0]} with build arguments: {_build_args}")
        if len(_names) > 1:
            for name in _names[1:]:
                logger.debug(f"Using additional tag: {name}")

        build_context = BuildContext(
            context_path=context or image.build.context,
            add_hosts=_add_hosts or image.build.add_hosts,
            allow=list(allow or []),
            build_args=_build_args,
            builder=builder,
            cache=cache,
            cache_from=cache_from,
            cache_to=cache_to,
            file=file or image.build.file,
            labels={**image.labels, **_labels},
            load=load,
            network=network,
            output=_output,
            platforms=list(platforms or []) or image.platforms,
            progress=_progress,
            pull=pull,
            push=push,
            secrets=secrets,
            ssh=ssh,
            tags=_names,
            target=target,
        )
        docker.buildx.build(**build_context.dict())
