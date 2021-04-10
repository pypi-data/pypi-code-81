"""Commands for creating datasets."""

import sys
import os
import getpass
import datetime

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import click
import dtoolcore
import dtoolcore.storagebroker
import dtoolcore.utils

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.parser import ParserError
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.scalarfloat import ScalarFloat
from ruamel.yaml.scanner import ScannerError

from dtool_cli.cli import (
    base_dataset_uri_argument,
    proto_dataset_uri_argument,
    dataset_uri_argument,
    CONFIG_PATH,
)

from dtool_create.utils import valid_handle


_HERE = os.path.dirname(__file__)
_TEMPLATE_DIR = os.path.join(_HERE, "templates")
README_TEMPLATE_FPATH = os.path.join(_TEMPLATE_DIR, "README.yml")


def _get_readme_template(fpath=None):

    if fpath is None:
        fpath = dtoolcore.utils.get_config_value(
            "DTOOL_README_TEMPLATE_FPATH",
            CONFIG_PATH
        )
    if fpath is None:
        fpath = README_TEMPLATE_FPATH

    with open(fpath) as fh:
        readme_template = fh.read()

    user_email = dtoolcore.utils.get_config_value(
        "DTOOL_USER_EMAIL",
        CONFIG_PATH,
        "you@example.com"
    )

    user_full_name = dtoolcore.utils.get_config_value(
        "DTOOL_USER_FULL_NAME",
        CONFIG_PATH,
        "Your Name"
    )

    readme_template = readme_template.format(
        username=getpass.getuser(),
        DTOOL_USER_FULL_NAME=user_full_name,
        DTOOL_USER_EMAIL=user_email,
        date=datetime.date.today(),
    )

    return readme_template


def _prompt_for_values(d):
    """Update the descriptive metadata interactively.

    Uses values entered by the user. Note that the function keeps recursing
    whenever a value is another ``CommentedMap`` or a ``list``. The
    function works as passing dictionaries and lists into a function edits
    the values in place.
    """
    for key, value in d.items():
        if isinstance(value, CommentedMap):
            _prompt_for_values(value)
        elif isinstance(value, list):
            for item in value:
                _prompt_for_values(item)
        elif isinstance(value, datetime.date):
            def parse_date(value):
                try:
                    date = datetime.datetime.strptime(value, "%Y-%m-%d")
                except ValueError as e:
                    raise click.BadParameter(
                        "Could not parse date, {}".format(e), param=value)
                return date
            new_value = click.prompt(key, default=value, value_proc=parse_date)
            if isinstance(new_value, datetime.date):
                d[key] = new_value
            else:
                d[key] = new_value.date()
        else:
            typ = type(value)

            if isinstance(value, ScalarFloat):  # Deal with ruamel.yaml floats.
                typ = float

            new_value = click.prompt(key, type=typ, default=value)
            d[key] = new_value
    return d


def _validate_name(name):
    if not dtoolcore.utils.name_is_valid(name):
        click.secho("Invalid dataset name '{}'".format(name), fg="red")
        click.secho(
            "Name must be 80 characters or less",
        )
        click.secho(
            "Dataset names may only contain the characters: {}".format(
                " ".join(dtoolcore.utils.NAME_VALID_CHARS_LIST)
            ),
        )
        click.secho("Example: field-trial-scores-T8.3")
        sys.exit(6)


@click.command()
@click.option("--quiet", "-q", is_flag=True, help="Only return new URI")
@click.argument("name")
@click.argument("base_uri", default="")
@click.option("--symlink-path", "-s", type=click.Path(exists=True))
def create(quiet, name, base_uri, symlink_path):
    """Create a proto dataset."""
    _validate_name(name)

    admin_metadata = dtoolcore.generate_admin_metadata(name)
    parsed_base_uri = dtoolcore.utils.generous_parse_uri(base_uri)

    if parsed_base_uri.scheme == "symlink":
        if symlink_path is None:
            raise click.UsageError("Need to specify symlink path using the -s/--symlink-path option")  # NOQA

    if symlink_path:
        base_uri = dtoolcore.utils.sanitise_uri(
            "symlink:" + parsed_base_uri.path
        )
        parsed_base_uri = dtoolcore.utils.generous_parse_uri(base_uri)

    # Create the dataset.
    proto_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=dtoolcore.utils.urlunparse(parsed_base_uri),
        config_path=CONFIG_PATH)

    # If we are creating a symlink dataset we need to set the symlink_path
    # attribute on the storage broker.
    if symlink_path:
        symlink_abspath = os.path.abspath(symlink_path)
        proto_dataset._storage_broker.symlink_path = symlink_abspath
    try:
        proto_dataset.create()
    except dtoolcore.storagebroker.StorageBrokerOSError as err:
        raise click.UsageError(str(err))

    proto_dataset.put_readme("")

    if quiet:
        click.secho(proto_dataset.uri)
    else:
        # Give the user some feedback and hints on what to do next.
        click.secho("Created proto dataset ", nl=False, fg="green")
        click.secho(proto_dataset.uri)
        click.secho("Next steps: ")

        step = 1

        if parsed_base_uri.scheme != "symlink":
            click.secho("{}. Add raw data, eg:".format(step))
            click.secho(
                "   dtool add item my_file.txt {}".format(proto_dataset.uri),
                fg="cyan")

            if parsed_base_uri.scheme == "file":
                # Find the abspath of the data directory for user feedback.
                data_path = proto_dataset._storage_broker._data_abspath
                click.secho("   Or use your system commands, e.g: ")
                click.secho(
                    "   mv my_data_directory {}/".format(data_path),
                    fg="cyan"
                )
            step = step + 1

        click.secho("{}. Add descriptive metadata, e.g: ".format(step))
        click.secho(
            "   dtool readme interactive {}".format(proto_dataset.uri),
            fg="cyan")
        step = step + 1

        click.secho(
            "{}. Convert the proto dataset into a dataset: ".format(step)
        )
        click.secho("   dtool freeze {}".format(proto_dataset.uri), fg="cyan")


@click.command()
@base_dataset_uri_argument
@click.argument("new_name", default="")
def name(dataset_uri, new_name):
    """
    Report / update the name of the dataset.

    It is only possible to update the name of a proto dataset,
    i.e. a dataset that has not yet been frozen.
    """
    if new_name != "":
        _validate_name(new_name)

        try:
            dataset = dtoolcore.ProtoDataSet.from_uri(
                uri=dataset_uri,
                config_path=CONFIG_PATH
            )
        except dtoolcore.DtoolCoreTypeError:
            dataset = dtoolcore.DataSet.from_uri(
                uri=dataset_uri,
                config_path=CONFIG_PATH
            )

        dataset.update_name(new_name)

    admin_metadata = dtoolcore._admin_metadata_from_uri(
        uri=dataset_uri,
        config_path=CONFIG_PATH
    )
    click.secho(admin_metadata["name"])


@click.group()
def readme():
    """Edit / show readme content.

    The readme content is descriptive metadata describing the dataset.
    """


@readme.command()
@proto_dataset_uri_argument
def interactive(proto_dataset_uri):
    """Interactive prompting to populate the readme."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH)

    # Create an CommentedMap representation of the yaml readme template.
    readme_template = _get_readme_template()
    yaml = YAML()
    yaml.explicit_start = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    descriptive_metadata = yaml.load(readme_template)

    descriptive_metadata = _prompt_for_values(descriptive_metadata)

    # Write out the descriptive metadata to the readme file.
    stream = StringIO()

    yaml.dump(descriptive_metadata, stream)

    proto_dataset.put_readme(stream.getvalue())

    click.secho("Updated readme ", fg="green")
    click.secho("To edit the readme using your default editor:")
    click.secho(
        "dtool readme edit {}".format(proto_dataset_uri),
        fg="cyan")


def _validate_readme(readme_content):
    """Return (YAML string, error message)."""
    yaml = YAML()
    # Ensure that the content is valid YAML.
    try:
        readme_formatted = yaml.load(readme_content)
        return readme_formatted, None
    except (ParserError, DuplicateKeyError, ScannerError) as message:
        readme_formatted = None
        return None, str(message)


def _validate_and_put_readme(dataset, readme_content):
    # Create YAML object to standardise the output formatting.
    yaml = YAML()
    yaml.explicit_start = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    # Validate the YAML.
    readme_formatted, message = _validate_readme(readme_content)
    if message is not None:
        click.secho("Error: Invalid YAML", fg="red")
        click.secho(str(message))
        click.secho("Did not update readme ", fg="red")
        sys.exit(5)

    # Write out formatted YAML.
    stream = StringIO()
    yaml.dump(readme_formatted, stream)
    dataset.put_readme(stream.getvalue())


@readme.command()
@base_dataset_uri_argument
def edit(dataset_uri):
    """Default editor updating of readme content.
    """
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    readme_content = dataset.get_readme_content()

    try:
        # Python2 compatibility.
        readme_content = unicode(readme_content, "utf-8")
    except NameError:
        pass

    edited_content = click.edit(readme_content, extension=".yml")
    if edited_content is not None:
        _validate_and_put_readme(dataset, edited_content)
        click.secho("Updated readme ", nl=False, fg="green")
    else:
        click.secho("Did not update readme ", nl=False, fg="red")
    click.secho(dataset_uri)


@readme.command()
@base_dataset_uri_argument
def show(dataset_uri):
    """Show the descriptive metadata in the readme."""
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    readme_content = dataset.get_readme_content()
    click.secho(readme_content)


@readme.command()
@base_dataset_uri_argument
def validate(dataset_uri):
    """Validate that the README is valid YAML.
    """
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    readme_content = dataset.get_readme_content()

    try:
        # Python2 compatibility.
        readme_content = unicode(readme_content, "utf-8")
    except NameError:
        pass

    _, message = _validate_readme(readme_content)
    if message is not None:
        click.secho("Invalid YAML", fg="red")
        click.secho(str(message))
    else:
        click.secho("All good!  :)", fg="green")


@readme.command()
@base_dataset_uri_argument
@click.argument('input', type=click.File('r'))
def write(dataset_uri, input):
    """Use YAML from a file or stdin to populate the readme.

    To stream content from stdin use "-", e.g.

    echo "desc: my data" | dtool readme write <DS_URI> -
    """
    try:
        dataset = dtoolcore.ProtoDataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    except dtoolcore.DtoolCoreTypeError:
        dataset = dtoolcore.DataSet.from_uri(
            uri=dataset_uri,
            config_path=CONFIG_PATH
        )
    _validate_and_put_readme(dataset, input.read())


@click.group()
def add():
    """Add items and item metadata to a proto dataset."""


@add.command()
@click.argument("input_file", type=click.Path(exists=True))
@proto_dataset_uri_argument
@click.argument("relpath_in_dataset", default="")
def item(proto_dataset_uri, input_file, relpath_in_dataset):
    """Add a file to the proto dataset."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        proto_dataset_uri,
        config_path=CONFIG_PATH)
    if relpath_in_dataset == "":
        relpath_in_dataset = os.path.basename(input_file)
    proto_dataset.put_item(input_file, relpath_in_dataset)


@add.command()
@proto_dataset_uri_argument
@click.argument("relpath_in_dataset")
@click.argument("key")
@click.argument("value")
def metadata(proto_dataset_uri, relpath_in_dataset, key, value):
    """Add metadata to a file in the proto dataset."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH)
    proto_dataset.add_item_metadata(
        handle=relpath_in_dataset,
        key=key,
        value=value)


@click.command()
@proto_dataset_uri_argument
def freeze(proto_dataset_uri):
    """Convert a proto dataset into a dataset.

    This step is carried out after all files have been added to the dataset.
    Freezing a dataset finalizes it with a stamp marking it as frozen.
    """
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(
        uri=proto_dataset_uri,
        config_path=CONFIG_PATH
    )

    num_items = len(list(proto_dataset._identifiers()))
    max_files_limit = int(dtoolcore.utils.get_config_value(
        "DTOOL_MAX_FILES_LIMIT",
        CONFIG_PATH,
        10000
    ))
    assert isinstance(max_files_limit, int)
    if num_items > max_files_limit:
        click.secho(
            "Too many items ({} > {}) in proto dataset".format(
                num_items,
                max_files_limit
            ),
            fg="red"
        )
        click.secho("1. Consider splitting the dataset into smaller datasets")
        click.secho("2. Consider packaging small files using tar")
        click.secho("3. Increase the limit using the DTOOL_MAX_FILES_LIMIT")
        click.secho("   environment variable")
        sys.exit(2)

    handles = [h for h in proto_dataset._storage_broker.iter_item_handles()]
    for h in handles:
        if not valid_handle(h):
            click.secho(
                "Invalid item name: {}".format(h),
                fg="red"
            )
            click.secho("1. Consider renaming the item")
            click.secho("2. Consider removing the item")
            sys.exit(3)

    with click.progressbar(length=len(list(proto_dataset._identifiers())),
                           label="Generating manifest") as progressbar:
        try:
            proto_dataset.freeze(progressbar=progressbar)
        except dtoolcore.storagebroker.DiskStorageBrokerValidationWarning as e:
            click.secho("")
            click.secho(str(e), fg="red", nl=False)
            sys.exit(4)

    click.secho("Dataset frozen ", nl=False, fg="green")
    click.secho(proto_dataset_uri)


def _copy(resume, quiet, dataset_uri, dest_base_uri):
    src_dataset = dtoolcore.DataSet.from_uri(dataset_uri)

    dest_uri = dtoolcore._generate_uri(
        admin_metadata=src_dataset._admin_metadata,
        base_uri=dest_base_uri
    )

    if not resume:
        # Check if the destination URI is already a dataset
        # and exit gracefully if true.
        if dtoolcore._is_dataset(dest_uri, config_path=CONFIG_PATH):
            raise click.UsageError(
                "Dataset already exists: {}".format(dest_uri))

        # If the destination URI is a "file" dataset one needs to check if
        # the path already exists and exit gracefully if true.
        parsed_dataset_uri = dtoolcore.utils.generous_parse_uri(dest_uri)
        if parsed_dataset_uri.scheme == "file":
            if os.path.exists(parsed_dataset_uri.path):
                raise click.UsageError(
                    "Path already exists: {}".format(parsed_dataset_uri.path))

    # Define the copy function to use.
    copy_func = dtoolcore.copy
    if resume:
        copy_func = dtoolcore.copy_resume

    # Finally do the copy
    if quiet:
        dest_uri = copy_func(
            src_uri=dataset_uri,
            dest_base_uri=dest_base_uri,
            config_path=CONFIG_PATH
        )
        click.secho(dest_uri)
    else:
        num_items = len(list(src_dataset.identifiers))
        with click.progressbar(length=num_items*2,
                               label="Copying dataset") as progressbar:
            dest_uri = copy_func(
                src_uri=dataset_uri,
                dest_base_uri=dest_base_uri,
                config_path=CONFIG_PATH,
                progressbar=progressbar
            )

        click.secho("Dataset copied to:\n{}".format(dest_uri))


@click.command()
@click.option("--resume", is_flag=True, help="Resume an interrupted copy")
@click.option("--quiet", "-q", is_flag=True, help="Only return new URI")
@dataset_uri_argument
@click.argument("dest_base_uri")
def copy(resume, quiet, dataset_uri, dest_base_uri):
    """DEPRECATED: Copy a dataset to a different location."""
    click.secho(
        "The ``dtool copy`` command is deprecated",
        fg="red",
        err=True
    )
    click.secho(
        "Use ``dtool cp`` instead",
        fg="red",
        err=True
    )
    _copy(resume, quiet, dataset_uri, dest_base_uri)


@click.command()
@click.option("--resume", is_flag=True, help="Resume an interrupted copy")
@click.option("--quiet", "-q", is_flag=True, help="Only return new URI")
@dataset_uri_argument
@click.argument("dest_base_uri")
def cp(resume, quiet, dataset_uri, dest_base_uri):
    """Copy a dataset to a different location."""
    _copy(resume, quiet, dataset_uri, dest_base_uri)
