"""Can run a gada node from a Python package installed in ``PYTHONPATH`` without spawning a subprocess.

Basic Python package structure:

.. code-block:: bash

    ├── mycomponent
    │   ├── __init__.py
    │   ├── mynode.py
    │   └── config.yml

Content of ``mynode.py``:

.. code-block:: python

    def main(**kwargs):
        print("hello world")

Sample ``config.yml``:

.. code-block:: yaml

    nodes:
      mynode:
        runner: pymodule
        module: mycomponent.mynode
        entrypoint: main

Usage:

.. code-block:: bash

    $ gada mycomponent.mynode
    hello world

"""
from __future__ import annotations

__all__ = ["run"]
from typing import Optional


def load_module(name: str):
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:
        raise Exception(f"failed to import module {name}") from e


def run(
    comp,
    *,
    gada_config: dict,
    node_config: dict,
    argv: Optional[list[str]] = None,
    stdin=None,
    stdout=None,
    stderr=None,
    **kwargs: dict,
):
    """Run a gada node from a Python package:

    .. code-block:: python

        >>> import gada
        >>> import gada.test_utils
        >>> import gada_pyrunner
        >>>
        >>> # Overwrite "gada_pyrunner/test/testnodes/config.yml" for this test
        >>> gada_pyrunner.test_utils.write_testnodes_config({
        ...     'nodes': {
        ...         'hello': {
        ...             'runner': 'pymodule',
        ...             'module': 'testnodes',
        ...             'entrypoint': 'hello'
        ...         }
        ...     }
        ... })
        >>>
        >>> # Load "testnodes" component
        >>> comp = gada.component.load('testnodes')
        >>>
        >>> # Load component and node configuration
        >>> gada_config = gada.datadir.load_config()
        >>> comp_config = gada.component.load_config(comp)
        >>> print(comp_config)
        {'nodes': ...}
        >>> node_config = gada.component.get_node_config(comp_config, 'hello')
        >>> print(node_config)
        {'runner': 'pymodule', ...}
        >>>
        >>> # Need to create fake stdin and stdout for unittests
        >>> with gada.test_utils.PipeStream(rmode='r', wmode='w') as stdin:
        ...     with gada.test_utils.PipeStream(rmode='r', wmode='w') as stdout:
        ...         # Run node with CLI arguments
        ...         gada_pyrunner.pymodule.run(
        ...             comp,
        ...             argv=['john'],
        ...             gada_config=gada_config,
        ...             node_config=node_config,
        ...             stdin=stdin.reader,
        ...             stdout=stdout.writer,
        ...             stderr=stdout.writer
        ...         )
        ...
        ...         # Close writer end so we can read form it
        ...         stdout.writer.close()
        ...
        ...         # Read node output
        ...         stdout.reader.read().strip()
        'hello john !'
        >>>

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param stdin: input stream
    :param stdout: output stream
    :param stderr: error stream
    :param kwargs: unused arguments
    """
    argv = argv if argv is not None else []

    # Check the entrypoint is configured
    entrypoint = node_config.get("entrypoint", None)
    if not entrypoint:
        raise Exception("missing entrypoint in configuration")

    # Load module if explicitely configured
    if "module" in node_config:
        comp = load_module(node_config["module"])

    # Check the entrypoint exists
    fun = getattr(comp, entrypoint, None)
    if not fun:
        raise Exception(f"module {comp.__name__} has no entrypoint {entrypoint}")

    # Call entrypoint
    fun(argv=[comp.__name__] + argv, stdin=stdin, stdout=stdout, stderr=stderr)
