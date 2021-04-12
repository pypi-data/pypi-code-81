#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import argparse
from pypushflow.representation.scheme.ows_parser import OwsParser
from pypushflow import Workflow
import est.version
import pypushflow.version
import subprocess
import os

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def _convert(scheme, output_file, overwrite):
    """

    :param scheme:
    :param scan:
    :param timeout:
    :return:
    """
    _logger.warning("translate {} to {}".format(scheme, output_file))

    if os.path.exists(output_file):
        if overwrite is True:
            os.remove(output_file)
        else:
            raise ValueError("{} already exists.".format(output_file))

    with open(output_file, "w+") as file_:
        file_.write(_dump_info_generation())

    workflow = Workflow.ProcessableWorkflow(scheme)
    converter = Workflow.Converter(
        workflow=workflow, output_file=output_file, with_opts=True
    )
    converter.process()

    # set up workflow
    with open(output_file, mode="a") as file_:
        file_.write(_dump_executable_script_section())

    # call `black` on it if available
    try:
        # use help because there is no information regarding version
        subprocess.call(["python", "-m", "black", output_file], stdout=subprocess.PIPE)
    except Exception as e:
        _logger.error(
            "Fail to apply black on {}. Error is " "{}".format(output_file, e)
        )

    _logger.info(
        "translation finished. You can execute python {} [[--input --input-spectra --input-spectra-dims --input-channel --input-energy-unit --input-dimensions]]".format(
            output_file
        )
    )


def _dump_info_generation():
    return (
        "# This file has been generated automatically using \n"
        "# pypushflow {} and est {}\n".format(
            pypushflow.version.version, est.version.version
        )
    )


def _dump_executable_script_section():
    return """

from pypushflow.utils import IgnoreProcess

if __name__ == '__main__':
    import sys
    import argparse
    from est.app.utils import get_xas_obj
    from est.app.utils import get_url
    from est.app.utils import get_unit
    from est.app.utils import convert_spectra_dims
    from silx.io.url import DataUrl
    from est.core.types import Dim
    from est.io.utils.information import InputInformation
    from est.io.utils.information import SpecInputInformation

    parser = argparse.ArgumentParser(description=__doc__)
        # single file input option
    parser.add_argument(
        "-i",
        "--input",
        dest="input_",
        default=None,
        help="Input of the workflow. Should be a path to a file",
    )
    # input url option
    parser.add_argument(
        "--input-spectra",
        "--spectra",
        dest="input_spectra",
        default=None,
        help="Input spectra url",
    )
    parser.add_argument(
        "--input-spectra-dims",
        "--spectra-dims",
        dest="input_spectra_dims",
        default=None,
        help="Input spectra dimension. Should be a tuple of three values: "
        "(X,Y,channel). If None will take the default dimension "
        "according to the input type.",
    )
    parser.add_argument(
        "--input-energy",
        "--input-channel",
        "--channel",
        dest="input_channel",
        default=None,
        help="Input channel url (usually energy)",
    )
    parser.add_argument(
        "--input-configuration",
        "--configuration",
        dest="input_configuration",
        default=None,
        help="Input configuration url",
    )
    parser.add_argument(
        "--input-energy-unit",
        "--energy-unit",
        dest="input_energy_unit",
        default="eV",
        help="energy unit",
    )
    parser.add_argument(
        "--input-dimensions",
        "--dimensions",
        dest="input_dimensions",
        default="None",
        help="dimension of the input as (Z,Y,X) for example."
        "If None will take default unit according to the input type",
    )
    # I0, I1, I2 & mu_ref
    parser.add_argument(
        "--input-I0",
        "--I0",
        dest="input_I0",
        default="None",
        help="url to I0",
    )
    parser.add_argument(
        "--input-I1",
        "--I1",
        dest="input_I1",
        default="None",
        help="url to I1",
    )
    parser.add_argument(
        "--input-I2",
        "--I2",
        dest="input_I2",
        default="None",
        help="url to I2",
    )
    parser.add_argument(
        "--input-mu-ref",
        "--mu-ref",
        dest="input_mu_ref",
        default="None",
        help="url to mu_ref",
    )
    # spec file specific inputs
    parser.add_argument(
        "--input-energy-col-name",
        "--energy-col-name",
        dest="input_energy_col_name",
        default=None,
        help="Provide name of the energy column for spec file",
    )
    parser.add_argument(
        "--input-abs-col-name",
        "--abs-col-name",
        dest="input_abs_col_name",
        default=None,
        help="Provide name of the absorption column for spec file",
    )
    parser.add_argument(
        "--input-monitor-col-name",
        "--monitor-col-name",
        dest="input_monitor_col_name",
        default=None,
        help="Provide name of the monitor column for spec file",
    )
    parser.add_argument(
        "--input-scan-title",
        "--scan-title",
        dest="input_scan_title_name",
        default=None,
        help="Provide scan title name to consider",
    )
    # handle larch settings
    parser.add_argument(
        "--set-autobk-params",
        dest="set_autobk_params",
        default=None,
        help="set autobk settings",
    )
    parser.add_argument(
        "--set-mback-params",
        dest="set_mback_params",
        default=None,
        help="set mback settings",
    )
    parser.add_argument(
        "--set-mback-norm-params",
        dest="set_mback_norm_params",
        default=None,
        help="set mback norm settings",
    )
    parser.add_argument(
        "--set-pre-edge-params",
        dest="set_pre_edge_params",
        default=None,
        help="set pre-edge settings",
    )
    parser.add_argument(
        "--set-xftf-params",
        dest="set_xftf_params",
        default=None,
        help="set xftf settings",
    )
    # handle noise settings
    parser.add_argument(
        "--set-noise-params",
        dest="set_noise_params",
        default=None,
        help="set noise settings",
    )
    # handle output settings
    parser.add_argument(
        "--set-output-params",
        dest="set_output_params",
        default=None,
        help="set output settings",
    )
    # handle energy roi settings
    parser.add_argument(
        "--set-energyroi-params",
        dest="set_energyroi_params",
        default=None,
        help="set energy roi settings",
    )

    options = parser.parse_args(sys.argv[1:])
    
    input_information = InputInformation(
        spectra_url=get_url(options.input_spectra),
        channel_url=get_url(options.input_channel),
        dimensions=convert_spectra_dims(options.input_spectra_dims),
        config_url=get_url(options.input_configuration),
        energy_unit=get_unit(options.input_energy_unit),
        spec_input=SpecInputInformation(
            options.input_,
            options.input_energy_col_name,
            options.input_abs_col_name,
            options.input_monitor_col_name,
            options.input_scan_title_name,
        ),
    )
    input_information.I0 = get_url(options.input_I0)
    input_information.I1 = get_url(options.input_I1)
    input_information.I2 = get_url(options.input_I2)
    input_information.mu_ref = get_url(options.input_mu_ref)

    xas_obj = get_xas_obj(input_information)
    main(input_data=xas_obj, channel="xas_obj", options=options)
    """


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workflow_file",
        help="Path to the .ows file defining the workflow to process with the"
        "provided scan",
    )
    parser.add_argument("output_file", help="Output python file")
    parser.add_argument(
        "--overwrite",
        help="Overwrite output file if exists",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )
    options = parser.parse_args(argv[1:])
    if not options.output_file.lower().endswith(".py"):
        options.output_file = options.output_file + ".py"
    # tune the log level
    log_level = logging.INFO
    if options.debug is True:
        log_level = logging.DEBUG

    for log_ in ("est", "pypushflow"):
        logging.getLogger(log_).setLevel(log_level)

    scheme = OwsParser.scheme_load(options.workflow_file, load_handlers=True)
    _convert(
        scheme=scheme, output_file=options.output_file, overwrite=options.overwrite
    )


if __name__ == "__main__":
    main(sys.argv)
# convert an ows file to a script calling est low level processes.
