#!python


# builtin
import contextlib
import os
import logging
import time
import copy
# external
import click
# local
import alphatims
import alphatims.utils


@contextlib.contextmanager
def parse_cli_settings(command_name: str, **kwargs):
    """A context manager that parses and logs CLI settings.

    Parameters
    ----------
    command_name : str
        The name of the command that utilizes these CLI settings.
    **kwargs
        All values that need to be logged.
        Values (if included) that explicitly will be parsed are:
            output_folder
            threads
            disable_log_stream
            log_file
            parameter_file
            export_parameters

    Returns
    -------
    : dict
        A dictionary with parsed parameters.
    """
    try:
        start_time = time.time()
        kwargs = {key: arg for key, arg in kwargs.items() if arg is not None}
        if "output_folder" in kwargs:
            if kwargs["output_folder"] is not None:
                kwargs["output_folder"] = os.path.abspath(
                    kwargs["output_folder"]
                )
                if not os.path.exists(kwargs["output_folder"]):
                    os.makedirs(kwargs["output_folder"])
                if "log_file" not in kwargs:
                    kwargs["log_file"] = kwargs["output_folder"]
                elif kwargs["log_file"] == "":
                    kwargs["log_file"] = kwargs["output_folder"]
        if ("parameter_file" in kwargs):
            kwargs["parameter_file"] = os.path.abspath(
                kwargs["parameter_file"]
            )
            parameters = alphatims.utils.load_parameters(
                kwargs["parameter_file"]
            )
            kwargs.update(parameters)
        if "threads" not in kwargs:
            kwargs["threads"] = alphatims.utils.INTERFACE_PARAMETERS[
                "threads"
            ]["default"]
        kwargs["threads"] = alphatims.utils.set_threads(
            kwargs["threads"]
        )
        if "log_file" not in kwargs:
            kwargs["log_file"] = alphatims.utils.INTERFACE_PARAMETERS[
                "log_file"
            ]["default"]
        if "disable_log_stream" not in kwargs:
            kwargs[
                "disable_log_stream"
            ] = alphatims.utils.INTERFACE_PARAMETERS[
                "disable_log_stream"
            ]["default"]
        kwargs["log_file"] = alphatims.utils.set_logger(
            log_file_name=kwargs["log_file"],
            stream=not kwargs["disable_log_stream"],
        )
        alphatims.utils.show_platform_info()
        alphatims.utils.show_python_info()
        alphatims.utils.check_github_version()
        logging.info(
            f"Running CLI command `alphatims "
            f"{command_name}` with parameters:"
        )
        max_len = max(len(key) + 1 for key in kwargs)
        for key, value in sorted(kwargs.items()):
            # if (isinstance(value, tuple)) and (len(value) > 1):
            #     key += "s"
            logging.info(f"{key:<{max_len}} - {value}")
        logging.info("")
        if "export_parameters" in kwargs:
            if kwargs["export_parameters"] is not None:
                kwargs["export_parameters"] = os.path.abspath(
                    kwargs["export_parameters"]
                )
                alphatims.utils.save_parameters(
                    kwargs["export_parameters"],
                    kwargs
                )
        yield kwargs
    except Exception:
        logging.exception("Something went wrong, execution incomplete!")
    else:
        logging.info(
            f"Analysis done in {time.time() - start_time:.2f} seconds."
        )
    finally:
        alphatims.utils.set_logger(log_file_name=None)


def cli_option(
    parameter_name: str,
    as_argument: bool = False,
    **kwargs
):
    """A wrapper for click.options and click.arguments using local defaults.

    Parameters
    ----------
    parameter_name : str
        The name of the parameter or argument.
        It's default values need to be present in
        lib/interface_parameters.json.
    as_argument : bool
        If True, a click.argument is returned.
        If False, a click.option is returned.
        Default is False.
    **kwargs
        Items that overwrite the default values of
        lib/interface_parameters.json.
        These need to be valid items for click.
        A special "type" dict can be used to pass a click.Path or click.Choice,
        that has the following format:
        type = {"name": "path" or "choice", **choice_or_path_kwargs}

    Returns
    -------
    : click.option, click.argument
        A click.option or click.argument decorator.
    """
    parameters = copy.deepcopy(
        alphatims.utils.INTERFACE_PARAMETERS[parameter_name]
    )
    parameters.update(kwargs)
    if "type" in parameters:
        if parameters["type"] == "int":
            parameters["type"] = int
        elif parameters["type"] == "float":
            parameters["type"] = float
        elif parameters["type"] == "str":
            parameters["type"] = str
        elif isinstance(parameters["type"], dict):
            parameter_type = parameters["type"].pop("name")
            if parameter_type == "path":
                parameters["type"] = click.Path(**parameters["type"])
                if ("default" in parameters) and (parameters["default"]):
                    parameters["default"] = os.path.join(
                        os.path.dirname(__file__),
                        parameters["default"]
                    )
            elif parameter_type == "choice":
                options = parameters["type"].pop("options")
                parameters["type"] = click.Choice(
                    options,
                    **parameters["type"]
                )
    if "default" in parameters:
        if "is_flag" in parameters:
            parameters["show_default"] = False
        else:
            parameters["show_default"] = True
    if not as_argument:
        if "short_name" in parameters:
            short_name = parameters.pop("short_name")
            return click.option(
                f"--{parameter_name}",
                f"-{short_name}",
                **parameters,
            )
        else:
            return click.option(
                f"--{parameter_name}",
                **parameters,
            )
    else:
        if "nargs" in parameters:
            return click.argument(
                parameter_name,
                type=click.Path(exists=True),
                nargs=parameters["nargs"],
                required=True
            )
        else:
            return click.argument(
                parameter_name,
                type=parameters["type"],
                required=True
            )


@click.group(
    context_settings=dict(
        help_option_names=['-h', '--help'],
    ),
    invoke_without_command=True
)
@click.pass_context
@click.version_option(alphatims.__version__, "-v", "--version")
def run(ctx, **kwargs):
    name = f"AlphaTims {alphatims.__version__}"
    click.echo("*" * (len(name) + 4))
    click.echo(f"* {name} *")
    click.echo("*" * (len(name) + 4))
    if ctx.invoked_subcommand is None:
        click.echo(run.get_help(ctx))


@run.command("gui", help="Start graphical user interface.")
def gui():
    with parse_cli_settings("gui"):
        logging.info("Loading GUI..")
        import alphatims.gui
        alphatims.gui.run()


@run.group("export", help="Export information.")
def export(**kwargs):
    pass


@run.group("detect", help="Detect structures within the data.")
def detect(**kwargs):
    pass


@export.command("hdf", help="Export BRUKER_D_FOLDER as hdf file.")
@cli_option("bruker_d_folder", as_argument=True)
@cli_option("disable_overwrite")
@cli_option("enable_compression")
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def export_hdf(**kwargs):
    with parse_cli_settings("export hdf", **kwargs) as parameters:
        import alphatims.bruker
        data = alphatims.bruker.TimsTOF(parameters["bruker_d_folder"])
        if "output_folder" not in parameters:
            directory = data.directory
        else:
            directory = parameters["output_folder"]
        data.save_as_hdf(
            overwrite=not parameters["disable_overwrite"],
            directory=directory,
            file_name=f"{data.sample_name}.hdf",
            compress=parameters["enable_compression"],
        )


@export.command("mgf", help="Export BRUKER_D_FOLDER as (profile) mgf file.")
@cli_option("bruker_d_folder", as_argument=True)
@cli_option("keep_n_most_abundant_peaks")
@cli_option("centroiding_window")
@cli_option("disable_overwrite")
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def export_mgf(**kwargs):
    with parse_cli_settings("export mgf", **kwargs) as parameters:
        import alphatims.bruker
        data = alphatims.bruker.TimsTOF(parameters["bruker_d_folder"])
        if "output_folder" not in parameters:
            directory = data.directory
        else:
            directory = parameters["output_folder"]
        data.save_as_mgf(
            overwrite=not parameters["disable_overwrite"],
            directory=directory,
            file_name=f"{data.sample_name}.mgf",
            centroiding_window=parameters["centroiding_window"],
            keep_n_most_abundant_peaks=parameters["keep_n_most_abundant_peaks"]
        )


@export.command(
    "selection",
    help="Load a BRUKER_D_FOLDER and select a data slice for export."
)
@cli_option(
    "bruker_d_folder",
    as_argument=True,
    type={
        "name": "path",
        "exists": True,
        "file_okay": True,
        "dir_okay": True
    }
)
@cli_option("ion_type")
@cli_option("rt_bounds")
@cli_option("mobility_bounds")
@cli_option("precursor_bounds")
@cli_option("quad_mz_bounds")
@cli_option("tof_mz_bounds")
@cli_option("intensity_bounds")
@cli_option("x_axis")
@cli_option("y_axis")
@cli_option("format")
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def export_selection(**kwargs):
    import numpy as np
    with parse_cli_settings("export selection", **kwargs) as parameters:
        import alphatims.bruker
        import alphatims.plotting
        import holoviews as hv
        data = alphatims.bruker.TimsTOF(parameters["bruker_d_folder"])
        if (parameters["rt_bounds"][0] is not None):
            if (parameters["rt_bounds"][0] < 0):
                parameters["rt_bounds"] = (
                    int(-parameters["rt_bounds"][0]),
                    int(-parameters["rt_bounds"][1]),
                )
        if (parameters["mobility_bounds"][0] is not None):
            if (parameters["mobility_bounds"][0] < 0):
                parameters["mobility_bounds"] = (
                    int(-parameters["mobility_bounds"][0]),
                    int(-parameters["mobility_bounds"][1]),
                )
        if (parameters["tof_mz_bounds"][0] is not None):
            if (parameters["tof_mz_bounds"][0] < 0):
                parameters["tof_mz_bounds"] = (
                    int(-parameters["tof_mz_bounds"][0]),
                    int(-parameters["tof_mz_bounds"][1]),
                )
        frame_values = alphatims.bruker.convert_slice_key_to_int_array(
            data, slice(*parameters["rt_bounds"]), "frame_indices"
        )
        scan_values = alphatims.bruker.convert_slice_key_to_int_array(
            data, slice(*parameters["mobility_bounds"]), "scan_indices"
        )
        if "precursors" in parameters["ion_type"]:
            quad_values = np.array([[-1, 0]])
            precursor_values = np.array([[0, 1, 1]])
        else:
            quad_values = np.empty(shape=(0, 2), dtype=np.float64)
            precursor_values = np.empty(shape=(0, 3), dtype=np.int64)
        if "fragments" in parameters["ion_type"]:
            quad_values_ = alphatims.bruker.convert_slice_key_to_float_array(
                slice(*parameters["quad_mz_bounds"])
            )
            precursor_values_ = alphatims.bruker.convert_slice_key_to_int_array(
                data,
                slice(*parameters["precursor_bounds"]),
                "precursor_indices"
            )
            if precursor_values_[0, 0] < 1:
                precursor_values_[0, 0] = 1
            quad_values = np.vstack([quad_values, quad_values_])
            precursor_values = np.vstack([precursor_values, precursor_values_])
        tof_values = alphatims.bruker.convert_slice_key_to_int_array(
            data, slice(*parameters["tof_mz_bounds"]), "tof_indices"
        )
        intensity_values = alphatims.bruker.convert_slice_key_to_float_array(
            slice(*parameters["intensity_bounds"])
        )
        logging.info("Filtering datapoints.")
        strike_indices = alphatims.bruker.filter_indices(
            frame_slices=frame_values,
            scan_slices=scan_values,
            precursor_slices=precursor_values,
            tof_slices=tof_values,
            quad_slices=quad_values,
            intensity_slices=intensity_values,
            frame_max_index=data.frame_max_index,
            scan_max_index=data.scan_max_index,
            push_indptr=data.push_indptr,
            precursor_indices=data.precursor_indices,
            quad_mz_values=data.quad_mz_values,
            quad_indptr=data.quad_indptr,
            tof_indices=data.tof_indices,
            intensities=data.intensity_values
        )
        df = data.as_dataframe(strike_indices)
        logging.info(f"Selected {len(df)} datapoints.")
        if "output_folder" not in parameters:
            output_folder = data.directory
        else:
            output_folder = parameters["output_folder"]
        output_file_name_base = os.path.join(
            output_folder,
            f"{data.sample_name}_selection"
        )
        if "csv" in parameters['format']:
            logging.info(f"Exporting results to {output_file_name_base}.csv")
            df.to_csv(f"{output_file_name_base}.csv", index=False)
        if ("html" in parameters['format']) or ("png" in parameters['format']):
            labels = {
                "tof_mz": "mz",
                "rt": "rt",
                "mobility": "mobility",
                "intensity": "intensity",
            }
            x_axis = labels[parameters["x_axis"]]
            y_axis = labels[parameters["y_axis"]]
            if y_axis == "intensity":
                plot = alphatims.plotting.line_plot(
                    data,
                    strike_indices,
                    x_axis,
                    data.sample_name,
                )
            else:
                plot = alphatims.plotting.heatmap(
                    df,
                    x_axis,
                    y_axis,
                    data.sample_name,
                )
            if "html" in parameters['format']:
                logging.info(
                    f"Exporting results to {output_file_name_base}.html"
                )
                hv.save(plot, f"{output_file_name_base}.html")
            if "png" in parameters['format']:
                logging.info(
                    f"Exporting results to {output_file_name_base}.png"
                )
                hv.save(plot, f"{output_file_name_base}.png", fmt="png")


@detect.command("ions", help="Detect ions (NotImplemented yet).")
@cli_option("bruker_d_folder", as_argument=True)
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def detect_ions(**kwargs):
    with parse_cli_settings("detect ions", **kwargs) as parameters:
        raise NotImplementedError


@detect.command("features", help="Detect features (NotImplemented yet).")
@cli_option("bruker_d_folder", as_argument=True)
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def detect_features(**kwargs):
    with parse_cli_settings("detect features", **kwargs) as parameters:
        raise NotImplementedError


@detect.command("analytes", help="Detect analytes (NotImplemented yet).")
@cli_option("bruker_d_folder", as_argument=True)
@cli_option("output_folder")
@cli_option("log_file")
@cli_option("threads")
@cli_option("disable_log_stream")
@cli_option("parameter_file")
@cli_option("export_parameters")
def detect_analytes(**kwargs):
    with parse_cli_settings("detect analytes", **kwargs) as parameters:
        raise NotImplementedError
