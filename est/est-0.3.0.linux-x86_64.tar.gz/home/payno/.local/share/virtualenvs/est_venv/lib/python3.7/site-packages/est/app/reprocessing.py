import argparse
import sys
import logging
from est.core.types import XASObject
from est.core.reprocessing import get_process_instance_frm_h5_desc
from typing import Union

try:
    import h5py

    has_h5py = True
except:
    has_h5py = False

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def exec_(
    h5_file: str,
    entry: str = "scan1",
    spectra_path: Union[None, str] = None,
    energy_path: Union[None, str] = None,
    configuration_path: Union[None, str] = None,
):

    try:
        xas_obj = XASObject.from_file(
            h5_file=h5_file,
            entry=entry or "scan1",
            spectra_path=spectra_path or "data/absorbed_beam",
            energy_path=energy_path or "data/energy",
            configuration_path=configuration_path,
        )
        xas_obj.link_to_h5(h5_file=h5_file)
    except Exception as e:
        _logger.error(e)
        xas_obj = None

    if not xas_obj:
        _logger.error("Unable to create an object from the given file and path")

    xas_processes = xas_obj.get_process_flow()
    if len(xas_processes) == 0:
        _logger.warning("no xas process found in the given h5 file")
        return
    xas_obj.clean_process_flow()
    for i_process, process in xas_processes.items():
        process_ins = get_process_instance_frm_h5_desc(process)
        xas_obj = process_ins(xas_obj)

    return xas_obj


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workflow_file", help="Workflow file providing the workflow description (.h5)"
    )
    parser.add_argument(
        "--spectra_path",
        dest="spectra_path",
        default=None,
        help="path to the spectra data",
    )
    parser.add_argument(
        "--energy_path",
        dest="energy_path",
        default=None,
        help="path to the energy data",
    )
    parser.add_argument(
        "--configuration_path",
        dest="configuration_path",
        default=None,
        help="path to the process configuration",
    )
    parser.add_argument(
        "--entry",
        dest="entry to load",
        default=None,
        help="path to the process configuration",
    )
    options = parser.parse_args(argv[1:])
    exec_(
        h5_file=options.workflow_file,
        spectra_path=options.spectra_path,
        energy_path=options.energy_path,
        configuration_path=options.configuration_path,
    )


if __name__ == "__main__":
    main(sys.argv)
