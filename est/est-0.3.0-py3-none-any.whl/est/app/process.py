import argparse
import sys
from pypushflow.Workflow import ProcessableWorkflow
from pypushflow.representation.scheme.ows_parser import OwsParser
import logging
import signal
from pypushflow.representation.scheme.scheme import Scheme
from silx.io.url import DataUrl
from est.units import ur
from est.io.utils.information import InputInformation
from est.io.utils.information import SpecInputInformation
from .utils import get_unit
from .utils import get_url
from .utils import convert_spectra_dims
from .utils import get_xas_obj

try:
    import h5py

    has_h5py = True
except:
    has_h5py = False
from typing import Union

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def _insert_input_in_scheme(scheme, input_information):
    """update 'starting' node properties to include the provided input"""
    # monkey patch the input file for start nodes if an input is given
    for node in scheme.nodes:
        if node.properties and "_spec_file_setting" in node.properties:
            if input_information.is_spec_input():
                node.properties["_spec_file_setting"] = input_information.spec_info
            if input_information.spectra_url is not None:
                node.properties[
                    "_spectra_url_setting"
                ] = input_information.spectra_url.path()
            if input_information.dimensions is not None:
                node.properties["_dimensions_setting"] = input_information.dimensions
            if input_information.channel_url is not None:
                node.properties[
                    "_energy_url_setting"
                ] = input_information.channel_url.path()
            if input_information.configuration_url is not None:
                node.properties[
                    "_configuration_url_setting"
                ] = input_information.configuration_url.path()


def _insert_output_in_scheme(scheme, output_):
    """update 'starting' node properties to include the provided input"""
    found_output = False
    # monkey patch the input file for start nodes if an input is given
    for node in scheme.nodes:
        if node.properties and "_output_file_setting" in node.properties:
            node.properties["_output_file_setting"] = output_
            found_output = True
    if not found_output:
        _logger.warning(
            "No node for processing output found. output "
            "information provided will be ignored"
        )


def exec_(
    scheme: Scheme,
    input_information: InputInformation,
    output_: Union[str, None, dict] = None,
    timeout: Union[int, None] = None,
):

    if not input_information.is_valid():
        raise ValueError("You cannot provide an input file and input urls")

    _insert_input_in_scheme(input_information=input_information, scheme=scheme)
    if output_ is not None:
        _insert_output_in_scheme(scheme=scheme, output_=output_)

    workflow = ProcessableWorkflow(scheme=scheme)

    # add SIGINT capture
    def signal_handler(sig, frame):
        _logger.warning("stop workflow execution on user request")
        workflow._end_actor.join(0)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    xas_obj = get_xas_obj(input_information=input_information)

    workflow._start_actor.trigger(("data", xas_obj.to_dict()))
    workflow._end_actor.join(timeout)
    res = workflow._end_actor.out_data
    title = scheme.title or "unknow"
    _logger.info(
        "workflow '{}' completed with {}".format(title, str(input_information))
    )
    return res


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workflow_file",
        help="Workflow file providing the workflow description (.ows, .xml)",
    )
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
    # output option
    parser.add_argument(
        "-o",
        "--output",
        dest="output_",
        default=None,
        help="Output file of the workflow. Require at most one "
        "instance of XASOutputOW",
    )
    options = parser.parse_args(argv[1:])

    scheme = OwsParser.scheme_load(options.workflow_file, load_handlers=True)
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
    exec_(scheme=scheme, input_information=input_information)


if __name__ == "__main__":
    main(sys.argv)
