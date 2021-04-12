# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding Simple DirectMedia Layer.
"""

import logging
import os

from ..support.cmake_generators import \
    get_visual_studio_16_cmake_generator_name

from ..support.environment import get_temporary_directory

from ..support.platform_names import get_windows_system_name

from ..util.build_util import build_with_cmake

from ..util.cache import cached

from ..util import http, shell


def _copy_visual_c_binaries(
    dependencies_root,
    subdirectory,
    dry_run=None,
    print_debug=None
):
    """
    Copies the pre-built binaries for Visual C on Windows.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    subdirectory -- The temporary directory where the SDL files
    are located.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    if not os.path.isdir(os.path.join(dependencies_root, "include")):
        shell.makedirs(
            os.path.join(dependencies_root, "include"),
            dry_run=dry_run,
            echo=print_debug
        )
    include_dir = os.path.join(dependencies_root, "include", "SDL2")
    if os.path.isdir(include_dir):
        shell.rmtree(include_dir, dry_run=dry_run, echo=print_debug)
    shell.copytree(
        os.path.join(subdirectory, "include"),
        include_dir,
        dry_run=dry_run,
        echo=print_debug
    )
    if not os.path.isdir(os.path.join(dependencies_root, "lib")):
        shell.makedirs(
            os.path.join(dependencies_root, "lib"),
            dry_run=dry_run,
            echo=print_debug
        )
    for lib_file in os.listdir(os.path.join(
        dependencies_root,
        "lib"
    )):
        if "SDL" in lib_file:
            shell.rm(
                os.path.join(dependencies_root, "lib", lib_file),
                dry_run=dry_run,
                echo=print_debug
            )
    for lib_file in os.listdir(os.path.join(subdirectory, "lib", "x64")):
        shell.copy(
            os.path.join(subdirectory, "lib", "x64", lib_file),
            os.path.join(dependencies_root, "lib", lib_file),
            dry_run=dry_run,
            echo=print_debug
        )


def _build_using_cmake(
    toolchain,
    cmake_generator,
    dependencies_root,
    temporary_directory,
    subdirectory,
    target,
    host_system,
    build_variant,
    dry_run=None,
    print_debug=None
):
    """
    Builds SDL using CMake.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    temporary_directory -- The temporary directory used for
    downloading and building SDL.

    subdirectory -- The temporary directory where the SDL files
    are located.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    build_with_cmake(
        toolchain=toolchain,
        cmake_generator=cmake_generator,
        source_directory=subdirectory,
        temporary_root=temporary_directory,
        dependencies_root=dependencies_root,
        target=target,
        host_system=host_system,
        build_variant=build_variant,
        msbuild_target="ALL_BUILD.vcxproj",
        dry_run=dry_run,
        print_debug=print_debug
    )

    def _copy_windows_lib(
        library_name,
        dependencies_root,
        temporary_directory,
        build_variant,
        extension,
        dry_run=None,
        print_debug=None
    ):
        """
        Copies a built SDL library on Windows from the temporary
        build directory to the dependency directory.

        library_name -- The name of the library to copy.

        dependencies_root -- The root directory of the
        dependencies for the current build target.

        temporary_directory -- The temporary directory used for
        downloading and building SDL.

        build_variant -- The build variant used to build the project.

        extension -- The file extension of the library files.

        dry_run -- Whether the commands are only printed instead
        of running them.

        print_debug -- Whether debug output should be printed.
        """
        lib_file = os.path.join(
            dependencies_root,
            "lib",
            "{}.{}".format(library_name, extension)
        )
        lib_file_d = os.path.join(
            dependencies_root,
            "lib",
            "{}d.{}".format(library_name, extension)
        )

        if os.path.exists(lib_file):
            shell.rm(lib_file, dry_run=dry_run, echo=print_debug)

        if os.path.exists(lib_file_d):
            shell.rm(lib_file_d, dry_run=dry_run, echo=print_debug)

        temp_lib_file = os.path.join(
            temporary_directory,
            "build",
            build_variant,
            "{}.{}".format(library_name, extension)
        )
        temp_lib_file_d = os.path.join(
            temporary_directory,
            "build",
            build_variant,
            "{}d.{}".format(library_name, extension)
        )

        if os.path.exists(temp_lib_file):
            shell.copy(
                temp_lib_file,
                lib_file,
                dry_run=dry_run,
                echo=print_debug
            )
        elif os.path.exists(temp_lib_file_d):
            shell.copy(
                temp_lib_file_d,
                lib_file_d,
                dry_run=dry_run,
                echo=print_debug
            )
        else:
            logging.debug(
                "No built SDL library was found with name %s",
                library_name
            )

    if cmake_generator == get_visual_studio_16_cmake_generator_name():
        if not os.path.isdir(os.path.join(dependencies_root, "lib")):
            shell.makedirs(
                os.path.join(dependencies_root, "lib"),
                dry_run=dry_run,
                echo=print_debug
            )

        _copy_windows_lib(
            library_name="SDL2-static",
            dependencies_root=dependencies_root,
            temporary_directory=temporary_directory,
            build_variant=build_variant,
            extension="lib",
            dry_run=dry_run,
            print_debug=print_debug
        )
        _copy_windows_lib(
            library_name="SDL2",
            dependencies_root=dependencies_root,
            temporary_directory=temporary_directory,
            build_variant=build_variant,
            extension="lib",
            dry_run=dry_run,
            print_debug=print_debug
        )
        _copy_windows_lib(
            library_name="SDL2main",
            dependencies_root=dependencies_root,
            temporary_directory=temporary_directory,
            build_variant=build_variant,
            extension="lib",
            dry_run=dry_run,
            print_debug=print_debug
        )
        _copy_windows_lib(
            library_name="SDL2",
            dependencies_root=dependencies_root,
            temporary_directory=temporary_directory,
            build_variant=build_variant,
            extension="dll",
            dry_run=dry_run,
            print_debug=print_debug
        )

        if not os.path.isdir(
            os.path.join(dependencies_root, "include", "SDL2")
        ):
            shell.makedirs(
                os.path.join(dependencies_root, "include", "SDL2"),
                dry_run=dry_run,
                echo=print_debug
            )

        shell.copytree(
            os.path.join(subdirectory, "include"),
            os.path.join(dependencies_root, "include", "SDL2"),
            dry_run=dry_run,
            echo=print_debug
        )


def _build(
    toolchain,
    dependencies_root,
    temporary_directory,
    subdirectory,
    dry_run=None,
    print_debug=None
):
    """
    Builds SDL using the build scripts supplied with it.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    temporary_directory -- The temporary directory used for
    downloading and building SDL.

    subdirectory -- The temporary directory where the SDL files
    are located.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    config_call = [
        os.path.join(subdirectory, "configure"),
        "--prefix={}".format(dependencies_root)
    ]

    build_directory = os.path.join(temporary_directory, "build")

    shell.makedirs(build_directory, dry_run=dry_run, echo=print_debug)

    with shell.pushd(build_directory):
        shell.call(config_call, dry_run=dry_run, echo=print_debug)
        shell.call([toolchain.make], dry_run=dry_run, echo=print_debug)
        shell.call(
            [toolchain.make, "install"],
            dry_run=dry_run,
            echo=print_debug
        )


################################################################
# DEPENDENCY DATA FUNCTIONS
################################################################


@cached
def should_install(
    dependencies_root,
    version,
    target,
    host_system,
    installed_version
):
    """
    Tells whether the build of the dependency should be skipped.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    installed_version -- The version of the dependecy that is
    written to the JSON file containing the currently installed
    versions of the dependencies.
    """
    if not installed_version or version != installed_version:
        return True

    if host_system == get_windows_system_name():
        lib_file = os.path.join(dependencies_root, "lib", "SDL2.lib")
        main_lib_file = os.path.join(dependencies_root, "lib", "SDL2main.lib")
        dynamic_lib_file = os.path.join(dependencies_root, "lib", "SDL2.dll")
        if not (os.path.exists(lib_file) and os.path.exists(main_lib_file)
                and os.path.exists(dynamic_lib_file)):
            lib_file = os.path.join(dependencies_root, "lib", "SDL2d.lib")
            main_lib_file = os.path.join(
                dependencies_root,
                "lib",
                "SDL2maind.lib"
            )
            dynamic_lib_file = os.path.join(
                dependencies_root,
                "lib",
                "SDL2d.dll"
            )
            return not (os.path.exists(lib_file)
                        and os.path.exists(main_lib_file)
                        and os.path.exists(dynamic_lib_file))
        else:
            return False
    else:
        lib_file = os.path.join(dependencies_root, "lib", "libSDL2.a")
        main_lib_file = os.path.join(dependencies_root, "lib", "libSDL2main.a")
        if not (os.path.exists(lib_file) and os.path.exists(main_lib_file)):
            lib_file = os.path.join(dependencies_root, "lib", "libSDL2d.a")
            main_lib_file = os.path.join(
                dependencies_root,
                "lib",
                "libSDL2maind.a"
            )
            return not (os.path.exists(lib_file)
                        and os.path.exists(main_lib_file))
        else:
            return False


def install_dependency(install_info, dry_run=None, print_debug=None):
    """
    Installs the dependency by downloading and possibly building
    it. Returns the path to the built dependency.

    install_info -- The object containing the install information
    for this tool.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    temp_dir = get_temporary_directory(build_root=install_info.build_root)
    dependency_temp_dir = os.path.join(temp_dir, "sdl")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    url = ("https://www.libsdl.org/release/SDL2-{version}.zip"
           if install_info.host_system == get_windows_system_name()
           else "https://www.libsdl.org/release/SDL2-{version}.tar.gz").format(
        version=install_info.version
    )
    dest = os.path.join(
        dependency_temp_dir,
        "sdl.zip" if install_info.host_system == get_windows_system_name()
        else "sdl.tar.gz"
    )

    http.stream(
        url=url,
        destination=dest,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
    shell.tar(dest, dependency_temp_dir, dry_run=dry_run, echo=print_debug)

    subdir = os.path.join(dependency_temp_dir, "SDL2-{}".format(
        install_info.version
    ))

    if install_info.host_system == get_windows_system_name():
        # _copy_visual_c_binaries(
        #     dependencies_root=dependencies_root,
        #     subdirectory=subdir,
        #     dry_run=dry_run,
        #     print_debug=print_debug
        # )
        _build_using_cmake(
            toolchain=install_info.toolchain,
            cmake_generator=install_info.cmake_generator,
            dependencies_root=install_info.dependencies_root,
            temporary_directory=temp_dir,
            subdirectory=subdir,
            target=install_info.target,
            host_system=install_info.host_system,
            build_variant=install_info.build_variant,
            dry_run=dry_run,
            print_debug=print_debug
        )
    else:
        _build(
            toolchain=install_info.toolchain,
            dependencies_root=install_info.dependencies_root,
            temporary_directory=temp_dir,
            subdirectory=subdir,
            dry_run=dry_run,
            print_debug=print_debug
        )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)
