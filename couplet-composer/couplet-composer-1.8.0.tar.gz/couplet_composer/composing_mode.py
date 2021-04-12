# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for running the
composing mode of the script.
"""

import logging
import os
import stat

from .compose import libraries

from .dependencies import googletest

from .support.cmake_generators import \
    get_ninja_cmake_generator_name, get_visual_studio_16_cmake_generator_name

from .support.environment import \
    get_artefact_directory, get_build_root, get_composing_directory, \
    get_destination_directory, get_documentation_directory, \
    get_running_directory, get_temporary_directory

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from .support.project_values import get_scripts_base_directory_name

from .util import shell


def create_composing_root(
    source_root,
    in_tree_build,
    target,
    cmake_generator,
    build_variant
):
    """
    Checks if the directory for the actual build of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    in_tree_build -- Whether the build files are created in-tree.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.
    """
    composing_root = get_composing_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=in_tree_build
        ),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant
    )
    if not os.path.exists(composing_root):
        shell.makedirs(path=composing_root)
    return composing_root


def create_destination_root(
    source_root,
    in_tree_build,
    target,
    cmake_generator,
    build_variant,
    version
):
    """
    Checks if the directory for the built products of the project
    exists and creates it if it doesn't exist. Returns the path
    to the created directory.

    source_root -- Path to the directory that is the root of the
    script run.

    in_tree_build -- Whether the build files are created in-tree.

    target -- The target system of the build represented by a
    Target.

    cmake_generator -- The CMake generator that is used.

    build_variant -- The build variant used to build the project.

    version -- The version number of the project.
    """
    destination_root = get_destination_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=in_tree_build
        ),
        target=target,
        cmake_generator=cmake_generator,
        build_variant=build_variant,
        version=version
    )
    if not os.path.exists(destination_root):
        shell.makedirs(path=destination_root)
    return destination_root


def _create_cmake_call(
    toolchain,
    arguments,
    host_system,
    project_root,
    destination_root,
    dependencies_root
):
    """
    Creates the CMake call that is used to generate the build
    files for the project.

    toolchain -- The toolchain object of the run.

    arguments -- The parsed command line arguments of the run.

    host_system -- The system this script is run on.

    project_root -- The root directory of the project this script
    acts on.

    destination_root -- The directory where the built product is
    placed in.

    dependencies_root -- The directory for the dependencies.
    """
    cmake_call = [
        toolchain.cmake,
        project_root,
        "-G",
        arguments.cmake_generator,
        "-DCMAKE_BUILD_TYPE={}".format(arguments.build_variant),
        "-DCMAKE_INSTALL_PREFIX={}".format(
            destination_root.replace("\\", "/")
            if host_system == get_windows_system_name() else destination_root
        ),
        "-DODE_BUILD_TEST={}".format("ON" if arguments.build_test else "OFF"),
        "-DODE_TEST_BENCHMARKING={}".format(
            "ON" if arguments.build_benchmark else "OFF"
        ),
        "-DODE_BUILD_DOCS={}".format(
            "ON" if arguments.build_docs and toolchain.doxygen else "OFF"
        ),
        "-DODE_CODE_COVERAGE={}".format("ON" if arguments.coverage else "OFF"),
        "-DODE_BUILD_STATIC={}".format(
            "ON" if arguments.build_ode_static_lib else "OFF"
        ),
        "-DODE_BUILD_SHARED={}".format(
            "ON" if arguments.build_ode_shared_lib else "OFF"
        ),
        "-DANTHEM_BUILD_STATIC={}".format(
            "ON" if arguments.build_anthem_static_lib else "OFF"
        ),
        "-DANTHEM_BUILD_SHARED={}".format(
            "ON" if arguments.build_anthem_shared_lib else "OFF"
        ),
        "-DODE_DEVELOPER={}".format(
            "ON" if arguments.developer_build else "OFF"
        ),
        "-DODE_TEST_USE_NULL_SINK={}".format(
            "ON" if not arguments.test_logging else "OFF"
        ),
        # TODO Maybe have some more sophisticated way to set this
        # option
        "-DODE_DISABLE_GL_CALLS={}".format(
            "ON" if host_system == get_linux_system_name() and os.getenv(
                "GITHUB_ACTIONS",
                None
            ) else "OFF"
        ),
        "-DODE_CXX_VERSION={}".format(arguments.std),
        "-DODE_DEPENDENCY_PREFIX={}".format(
            dependencies_root.replace("\\", "/")
            if host_system == get_windows_system_name() else dependencies_root
        ),
        "-DODE_VERSION={}".format(arguments.ode_version),
        "-DANTHEM_VERSION={}".format(arguments.anthem_version),
        "-DODE_OPENGL_VERSION_MAJOR={}".format(
            arguments.opengl_version.split(".")[0]
        ),
        "-DODE_OPENGL_VERSION_MINOR={}".format(
            arguments.opengl_version.split(".")[1]
        ),
        "-DODE_SCRIPTS_BASE_DIRECTORY={}".format(
            get_scripts_base_directory_name(coverage=arguments.coverage)
        ),
        "-DODE_NAME={}".format(arguments.ode_binaries_name),
        "-DANTHEM_NAME={}".format(arguments.anthem_binaries_name)
    ]

    if host_system != get_windows_system_name():
        cmake_call.extend(["-DCMAKE_C_COMPILER={}".format(
            toolchain.compiler["cc"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])
        cmake_call.extend(["-DCMAKE_CXX_COMPILER={}".format(
            toolchain.compiler["cxx"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])

    if arguments.cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend(
            ["-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)]
        )

    if host_system == get_darwin_system_name():
        cmake_call.extend(["-DODE_RPATH=@loader_path"])
    elif host_system == get_linux_system_name():
        cmake_call.extend(["-DODE_RPATH=$ORIGIN"])

    if host_system == get_windows_system_name():
        if os.path.exists(os.path.join(dependencies_root, "lib", "SDL2d.lib")):
            cmake_call.extend(["-DODE_USE_SDL_DEBUG_SUFFIX=ON"])
        else:
            cmake_call.extend(["-DODE_USE_SDL_DEBUG_SUFFIX=OFF"])

    if googletest.should_add_sources_to_project(host_system=host_system):
        cmake_call.extend(["-DODE_ADD_GOOGLE_TEST_SOURCE=ON"])
        cmake_call.extend(["-DODE_GOOGLE_TEST_DIRECTORY={}".format(
            googletest.get_dependency_source_directory(
                dependencies_root=dependencies_root
            )
        )])
    else:
        cmake_call.extend(["-DODE_ADD_GOOGLE_TEST_SOURCE=OFF"])

    if arguments.lint:
        if toolchain.linter:
            cmake_call.extend(["-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
        else:
            cmake_call.extend(["-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
            logging.warning(
                "Couplet Composer should perform linting, but clang-tidy "
                "wasn't found"
            )
    else:
        cmake_call.extend(["-DCMAKE_EXPORT_COMPILE_COMMANDS=OFF"])

    if arguments.skip_build:
        cmake_call.extend(["-DODE_SKIP_BUILD=ON"])
    else:
        cmake_call.extend(["-DODE_SKIP_BUILD=OFF"])

    # if host_system == get_windows_system_name():
    #     cmake_call.extend(["-DODE_MSVC_RUNTIME_LIBRARY=MultiThreadedDebug"])

    return cmake_call


def compose_project(
    source_root,
    toolchain,
    arguments,
    host_system,
    project_root,
    build_root,
    composing_root,
    destination_root,
    dependencies_root
):
    """
    Builds the project this script acts on.

    source_root -- Path to the directory that is the root of the
    script run.

    toolchain -- The toolchain object of the run.

    arguments -- The parsed command line arguments of the run.

    host_system -- The system this script is run on.

    project_root -- The root directory of the project this script
    acts on.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    composing_root -- The directory for the actual build of the
    project.

    destination_root -- The directory where the built product is
    placed in.

    dependencies_root -- The directory for the dependencies.
    """
    cmake_call = _create_cmake_call(
        toolchain=toolchain,
        arguments=arguments,
        host_system=host_system,
        project_root=project_root,
        destination_root=destination_root,
        dependencies_root=dependencies_root
    )

    if host_system != get_windows_system_name():
        if isinstance(toolchain.compiler, dict):
            cmake_env = {
                "CC": toolchain.compiler["cc"],
                "CXX": toolchain.compiler["cxx"]
            }
        else:
            cmake_env = {"CC": toolchain.compiler, "CXX": toolchain.compiler}
    else:
        cmake_env = None

    with shell.pushd(composing_root):
        shell.call(
            cmake_call,
            env=cmake_env,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        if arguments.lint and toolchain.linter:
            run_clang_tidy = os.path.join(
                os.path.dirname(__file__),
                "llvm",
                "run-clang-tidy.py"
            )
            shell.chmod(
                run_clang_tidy,
                stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            clang_tidy_call = [
                run_clang_tidy,
                "-clang-tidy-binary",
                toolchain.linter,
                "-j",
                str(arguments.jobs)
            ]
            if arguments.export_linter_fixes:
                if toolchain.linter_replacements:
                    clang_tidy_call.extend([
                        "-clang-apply-replacements-binary",
                        toolchain.linter_replacements,
                        "-export-fixes",
                        os.path.join(
                            source_root,
                            arguments.export_linter_fixes
                        )
                    ])
                else:
                    logging.warning(
                        "Couplet Composer should export diagnostics from "
                        "clang-tidy, but clang-apply-replacements wasn't found"
                    )
            shell.call(
                clang_tidy_call,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        if arguments.skip_build:
            return
        if arguments.cmake_generator \
                == get_visual_studio_16_cmake_generator_name():
            logging.debug(
                "The build directory contains the following files and "
                "directories:\n%s",
                "\n".join([f for f in os.listdir(composing_root)])
            )
            shell.call(
                [
                    toolchain.build_system,
                    "anthem.sln",
                    "/property:Configuration={}".format(
                        arguments.build_variant
                    )
                ],
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            anthem_executable_name = "{}.exe".format(
                arguments.anthem_binaries_name
            )
            anthem_executable = os.path.join(
                destination_root,
                "bin",
                anthem_executable_name
            )
            if os.path.exists(anthem_executable):
                shell.rm(
                    anthem_executable,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            test_executable_name = "test-{}.exe".format(
                arguments.anthem_binaries_name
            )
            test_executable = os.path.join(
                destination_root,
                "bin",
                test_executable_name
            )
            if os.path.exists(test_executable):
                shell.rm(
                    test_executable,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )
            shell.makedirs(
                os.path.join(destination_root, "bin"),
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copy(
                os.path.join(
                    composing_root,
                    arguments.build_variant,
                    anthem_executable_name
                ),
                anthem_executable,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.copy(
                os.path.join(
                    composing_root,
                    arguments.build_variant,
                    test_executable_name
                ),
                test_executable,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

            libraries.copy_scripts(
                path=destination_root,
                arguments=arguments,
                project_root=project_root
            )
        else:
            shell.call(
                [toolchain.build_system],
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            shell.call(
                [toolchain.build_system, "install"],
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
            if arguments.coverage:
                libraries.copy_scripts(
                    path=composing_root,
                    arguments=arguments,
                    project_root=project_root
                )
                libraries.copy_sdl_libraries(
                    path=composing_root,
                    arguments=arguments,
                    host_system=host_system,
                    project_root=project_root,
                    dependencies_root=dependencies_root
                )
                coverage_env = {}
                coverage_call = []
                if arguments.enable_xvfb:
                    coverage_env.update({"SDL_VIDEODRIVER": "x11"})
                    coverage_env.update({"DISPLAY": ":99.0"})
                    coverage_call.extend([
                        toolchain.xvfb,
                        "-n",
                        "99",
                        "--server-args",
                        "-screen 0 1920x1080x24 +extension GLX",
                        "-e",
                        "/dev/stdout"
                    ])
                coverage_call.extend([
                    toolchain.build_system,
                    "{}_coverage".format(arguments.anthem_binaries_name)
                ])
                shell.call(
                    coverage_call,
                    env=coverage_env,
                    dry_run=arguments.dry_run,
                    echo=arguments.print_debug
                )

    shell.copytree(
        os.path.join(project_root, "util", "bin"),
        os.path.join(destination_root, "bin"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    launch_file = os.path.join(destination_root, "bin", "launch")
    launch_test_file = os.path.join(destination_root, "bin", "launch_test")

    mode_launch = os.stat(launch_file).st_mode
    os.chmod(
        launch_file,
        mode_launch | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )

    mode_launch_test = os.stat(launch_test_file).st_mode
    os.chmod(
        launch_test_file,
        mode_launch_test | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )

    libraries.copy_sdl_libraries(
        path=os.path.join(destination_root, "bin"),
        arguments=arguments,
        host_system=host_system,
        source_root=source_root,
        project_root=project_root,
        dependencies_root=dependencies_root
    )


def install_running_copies(arguments, build_root, destination_root):
    """
    Installs the built products to the running directories.

    arguments -- The parsed command line arguments of the run.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    destination_root -- The directory where the built product is
    placed in.
    """
    running_path = get_running_directory(build_root=build_root)

    if os.path.exists(running_path):
        shell.rmtree(
            running_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        running_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(destination_root, "bin"),
        running_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.makedirs(
        os.path.join(running_path, "lib"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(destination_root, "lib"),
        os.path.join(running_path, "lib"),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )


def install_documentation(arguments, build_root, composing_root):
    """
    Installs the built Doxygen to its destination directories.

    arguments -- The parsed command line arguments of the run.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    composing_root -- The directory for the actual build of the
    project.
    """
    docs_path = get_documentation_directory(build_root=build_root)
    html_path = os.path.join(docs_path, "html")

    if os.path.exists(html_path):
        shell.rmtree(
            html_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        html_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.copytree(
        os.path.join(composing_root, "docs", "doxygen", "html"),
        html_path,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )


def create_artefacts(arguments, host_system, build_root):
    """
    Creates the artefacts of the built products.

    arguments -- The parsed command line arguments of the run.

    host_system -- The system this script is run on.

    build_root -- The path to the root directory that is used for
    all created files and directories.
    """
    artefact_base_name = "{}-{}-{}".format(
        arguments.anthem_artefacts_name,
        arguments.anthem_version,
        arguments.host_target
    )

    use_dir = arguments.use_artefact_directory
    artefact_name = artefact_base_name if use_dir else "{}.{}".format(
        artefact_base_name,
        "zip" if host_system == get_windows_system_name() else "tar.gz"
    )
    artefact_dir = get_artefact_directory(build_root=build_root)
    artefact_path = os.path.join(artefact_dir, artefact_name)

    if os.path.exists(artefact_path):
        if use_dir:
            shell.rmtree(
                artefact_path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        else:
            shell.rm(
                artefact_path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

    shell.makedirs(
        artefact_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    tmp_dir = get_temporary_directory(build_root=build_root)
    tmp_subdir = "{}-{}-{}".format(
        arguments.anthem_artefacts_name,
        arguments.anthem_version,
        arguments.host_target
    )

    if os.path.exists(tmp_dir):
        shell.rmtree(
            tmp_dir,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )

    shell.makedirs(
        tmp_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.makedirs(
        os.path.join(tmp_dir, tmp_subdir),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    running_path = get_running_directory(build_root=build_root)

    shell.copytree(
        running_path,
        os.path.join(tmp_dir, tmp_subdir),
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )

    if use_dir:
        shell.copytree(
            os.path.join(tmp_dir, tmp_subdir),
            artefact_path,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    else:
        if host_system == get_windows_system_name():
            shell.create_zip(
                os.path.join(tmp_dir, tmp_subdir),
                artefact_path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )
        else:
            shell.create_tar(
                os.path.join(tmp_dir, tmp_subdir),
                artefact_path,
                dry_run=arguments.dry_run,
                echo=arguments.print_debug
            )

    shell.rmtree(
        tmp_dir,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
