# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/12/2019"

import logging
from datetime import datetime
import h5py
import numpy
from silx.io.dictdump import dicttoh5, h5todict
from silx.io.url import DataUrl
from silx.utils.enum import Enum
from est.units import ur
from est.core.types.dim import Dim
from est.core.types import Spectra
from est.io.utils.spec import read_spectrum as read_spec_spectrum
from est.thirdparty.silx.hdf5file import get_data, HDF5File

try:
    from est.io.utils.larch import read_ascii as larch_read_ascii
except ImportError:
    has_larch = False
else:
    has_larch = True

_logger = logging.getLogger(__name__)


class InputType(Enum):
    dat_spectrum = "*.dat"  # contains one spectrum
    hdf5_spectra = "*.h5"  # contains several spectra
    xmu_spectrum = "*.xmu"  # contains one spectrum
    csv_spectrum = "*.csv"  # two columns, comma separated


def move_axis_to_standard(spectra, dimensions):
    # make sure all dimensions are defined
    for dim in Dim:
        if dim not in dimensions:
            err = "%s is not defined in the dimensions" % dim
            raise ValueError(err)
    # fit spectra according to dimension
    src_axis = (
        dimensions.index(Dim.DIM_2),
        dimensions.index(Dim.DIM_1),
        dimensions.index(Dim.DIM_0),
    )
    dst_axis = (0, 1, 2)
    _logger.warning("move axis for spectra, from %s to %s" % (src_axis, dst_axis))
    if isinstance(spectra, Spectra):
        spectra.data = numpy.moveaxis(spectra.data, src_axis, dst_axis)
    elif isinstance(spectra, numpy.ndarray):
        spectra = numpy.moveaxis(spectra, src_axis, dst_axis)
    return spectra


def load_data(data_url, name, dimensions, columns_names=None, energy_unit=ur.eV):
    """
    Load a specific data from an url. Manage the different scheme (silx, fabio,
    numpy, PyMca, xraylarch)

    :param data_url: silx DataUrl with path to the data
    :type: DataUrl
    :param str name: name of the data we want to load. Should be in
                    ('spectra', 'energy', 'configuration')
    :param Union[None,dict] columns_names: name of the column to pick for .dat
                                           files... Expect key 'mu' and
                                                    'energy' to be registered
    :return: data loaded
    :rtype: Union[None,dict,numpy.ndarray]
    """
    if data_url is None:
        return None
    from est.core.types import Dim  # avoid cyclic import

    if dimensions is not None:
        dimensions = tuple([Dim.from_value(dim) for dim in dimensions])
    assert isinstance(data_url, DataUrl)
    if data_url.scheme() in ("PyMca", "PyMca5", "Spec", "spec"):

        def get_energy_col_name():
            if columns_names is not None:
                return columns_names["energy"]
            if name == "energy" and data_url.data_path() is not None:
                return data_url.data_path()
            else:
                return None

        def get_absorption_col_name():
            if columns_names is not None:
                return columns_names["mu"]
            if name == "spectra" and data_url.data_path() is not None:
                return data_url.data_path()
            else:
                return None

        energy, mu = read_spec_spectrum(
            data_url.file_path(),
            energy_col_name=get_energy_col_name(),
            absorption_col_name=get_absorption_col_name(),
            monitor_col_name=columns_names["monitor"] if columns_names else None,
            scan_header_S=columns_names["scan_title"] if columns_names else None,
            energy_unit=energy_unit,
        )
        if name == "spectra":
            return mu.reshape(-1, 1, 1)
        else:
            return energy
    elif data_url.scheme() in ("larch", "xraylarch"):
        if has_larch is False:
            _logger.warning("Requires larch to load data from " "%s" % data_url.path())
            return None
        else:
            assert name in ("spectra", "energy")
            energy, mu = larch_read_ascii(
                xmu_file=data_url.file_path(), energy_unit=energy_unit
            )

            if name == "spectra":
                mu = numpy.ascontiguousarray(mu[:])
                return mu.reshape(mu.shape[0], 1, 1)
            else:
                return energy
    elif data_url.scheme() == "numpy":
        return move_axis_to_standard(numpy.load(data_url.file_path()), dimensions)
    elif data_url.scheme() == "est":
        assert name == "spectra"
        spectra = []
        with HDF5File(data_url.file_path(), "r") as hdf5:
            # get all possible entries
            entries = filter(
                lambda x: isinstance(hdf5[x], h5py.Group)
                and "est_saving_pt" in hdf5[x].keys(),
                hdf5.keys(),
            )
            entries = list(entries)
            if len(entries) == 0:
                _logger.error(
                    "no spectra dataset found in the file", data_url.file_path()
                )
                return

            if len(entries) > 1:
                _logger.warning(
                    "several entry detected, only one will be loaded:", entries[0]
                )
            spectra_path = "/".join((entries[0], "est_saving_pt", "spectra"))
            node_spectra = hdf5[spectra_path]
            spectrum_indexes = list(node_spectra.keys())
            spectrum_indexes = list(map(lambda x: int(x), spectrum_indexes))
            spectrum_indexes.sort()
            from est.core.types import Spectrum

            for index in spectrum_indexes:
                spectrum_path = "/".join((spectra_path, str(index)))
                dict_ = h5todict(
                    h5file=data_url.file_path(), path=spectrum_path, asarray=False
                )
                spectrum = Spectrum().load_frm_dict(dict_)
                spectra.append(spectrum)
        return Spectra(energy=spectra[0].energy, spectra=spectra)
    else:
        if data_url.is_valid():
            try:
                data = get_data(data_url)
            except ValueError as e:
                _logger.error(e)
            else:
                if name == "spectra":
                    if data.ndim == 1:
                        return data.reshape(data.shape[0], 1, 1)
                    elif data.ndim == 3:
                        return move_axis_to_standard(data, dimensions=dimensions)
                return data
        else:
            _logger.warning(
                "invalid url for {}: {}  will not load it".format(name, data_url)
            )


def read_xas(information):
    """
    Read the given spectra, configuration... from the provided input
    Information

    :param InputInformation informationUnion:

    :return: spectra, energy, configuration
    """

    def get_url(original_url, name):
        url_ = original_url
        if type(url_) is str:
            try:
                url_ = DataUrl(path=url_)
            except Exception:
                url_ = DataUrl(file_path=url_, scheme="PyMca")

        if not isinstance(url_, DataUrl):
            raise TypeError("given input for, {} is invalid".format(name))
        return url_

    _spectra_url = get_url(original_url=information.spectra_url, name="spectra")
    _energy_url = get_url(original_url=information.channel_url, name="energy")
    _config_url = information.config_url
    if type(_config_url) is str and _config_url == "":
        _config_url = None
    if not (_config_url is None or isinstance(_config_url, DataUrl)):
        raise TypeError("given input for configuration is invalid")

    from est.core.types import Dim  # avoid cyclic import

    # this should be extractable and done in the InputInformation class
    dimensions_ = information.dimensions
    if dimensions_ is None:
        dimensions_ = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)
    else:
        dimensions_ = []
        for dim in information.dimensions:
            dimensions_.append(Dim.from_value(dim))
    spectra = load_data(
        _spectra_url,
        name="spectra",
        dimensions=dimensions_,
        columns_names=information.columns_names,
        energy_unit=information.energy_unit,
    )
    energy = load_data(
        _energy_url,
        name="energy",
        dimensions=dimensions_,
        columns_names=information.columns_names,
        energy_unit=information.energy_unit,
    )
    configuration = load_data(
        _config_url,
        name="configuration",
        dimensions=dimensions_,
        columns_names=information.columns_names,
        energy_unit=information.energy_unit,
    )

    if energy is None:
        raise ValueError("Unable to load energy from {}".format(_energy_url))
    if not energy.ndim == 1:
        raise ValueError("Energy / channel is not 1D")
    if energy.shape[0] > spectra.shape[0]:
        energy = energy[: spectra.shape[0]]
        _logger.warning("energy has less value than spectra. Clip energy.")
    if not energy.shape[0] == spectra.shape[0]:
        err = "Energy / channel and spectra dim1 have incoherent length (%s vs %s)" % (
            energy.shape[0],
            spectra.shape[0],
        )
        raise ValueError(err)
    return spectra, energy * information.energy_unit, configuration


def write_xas_proc(
    h5_file,
    entry,
    process,
    results,
    processing_order,
    plots,
    data_path="/",
    overwrite=True,
):
    """
    Write a xas :class:`.Process` into .h5

    :param str h5_file: path to the hdf5 file
    :param str entry: entry name
    :param process: process executed
    :type: :class:`.Process`
    :param results: process result data
    :type: numpy.ndarray
    :param processing_order: processing order of treatment
    :type: int
    :param data_path: path to store the data
    :type: str
    """
    if plots is None:
        plots = tuple()
    process_name = "xas_process_" + str(processing_order)
    # write the xasproc default information
    with HDF5File(h5_file, "a") as h5f:
        nx_entry = h5f.require_group("/".join((data_path, entry)))
        nx_entry.attrs["NX_class"] = "NXentry"

        nx_process = nx_entry.require_group(process_name)
        nx_process.attrs["NX_class"] = "NXprocess"
        if overwrite:
            for key in (
                "program",
                "version",
                "date",
                "processing_order",
                "class_instance",
                "ft",
            ):
                if key in nx_process:
                    del nx_process[key]
        nx_process["program"] = process.program_name()
        nx_process["version"] = process.program_version()
        nx_process["date"] = datetime.now().replace(microsecond=0).isoformat()
        nx_process["processing_order"] = numpy.int32(processing_order)
        _class = process.__class__
        nx_process["class_instance"] = ".".join((_class.__module__, _class.__name__))

        nx_data = nx_entry.require_group("data")
        nx_data.attrs["NX_class"] = "NXdata"
        nx_data.attrs["signal"] = "data"
        nx_process_path = nx_process.name

    if isinstance(results, numpy.ndarray):
        data_ = {"data": results}
    else:
        data_ = results

    def get_interpretation(my_data):
        """Return hdf5 attribute for this type of data"""
        if isinstance(my_data, numpy.ndarray):
            if my_data.ndim == 1:
                return "spectrum"
            elif my_data.ndim in (2, 3):
                return "image"
        return None

    def get_path_to_result(res_name):
        res_name = res_name.replace(".", "/")
        path = "/".join((entry, process_name, "results", res_name))
        if path.startswith("/"):
            path = "/" + path
        return path

    # save results
    def save_key(key_path, value, attrs):
        """Save the given value to the associated path. Manage numpy arrays
        and dictionaries.
        """
        if attrs is not None:
            assert value is None, "can save value or attribute not both"
        if value is not None:
            assert attrs is None, "can save value or attribute not both"
        key_path = key_path.replace(".", "/")
        # save if is dict
        if isinstance(value, dict):
            h5_path = "/".join((entry, process_name, key_path))
            dicttoh5(
                value,
                h5file=h5_file,
                h5path=h5_path,
                overwrite_data=True,
                mode="a",
            )
        else:
            with HDF5File(h5_file, "a") as h5f:
                nx_process = h5f.require_group(nx_process_path)
                if attrs is None:
                    try:
                        nx_process[key_path] = value
                    except TypeError as e:
                        _logger.warning(
                            "Unable to write at {} reason is {}"
                            "".format(str(key_path), str(e))
                        )
                    else:
                        interpretation = get_interpretation(value)
                        if interpretation:
                            nx_process[key_path].attrs[
                                "interpretation"
                            ] = interpretation
                else:
                    for key, value in attrs.items():
                        try:
                            nx_process[key_path].attrs[key] = value
                        except Exception as e:
                            _logger.warning(e)

    for key, value in data_.items():
        if isinstance(key, tuple):
            key_path = "/".join(("results", key[0]))
            save_key(key_path=key_path, value=None, attrs={key[1]: value})
        else:
            key_path = "/".join(("results", str(key)))
            save_key(key_path=key_path, value=value, attrs=None)

    def save_plot(plot_name, plot):
        """save the given plot to an hdf5 group"""
        plot_name = plot_name.replace(".", "/")
        plot_path = "/".join((entry, process_name, "plots", plot_name))

        with HDF5File(h5_file, "a") as h5f:
            plot_group = h5f.require_group(plot_path)
            plot_group.attrs["NX_class"] = "NXdata"
            plot_group.attrs["interpretation"] = "spectrum"
            assert plot.signal is not None
            assert plot.axes is not None

            def link_dataset(dataset_to_link, name):
                # to insure silx isplotting it we should have curve as a 1D object
                # but by default we are handling a map of spectra. This is why we
                # need to duplicate data here
                if dataset_to_link.ndim == 1:
                    plot_group[name] = h5py.SoftLink(dataset_to_link.name)
                elif dataset_to_link.ndim == 2:
                    plot_group[name] = dataset_to_link[:, 0]
                    for key in ("units", "units_latex"):
                        if key in dataset_to_link.attrs:
                            plot_group[name].attrs[key] = dataset_to_link.attrs[key]
                elif dataset_to_link.ndim == 3:
                    plot_group[name] = dataset_to_link[:, 0, 0]
                    for key in ("units", "units_latex"):
                        if key in dataset_to_link.attrs:
                            plot_group[name].attrs[key] = dataset_to_link.attrs[key]
                else:
                    raise ValueError(
                        "Unable to handle dataset {}".format(dataset_to_link.name)
                    )

            # handle signal
            # plot is only handling 1D data
            try:
                signal_dataset = h5f[get_path_to_result(plot.signal)]
            except KeyError:
                _logger.info("{} is not available".format(plot.signal))
            else:
                link_dataset(dataset_to_link=signal_dataset, name=plot.signal)
            plot_group.attrs["signal"] = plot.signal
            # handle axes
            for axe in plot.axes:
                try:
                    axe_dataset = h5f[get_path_to_result(axe)]
                except KeyError:
                    _logger.info("{} is not available".format(axe))
                else:
                    link_dataset(dataset_to_link=axe_dataset, name=axe)
            plot_group.attrs["axes"] = plot.axes
            # handle auxiliary signals
            if plot.auxiliary_signals is not None:
                for aux_sig in plot.auxiliary_signals:
                    try:
                        aux_sig_dataset = h5f[get_path_to_result(aux_sig)]
                    except KeyError:
                        _logger.info("{} is not available".format(aux_sig))
                    else:
                        link_dataset(dataset_to_link=aux_sig_dataset, name=aux_sig)

                plot_group.attrs["auxiliary_signals"] = plot.auxiliary_signals
            # handle title(s)
            if plot.title is not None:
                plot_group.attrs["title"] = plot.title
            if plot.title_latex is not None:
                plot_group.attrs["title_latex"] = plot.title_latex

            # handle silx style
            if plot.silx_style is not None:
                import json

                plot_group.attrs["SILX_style"] = json.dumps(plot.silx_style)

    # save plots
    for i_plot, plot in enumerate(plots):
        plot_name = "plot_{}".format(i_plot)
        save_plot(plot_name=plot_name, plot=plot)

    # default plot will always be the first one
    if len(plots) > 0:
        plots_path = "/".join((entry, process_name, "plots"))
        with HDF5File(h5_file, "a") as h5f:
            plots_group = h5f.require_group(plots_path)
            plots_group.attrs["NX_class"] = "NXdata"
            plots_group.attrs["default"] = "plot_0"

    if process.getConfiguration() is not None:
        h5_path = "/".join((nx_process_path, "configuration"))
        dicttoh5(
            process.getConfiguration(),
            h5file=h5_file,
            h5path=h5_path,
            overwrite_data=True,
            mode="a",
        )


def write_xas(
    h5_file,
    entry,
    energy,
    mu,
    sample=None,
    start_time=None,
    data_path="/",
    title=None,
    definition=None,
    overwrite=True,
):
    """
    Write raw date in nexus format

    :param str h5_file: path to the hdf5 file
    :param str entry: entry name
    :param sample: definition of the sample
    :type: :class:`.Sample`
    :param energy: beam energy (1D)
    :type: numpy.ndarray
    :param mu: beam absorption (2D)
    :type: numpy.ndarray
    :param start_time:
    :param str data_path:
    :param str title: experiment title
    :param str definition: experiment definition
    """
    with HDF5File(h5_file, "w") as h5f:
        nx_entry = h5f.require_group("/".join((data_path, entry)))
        nx_entry.attrs["NX_class"] = "NXentry"

        # store energy
        nx_monochromator = nx_entry.require_group("monochromator")
        nx_monochromator.attrs["NX_class"] = "NXmonochromator"
        if overwrite and "energy" in nx_monochromator:
            del nx_monochromator["energy"]
        nx_monochromator["energy"] = energy
        nx_monochromator["energy"].attrs["interpretation"] = "spectrum"
        nx_monochromator["energy"].attrs["NX_class"] = "NXdata"
        nx_monochromator["energy"].attrs["unit"] = "eV"

        # store absorbed beam
        nx_absorbed_beam = nx_entry.require_group("absorbed_beam")
        nx_absorbed_beam.attrs["NX_class"] = "NXdetector"
        if overwrite and "data" in nx_absorbed_beam:
            del nx_absorbed_beam["data"]
        nx_absorbed_beam["data"] = mu
        nx_absorbed_beam["data"].attrs["interpretation"] = "image"
        nx_absorbed_beam["data"].attrs["NX_class"] = "NXdata"

        if sample:
            nx_sample = nx_entry.require_group("sample")
            nx_sample.attrs["NX_class"] = "NXsample"
            if overwrite and "name" in nx_sample:
                del nx_sample["name"]
            nx_sample["name"] = sample.name

        nx_data = nx_entry.require_group("data")
        nx_data.attrs["NX_class"] = "NXdata"
        # create some link on data
        if overwrite and "energy" in nx_data:
            del nx_data["energy"]
        nx_data["energy"] = h5py.SoftLink(nx_monochromator["energy"].name)
        if overwrite and "absorbed_beam" in nx_data:
            del nx_data["absorbed_beam"]
        nx_data["absorbed_beam"] = h5py.SoftLink(nx_absorbed_beam["data"].name)

        if start_time is not None:
            if overwrite and "start_time" in nx_entry:
                del nx_entry["start_time"]
            nx_entry["start_time"] = start_time
        if title is not None:
            if overwrite and "title" in nx_entry:
                del nx_entry["title"]
            nx_entry["title"] = title
        if definition is not None:
            if overwrite and "definition" in nx_entry:
                del nx_entry["definition"]
            nx_entry["definition"] = definition


def write_spectrum_saving_pt(h5_file, entry, obj, overwrite=True):
    """Save the current status of an est object

    :param str h5_file: path to the hdf5 file
    :param str entry: entry name
    :param obj: object to save.
    :param str obj_name: name of the object to store
    :param str data_path:
    """
    dicttoh5(obj, h5file=h5_file, h5path=entry, overwrite_data=True, mode="a")


def get_xasproc(h5_file, entry):
    """
    Return the list of all NXxasproc existing at the data_path level

    :param str h5_file: hdf5 file
    :param str entry: data location

    :return:
    :rtype: list
    """

    def copy_nx_xas_process(h5_group):
        """copy base information from nx_xas_process"""
        res = {}
        res["_h5py_path"] = h5_group.name
        relevant_keys = (
            "program",
            "version",
            "data",
            "parameters",
            "processing_order",
            "configuration",
            "class_instance",
            "plots",
        )
        from silx.io.dictdump import h5todict

        for key in h5_group.keys():
            # for now we don't want to copy the numpy array (data)
            if key in relevant_keys:
                if key == "configuration":
                    config_path = "/".join((h5_group.name, "configuration"))
                    res[key] = h5todict(h5_file, config_path, asarray=False)
                elif key == "plots":
                    plots_grp = h5_group["plots"]
                    res[key] = {}
                    for plot_key in plots_grp.keys():
                        res[key][plot_key] = dict(plots_grp[plot_key].attrs.items())
                else:
                    res[key] = h5_group[key][...]
        return res

    res = []
    with HDF5File(h5_file, "a") as h5f:
        try:
            root_group = h5f[entry]
        except KeyError:
            _logger.warning(entry + " does not exist in " + h5_file)
        else:
            for key in root_group.keys():
                elmt = root_group[key]
                if hasattr(elmt, "attrs") and "NX_class" in elmt.attrs:
                    if elmt.attrs["NX_class"] == "NXprocess":
                        nx_xas_proc = copy_nx_xas_process(elmt)
                        if len(nx_xas_proc) == 0:
                            _logger.warning(
                                "one xas process was not readable "
                                "from the hdf5 file at:" + key
                            )
                        else:
                            res.append(nx_xas_proc)
    return res


if __name__ == "__main__":
    import os
    from est.core.process.pymca.normalization import PyMca_normalization
    from est.core.process.pymca.exafs import PyMca_exafs
    from est.core.types import Sample

    h5_file = "test_xas_123.h5"
    if os.path.exists(h5_file):
        os.remove(h5_file)
    sample = Sample(name="mysample")
    data = numpy.random.rand(256 * 20 * 10)
    data = data.reshape((256, 20, 10))
    process_data = numpy.random.rand(256 * 20 * 10).reshape((256, 20, 10))
    energy = numpy.linspace(start=3.25, stop=3.69, num=256)

    write_xas(h5_file=h5_file, entry="scan1", sample=sample, energy=energy, mu=data)

    process_norm = PyMca_normalization()
    write_xas_proc(
        h5_file=h5_file,
        entry="scan1",
        process=process_norm,
        results=process_data,
        processing_order=1,
    )
    process_exafs = PyMca_exafs()
    process_data2 = numpy.random.rand(256 * 20 * 10).reshape((256, 20, 10))
    write_xas_proc(
        h5_file=h5_file,
        entry="scan1",
        process=process_exafs,
        results=process_data2,
        processing_order=2,
    )


def get_column_name(dat_file):
    from silx.io.spech5 import SpecH5
    from silx.io.spech5 import SpecFile

    spec_h5 = SpecH5(dat_file)
    spec_file = SpecFile(dat_file)


if __name__ == "__main__":
    get_column_name("specfiledata_tests.dat")
