"""
The compiler package allows to compile built API specifications into SDKs,
documents or other utilities.
"""

import abc
import typing
import os
import sys
import imp
import pydoc
import logging
import inspect
import shutil

from portapy.core import API

from .template import Renderer


class IAction(metaclass=abc.ABCMeta):
    """
    This interface can be implemented to provide actions to manifests.
    """

    @abc.abstractmethod
    def run(self, compiler: 'Compiler') -> None:
        """
        Method to implement to implement an action.
        """


class Compile(IAction):
    """
    This action compiles another manifest.
    """

    def __init__(self, build_dir: str, manifest: typing.Union[str, 'Manifest']) -> None:
        """
        The *build_dir* describes where the project will be compiled. It is relative to
        the current build directory.

        The *manifest* argument is passed to the `Compiler` instance.
        """
        self.build_dir = build_dir
        self.manifest = manifest

    def run(self, compiler: 'Compiler') -> None:
        """
        Compile the project.
        """
        compiler.logger.info('compiling project dependency: %s', self.manifest)
        new_compiler = Compiler(compiler.api, self.build_dir)
        new_compiler.run(self.manifest)


class Function(IAction):
    """
    This action executes a Python function.
    """

    def __init__(self, func_: typing.Callable, *args, **kwargs):
        """
        The *_func* argument is the function to execute, and the *args* and *kwargs*
        arguments are the arguments to pass to it at runtime.
        """
        self.func = func_
        self.args = args
        self.kwargs = kwargs

    def run(self, compiler: 'Compiler') -> None:
        """
        Execute the given function.
        """
        compiler.logger.info('running function: %s.%s, args=%s, kwargs=%s',
                             self.func.__module__, self.func.__name__, self.args, self.kwargs)
        self.func(*self.args, **self.kwargs)


class Template(IAction):
    """
    This action templates a specific file using Jinja2.
    """

    def __init__(self, src: str, dest: str = None, *args, keep: bool = True,
                 filemode: str = 'w', **kwargs) -> None:
        """
        The *src* argument is the source template file. The *dest* argument is
        where to save the file after it's templated. If omitted, it uses and
        thus overwrites the same filename as the source.

        If *keep* is false, the original template is deleted afterwards.

        The *filemode* is the mode to use when opening the destination file.
        This allows appending, per example.

        The *args* and *kwargs* arguments are passed to the `Renderer` instance,
        """
        self.src = src
        self.dest = dest or src
        self.keep = keep
        self.filemode = filemode
        self.args = args
        self.kwargs = kwargs

    def run(self, compiler: 'Compiler') -> None:
        """
        Compile the template.
        """
        compiler.logger.info('compiling template: %s -> %s', self.src, self.dest)

        kwargs = dict(self.kwargs)
        if 'data' not in kwargs:
            kwargs['data'] = {}
        kwargs['data']['config'] = compiler.config

        renderer = Renderer(compiler.api, *self.args, **kwargs)
        output = renderer.render(self.src)
        with open(self.dest, self.filemode) as fp:
            fp.write(output)

        if not self.keep:
            compiler.logger.info('removing source template: %s', self.src)
            os.unlink(self.src)


class Shell(IAction):
    """
    This action executes shell commands in the compiler distribution directory.
    """

    def __init__(self, cmd: str) -> None:
        """
        The *cmd* is the command to execute.
        """
        self.cmd = cmd

    def run(self, compiler: 'Compiler') -> None:
        """
        Run a shell command.
        """
        exitcode = os.system(self.cmd)
        if hasattr(os, 'WEXITSTATUS'):
            exitcode = os.WEXITSTATUS(exitcode)
        if exitcode != 0:
            sys.exit(exitcode)


class Manifest():
    """
    The manifest describes the actions to take in order to compile an API into
    a SDK.
    """

    instance: 'Manifest' = None
    """ Stores the last manifest instance. """

    def __init__(self, *args: IAction, src_dir: str = '', dist_dir: str = 'dist',
                 config_vars: typing.List[str] = None) -> None:
        """
        Initialize the manifest using the specified actions.

        The *src_dir* argument is the directory containing the source to copy to the
        build directory, relative to where the manifest is declared.

        The *dist_dir* argument is the path where the distribution will be generated.

        This *config_vars* argument is a list of required configuration values.
        """
        self.actions = list(args)
        self.src_dir = src_dir
        self.dist_dir = dist_dir
        self.config_vars = config_vars or []
        self.__class__.instance = self
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        self.filename = calframe[1].filename

    def get(self, cls: typing.Type) -> typing.List[IAction]:
        """
        Get actions of a specific type from the manifest.
        """
        result = []
        for action in self.actions:
            if isinstance(action, cls):
                result.append(action)
        return result


class Compiler():
    """
    The compiler class executes manifests.
    """

    def __init__(self, api: API, build_dir: str = 'build', config: dict = None) -> None:
        """
        Initialize the compiler.

        The *api* argument is the API object to compile.

        The *build_dir* argument is the path used to build the source. The
        path is recursively deleted and re-created at each compilation.

        The *config* argument is a dictionary containing configuration values.
        """
        self.api = api
        self.build_dir = build_dir
        self.config = config or {}
        self.logger = logging.getLogger(self.__module__)

    def run(self, manifest: typing.Union[Manifest, str] = None) -> None:
        """
        Compile using a manifest.

        The *manifest* argument can either be a `Manifest` object, a filesystem
        path containing a manifest, a Python module containing a manifest or
        `None`. The the last case, the last manifest to be declared is used.
        """
        spec = manifest
        if manifest is None:
            manifest = Manifest.instance
        else:
            Manifest.instance = None

        if isinstance(manifest, str):
            if os.path.exists(manifest):
                imp.load_source('<manifest>', manifest)
                manifest = Manifest.instance
            else:
                manifest = pydoc.locate(manifest)
                manifest = Manifest.instance

        if manifest is None:
            raise IOError('no manifest found using spec: %s', spec)

        for key in manifest.config_vars:
            if key not in self.config:
                raise EnvironmentError('missing configuration value: %s' % key)

        cwd = os.getcwd()
        build_dir = os.path.realpath(self.build_dir)
        self.logger.info('starting compiler, using build dir: %s', build_dir)

        self.logger.info('using manifest: %s', manifest.filename)
        source_dir = os.path.dirname(manifest.filename)
        source_dir = os.path.join(source_dir, manifest.src_dir)

        if os.path.exists(build_dir):
            self.logger.info('removing build directory')
            shutil.rmtree(build_dir)

        self.logger.info('copying source data: %s -> %s',
                         source_dir, build_dir)
        shutil.copytree(source_dir, build_dir)

        try:
            self.logger.info('changing directory to: %s', build_dir)
            os.chdir(build_dir)
            dist_dir = os.path.realpath(manifest.dist_dir)

            for action in manifest.actions:
                self.logger.info('executing action: %s', action.__class__.__name__)
                action.run(self)

        finally:
            os.chdir(cwd)

        self.logger.info('build success!')
        self.logger.info('build is available in: %s', dist_dir)
