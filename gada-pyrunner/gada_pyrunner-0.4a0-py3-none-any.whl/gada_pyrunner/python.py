"""Can run a gada node from a Python script by spawning a subprocess.

Basic Python package structure:

.. code-block:: bash

    ├── mycomponent
    │   ├── __init__.py
    │   ├── mynode.py
    │   └── config.yml

Content of ``mynode.py``:

.. code-block:: python

    def main():
        print("hello world")

    if __name__ == "__main__":
        main()

Sample ``config.yml``:

.. code-block:: yaml

    nodes:
      mynode:
        runner: python
        file: ${comp_dir}/mynode.py

Usage:

.. code-block:: bash

    $ gada mycomponent.mynode
    hello world

"""
from __future__ import annotations

__all__ = ["run"]
from typing import Optional
from gada.runners import generic


def run(
    comp,
    *,
    gada_config: dict,
    node_config: dict,
    argv: Optional[list[str]] = None,
    **kwargs: dict
):
    """Run a gada node from a Python script:

    .. code-block:: python

        >>> import gada
        >>> import gada.test_utils
        >>> import gada_pyrunner
        >>>
        >>> # Overwrite "gada_pyrunner/test/testnodes/config.yml" for this test
        >>> gada_pyrunner.test_utils.write_testnodes_config({
        ...     'nodes': {
        ...         'hello': {
        ...             'runner': 'python',
        ...             'file': '${comp_dir}/__init__.py'
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
        {'runner': 'python', ...}
        >>>
        >>> # Need to create fake stdin and stdout for unittests
        >>> with gada.test_utils.PipeStream() as stdin:
        ...     with gada.test_utils.PipeStream() as stdout:
        ...         # Run node with CLI arguments
        ...         gada_pyrunner.python.run(
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
        ...         stdout.reader.read().decode().strip()
        'hello john !'
        >>>

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param kwargs: unused arguments
    """
    argv = argv if argv is not None else []

    generic.run(
        comp=comp,
        gada_config=gada_config,
        node_config={
            "bin": node_config.get("bin", "python"),
            "env": node_config.get("env", {}),
        },
        argv=[node_config["file"]] + argv,
        **kwargs
    )
