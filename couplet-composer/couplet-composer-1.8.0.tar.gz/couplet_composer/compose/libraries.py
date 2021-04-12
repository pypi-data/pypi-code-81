# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for installing the
dynamic libraries needed to run the project.
"""

import json
import logging
import os

from ..support.file_paths import get_project_dependencies_file_path

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..support.project_values import get_scripts_base_directory_name

from ..util import shell


def copy_scripts(path, arguments, project_root):
    """
    Copies the scripts required to run the project.

    path -- The directory where the scripts will be copied to.

    arguments -- The parsed command line arguments of the run.

    project_root -- The root directory of the project this script
    acts on.
    """
    script_dest_dir = os.path.join(
        path,
        get_scripts_base_directory_name(coverage=arguments.coverage)
    )

    if os.path.exists(script_dest_dir):
        shell.rmtree(
            script_dest_dir,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        script_dest_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    shell.copytree(
        os.path.join(project_root, "script", "anthem"),
        os.path.join(script_dest_dir, "anthem"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(project_root, "script", "ode"),
        os.path.join(script_dest_dir, "ode"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(project_root, "script", "test", "anthem"),
        os.path.join(script_dest_dir, "anthem"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(project_root, "script", "test", "ode"),
        os.path.join(script_dest_dir, "ode"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    lua_scripts = []

    for dirpath, _, filenames in os.walk(script_dest_dir):
        for filename in filenames:
            if filename == "CMakeLists.txt":
                shell.rm(
                    os.path.join(dirpath, filename),
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            else:
                lua_scripts.append(os.path.join(dirpath, filename))

    logging.debug("The Lua scripts are:\n\n%s", "\n".join(lua_scripts))


def copy_sdl_libraries(
    path,
    arguments,
    host_system,
    source_root,
    project_root,
    dependencies_root
):
    """
    Copies the dynamic SDL libraries required to run the project.

    path -- The directory where the scripts will be copied to.

    arguments -- The parsed command line arguments of the run.

    host_system -- The system this script is run on.

    project_root -- The root directory of the project this script
    acts on.

    dependencies_root -- The directory for the dependencies.
    """
    if host_system != get_windows_system_name():
        logging.debug(
            "Found the following SDL libraries:\n\n{}".format(
                "\n".join(
                    [f for f in os.listdir(os.path.join(
                        dependencies_root,
                        "lib"
                    )) if "libSDL" in f]
                )
            )
        )

    if host_system == get_darwin_system_name():
        sdl_dynamic_lib_name = "libSDL2-2.0.0.dylib"
        sdl_dynamic_lib = os.path.join(path, sdl_dynamic_lib_name)
        if os.path.exists(sdl_dynamic_lib):
            shell.rm(
                sdl_dynamic_lib,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        shell.copy(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name),
            path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    elif host_system == get_linux_system_name():
        def _copy_linux_sdl(name):
            dynamic_lib = os.path.join(path, name)
            if os.path.exists(dynamic_lib):
                shell.rm(
                    dynamic_lib,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            shell.copy(
                os.path.join(dependencies_root, "lib", name),
                path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

        dependency_version_file = os.path.join(
            project_root,
            get_project_dependencies_file_path(source_root)
        )
        with open(dependency_version_file) as f:
            json_data = json.load(f)
            sdl_version = json_data["dependencies"]["sdl"]["version"] \
                if "dependencies" in json_data else json_data["sdl"]["version"]

        sdl_major, sdl_minor, sdl_patch = sdl_version.split(".")

        _copy_linux_sdl("libSDL2-2.0.so.{}.{}.0".format(sdl_minor, sdl_patch))

        def _link_linux_sdl(name, src):
            new_link = os.path.join(path, name)
            if os.path.exists(new_link):
                shell.rm(
                    new_link,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            original = os.path.join(path, src)
            shell.link(
                original,
                new_link,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

        _link_linux_sdl(
            name="libSDL2-2.0.so.{}".format(sdl_major),
            src="libSDL2-2.0.so.{}.{}.0".format(sdl_minor, sdl_patch)
        )
        _link_linux_sdl(
            name="libSDL2-2.0.so",
            src="libSDL2-2.0.so.{}".format(sdl_major)
        )
        _link_linux_sdl(name="libSDL2.so", src="libSDL2-2.0.so")
    elif host_system == get_windows_system_name():
        sdl_dynamic_lib_name = "SDL2.dll"
        sdl_dynamic_lib_d_name = "SDL2d.dll"
        sdl_dynamic_lib = os.path.join(path, sdl_dynamic_lib_name)
        sdl_dynamic_lib_d = os.path.join(path, sdl_dynamic_lib_d_name)
        if os.path.exists(sdl_dynamic_lib):
            shell.rm(
                sdl_dynamic_lib,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        if os.path.exists(sdl_dynamic_lib_d):
            shell.rm(
                sdl_dynamic_lib_d,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        if os.path.exists(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name)
        ):
            shell.copy(
                os.path.join(dependencies_root, "lib", sdl_dynamic_lib_name),
                path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        elif os.path.exists(
            os.path.join(dependencies_root, "lib", sdl_dynamic_lib_d_name)
        ):
            shell.copy(
                os.path.join(dependencies_root, "lib", sdl_dynamic_lib_d_name),
                path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        else:
            logging.debug("No dynamic SDL library was found for Windows")
