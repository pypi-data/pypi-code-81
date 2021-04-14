"""
Run a model.
"""
import json
import inspect
import os
import typing
import subprocess
import sys

from pexpect import split_command_line

from dslibrary import ENV_DSLIBRARY_TOKEN
from dslibrary.front import DSLibraryException, ENV_DSLIBRARY_TARGET, ENV_DSLIBRARY_SPEC, METRICS_ALIAS
from dslibrary.metadata import Metadata


class ModelRunner(object):
    """
    Each instance sets up for one run of one model.
    """
    def __init__(self, uri: str=None, user: str=None, run_id: str=None, entry_point: str = "main", mlflow: dict=None):
        """
        The constructor provides some context which is optional when directly invoking local code, and required
        when invoking code remotely.

        :param uri:             Unique identifier for the model.
        :param user:            Which user is running the model.
        :param run_id:          Run ID needs to be specified when running in MLFlow.
        :param entry_point:     Which entry point is being called.
        :param mlflow:          MLFlow-related settings.  True = send all to mlflow, {} = send some calls to mlflow.
        """
        self.uri = uri or ""
        self.user = user or ""
        self.run_id = run_id or ""
        self.entry_point = entry_point
        # TODO document & validate these
        self.mlflow = mlflow if isinstance(mlflow, dict) else {"all": True} if mlflow is True else {}
        self.inputs = {}
        self.outputs = {}
        self.parameters = {}

    def get_metadata(self):
        """
        Obtain metadata for the selected model.
        """
        # TODO code me ... depends quite a bit on where the model is and how it is packaged, not possible without more context

    def _to_absolute(self, uri: str):
        """
        Convert local paths to absolute paths except when they match a certain pattern.
        """
        # TODO test this (and make sure it seems reasonable to use '~')
        if ":" in uri:
            # no changes to URIs
            return uri
        if uri.startswith("~/"):
            # specifically point to files within the sandbox
            return "./" + uri[1:]
        if uri.startswith("/"):
            # already absolute
            return uri
        # convert to absolute path
        return os.path.abspath(uri)

    def set_input(self, name: str, uri: str, **kwargs):
        """
        Specify where data will come from for a particular named input.
        :param name:    Name of input.
        :param uri:     A path to a local file, or the URI of remote data.  Or, a URI specifying a sql or nosql data
                        source.
        :param kwargs:  Additional parameters to support the various data sources, following fsspec for file-like
                        sources.
        """
        self.inputs[name] = {"uri": self._to_absolute(uri), **kwargs}
        return self

    def set_output(self, name: str, uri: str, **kwargs):
        """
        Specify where data should go for a particular named output.

        A format can be chosen by specifying "format".
          csv or tab -- remaining arguments are sent to pandas.to_csv()
          json - remaining arguments are sent to pandas.to_json()
          etc.

        :param name:    Name of output.
        :param uri:     See set_input()
        :param kwargs:  See set_input()
        """
        self.outputs[name] = {"uri": self._to_absolute(uri), **kwargs}
        return self

    def set_parameter(self, name: str, value):
        """
        Specify a value for one of the parameters.
        """
        self.parameters[name] = value
        return self

    def set_parameters(self, params: dict):
        """
        Specify values for multiple parameters.
        """
        self.parameters.update(params)
        return self

    def send_metrics_to(self, uri: str=None, mlflow: bool=None, **kwargs):
        """
        Determine where metrics will be stored (for read and write).  Parameters are equivalent to set_output(), in
        that metrics can be sent to a particular location.

        :param uri:         A URI or filename.
        :param mlflow:      Specify True to have the model log its metrics through MLFlow.
        :param kwargs:      Additional arguments.
        """
        if mlflow is not None:
            self.mlflow["metrics"] = bool(mlflow)
        # TODO shouldn't the input and the output be separate?
        self.inputs[METRICS_ALIAS] = {"uri": uri, **kwargs}
        self.outputs[METRICS_ALIAS] = {"uri": uri, **kwargs}
        return self

    def _generate_spec(self):
        spec = {
            "uri": self.uri,
            "user": self.user,
            "run_id": self.run_id,
            "entry_point": self.entry_point,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "parameters": self.parameters
        }
        if self.mlflow:
            spec["mlflow"] = self.mlflow
        return spec

    def run_method(self, method: typing.Callable, path: str=None):
        """
        As long as the target 'method' does not uses subprocesses or threads, this method can be used to invoke it.
        """
        # store specification
        orig_env = {ENV_DSLIBRARY_TARGET: os.environ.get(ENV_DSLIBRARY_TARGET), ENV_DSLIBRARY_SPEC: os.environ.get(ENV_DSLIBRARY_SPEC)}
        os.environ[ENV_DSLIBRARY_TARGET] = f"local:{path or '.'}"
        os.environ[ENV_DSLIBRARY_SPEC] = json.dumps(self._generate_spec())
        # map parameters to method signature
        call_kwargs = {}
        sig = inspect.signature(method)
        for p_name in sig.parameters:
            if p_name in self.parameters:
                param = sig.parameters[p_name]
                value = self.parameters[p_name]
                if param.annotation:
                    value = param.annotation(value)
                call_kwargs[p_name] = value
        # the method makes calls to dslibrary, following rules set above
        method(**call_kwargs)
        # restore environment
        for k, v in orig_env.items():
            os.environ[k] = v or ""

    def run_local(self, path: str, extra_env: dict=None):
        """
        Execute a python, R or notebook based model in a subprocess.
        """
        # verify target exists, split apart path
        if not os.path.exists(path):
            raise DSLibraryException(f"Path not found: {path}")
        folder, fn = os.path.split(path)
        f_base, f_ext = os.path.splitext(fn)
        # if only a path is specified we can look up 'entry_point' and run its official command
        cmd = None
        if os.path.isdir(path):
            folder, fn = path, ""
            meta = Metadata.from_folder(path)
            entry_point = self.entry_point or "main"
            if entry_point not in meta.entry_points:
                raise DSLibraryException(f"Entry point {entry_point} not found in model at {path}")
            cmd_str = meta.entry_points[entry_point].command
            if not cmd_str:
                raise DSLibraryException(f"Entry point {entry_point} for {path} does not define a command")
            cmd = split_command_line(cmd_str)
        # if we're not using metadata we have to infer how to execute the code
        if not cmd:
            cmd = self.infer_command_from_path(path)
        # work out environment variables
        env = {
            ENV_DSLIBRARY_TARGET: f"local:{folder}",
            ENV_DSLIBRARY_SPEC: json.dumps(self._generate_spec()),
            **(extra_env or {})
        }
        # call the model
        result = subprocess.run(cmd, cwd=folder, env=env, check=True)
        # TODO report failures in a more elegant way

    @staticmethod
    def infer_command_from_path(path: str):
        """
        When we only know the name of a source file we have to work out how to execute it.
        """
        _, fn = os.path.split(path)
        _, f_ext = os.path.splitext(fn)
        f_ext = f_ext.lower()
        # if we're not using metadata we have to infer how to execute the code
        if f_ext == ".py":
            cmd = [sys.executable, path]
        elif f_ext == ".r":
            cmd = ["RScript", path]
        elif f_ext == ".ipynb":
            cmd = ["nbconvert", "--to", "notebook", "--execute", "--inplace", path]
        else:
            raise DSLibraryException(f"unrecognized executable extension: {f_ext} in {fn}")
        return cmd

    def prepare_remote_run(self, local_rest_url: str, rest_access_token: str=None) -> dict:
        """
        Generically prepare for a remote run, assuming the remote will use make REST calls to access its data.  Returns
        the environment variables that must be set when the remote executes.  These can go in a k8s job spec, for
        instance.
        :param local_rest_url:  URL of REST service.
        :param rest_access_token: Access token to secure communications.
        :return:  Environment variables to set, as a {}.
        """
        env = {}
        if local_rest_url:
            env[ENV_DSLIBRARY_TARGET] = local_rest_url
        if rest_access_token:
            env[ENV_DSLIBRARY_TOKEN] = rest_access_token
        env[ENV_DSLIBRARY_SPEC] = json.dumps(self._generate_spec())
        return env

    def run_mlflow(self, model_uri: str):
        """
        Use mlflow.run() to execute an MLFlow model.

        The trick will be how to set the environment variables in the remote model such that the interception takes
        place and sends data back to us.  Could initially only be supported when running locally with an environment
        variable.
        """
        # TODO code me
