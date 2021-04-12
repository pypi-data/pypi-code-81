# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module helps to resolve the platform on which the
script runs on. The functions in the module aren't
functional-like as they depend on the platform.
"""

import functools
import platform

from collections import namedtuple

from .cache import cached

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name


# The type of the target representations.
#
# system -- The name of the system or OS.
#
# machine -- The machine type.
Target = namedtuple("Target", ["system", "machine"])


def _get_linux_machines():
    """Gives the possible machine types for Linux systems."""
    return [
        "x86_64",
        "armv6",
        "armv7",
        "aarch64",
        "powerpc64",
        "powerpc64le",
        "s390x"
    ]


def _get_windows_machines():
    """Gives the possible machine types for Windows systems."""
    return ["x86_64", "AMD64"]


def get_known_targets():
    """
    Gives a list of the known targets that the script and the
    project that the script acts on supports.
    """
    def _create_target(system, machine="x86_64"):
        """
        Creates a representation of a target.

        system -- The name of the system or OS.

        machine -- The machine type.
        """
        return Target(system=system, machine=machine)

    targets = []

    # Create the Darwin targets.
    targets.append(_create_target(system=get_darwin_system_name()))

    # Create the Linux targets.
    create_linux_target = functools.partial(
        _create_target,
        system=get_linux_system_name()
    )

    for m in _get_linux_machines():
        targets.append(create_linux_target(machine=m))

    # Create the Windows targets.
    create_windows_target = functools.partial(
        _create_target,
        system=get_windows_system_name()
    )

    for m in _get_windows_machines():
        targets.append(create_windows_target(machine=m))

    return targets


@cached
def current_platform():
    """Resolves the platform in the correct format."""
    return platform.system().lower()


@cached
def resolve_host_target():
    """Resolves the platform on which the script is run."""
    def _is_host_target_valid(system, machine):
        """
        Checks if the current host machine is a valid target.

        system -- The name of the system or OS.

        machine -- The machine type.
        """
        machines = (t.machine for t in get_known_targets()
                    if t.system == system)
        return machine in machines
    if _is_host_target_valid(current_platform(), platform.machine()):
        return "{}-{}".format(current_platform(), platform.machine()).lower()
    raise NotImplementedError(
        "System '{}' with architecture '{}' is not supported".format(
            current_platform(),
            platform.machine()
        )
    )


def parse_target_from_argument_string(target):
    """Creates an object representation of the given target."""
    return Target(system=target.split("-")[0], machine=target.split("-")[1])
