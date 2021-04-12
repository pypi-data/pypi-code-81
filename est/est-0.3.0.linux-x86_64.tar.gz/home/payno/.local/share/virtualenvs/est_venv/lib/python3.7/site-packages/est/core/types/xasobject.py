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
__date__ = "14/12/2020"


from silx.io.url import DataUrl
import est.io
import copy
import numpy
import logging
import h5py
import tempfile
import os
import shutil
import pint
from est.units import ur
from est.units import convert_to as convert_unit_to
from silx.io.utils import h5py_read_dataset
from typing import Union
from .dim import Dim
from .spectra import Spectra
from est.thirdparty.silx.hdf5file import get_data, HDF5File

try:
    import larch
except ImportError:
    _has_larch = False
else:
    _has_larch = True

_logger = logging.getLogger(__name__)


class XASObject(object):
    """Base class of XAS

    :param spectra: absorbed beam as a list of :class:`.Spectrum` or a
                    numpy.ndarray. If is a numpy array:
                        * dim0: channel,
                        * dim1: Y,
                        * dim2: X
    :type: Union[numpy.ndarray, list]
    :param energy: beam energy
    :type: numpy.ndarray of one dimension
    :param dict configuration: configuration of the different process
    :param int dim1: first dimension of the spectra
    :param int dim2: second dimension of the spectra
    :param str name: name of the object. Will be used for the hdf5 entry
    :param bool keep_process_flow: if True then will keep the trace of the set
                                   of process applied to the XASObject into a
                                   hdf5 file.
                                   This is also used for the
    :param spectra_url: path to the spectra data if any. Used when serializing
                        the XASObject. Won't read it from it.
    :type: Union[None,str]
    :param spectra_url_dimensions: dimensions of the stored spectra. WARNING:
                                   this is different of the spectra dimension
                                   which should be given in the
                                   `DEFAULT_DIMENSIONS` order (Channel, Y, X)
    :type: Union[tuple,None]
    :param energy_url: path to the energy / channel  data if any. Used when
                       serializing the XASObject. Won't read it from it.
    :type: Union[None,str]
    """

    DEFAULT_DIMENSIONS = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)

    def __init__(
        self,
        spectra=None,
        energy=None,
        configuration: Union[dict, None] = None,
        dim1: Union[int, None] = None,
        dim2: Union[int, None] = None,
        name: str = "scan1",
        keep_process_flow: bool = True,
        spectra_url: Union[DataUrl, None] = None,
        spectra_url_dims=None,
        energy_url: Union[DataUrl, None] = None,
        check_energy: bool = True,
    ):
        if isinstance(energy, numpy.ndarray) and not isinstance(
            energy, pint.quantity.Quantity
        ):
            # automatic energy unit guess. convert energy provided in keV to eV
            # works because EXAFS data are never longer than 2 keV and a low
            # energy XANES is never shorter than 3 eV. See issue 30
            if (energy.max() - energy.min()) < 3.0:
                energy = energy * ur.keV
            else:
                energy = energy * ur.eV

        if energy is not None:
            energy = energy.m_as(ur.eV)

        self.__channels = None
        self.__spectra = Spectra(energy=energy)
        self.__dim1 = None
        self.__dim2 = None
        self.__processing_index = 0
        self.__h5_file = None
        self.__entry_name = name
        self.__spectra_url = spectra_url
        self.__spectra_url_dims = spectra_url_dims
        self.__energy_url = energy_url
        self.spectra = (energy, spectra, dim1, dim2)
        self.configuration = configuration
        if keep_process_flow is True:
            self.__h5_file = os.path.join(
                tempfile.mkdtemp(), "_".join((name, "_flow.h5"))
            )
            self.link_to_h5(self.__h5_file)

    def attach_3d_array(self, attr_name, attr_value):
        """
        Attach to each attribute the provided value

        :param attr_name:
        :param attr_value:
        :return:
        """
        if isinstance(attr_value, DataUrl):
            data = get_data(attr_value)
        else:
            data = attr_value
        if not isinstance(data, numpy.ndarray):
            raise TypeError(
                "`attr_value` should be an instance of DataUrl "
                "referencing a numpy array or a numpy array not "
                "{}".format(type(data))
            )
        if data.ndim > 2:
            for spectrum, d in zip(self.spectra.data.flat, data):
                setattr(spectrum, attr_name, d)
        else:
            for spectrum in self.spectra.data.flat:
                setattr(spectrum, attr_name, data)

    @property
    def entry(self) -> str:
        return self.__entry_name

    @property
    def spectra(self):
        return self.__spectra

    @property
    def spectra_url(self) -> Union[None, DataUrl]:
        """Url from where the spectra is available.
        Used for object serialization"""
        return self.__spectra_url

    @spectra_url.setter
    def spectra_url(self, url: DataUrl):
        self.__spectra_url = url

    @property
    def spectra_url_dims(self) -> tuple:
        """used to interpret the spectra_url if any"""
        return self.__spectra_url_dims

    @spectra_url_dims.setter
    def spectra_url_dims(self, dims: tuple):
        self.__spectra_url_dims = dims

    @property
    def energy_url(self) -> Union[DataUrl, None]:
        """Url from where the energy is available.
        Used for object serialization"""
        return self.__energy_url

    @energy_url.setter
    def energy_url(self, url: DataUrl):
        self.__energy_url = url

    @property
    def normalized_energy(self):
        if self.spectra is not None:
            return self.spectra.data.flat[0].normalized_energy

    # TODO: should no take such a tuple in parameter but the different parameter
    # energy, spectra, dim1, dim2
    @spectra.setter
    def spectra(self, energy_spectra: tuple):
        if isinstance(energy_spectra, Spectra):
            self.__spectra = energy_spectra
        else:
            if not len(energy_spectra) == 4:
                raise ValueError(
                    "4 elements expected: energy, spectra, dim1 and dim2. get {} instead".format(
                        len(energy_spectra)
                    )
                )
            energy, spectra, dim1, dim2 = energy_spectra
            self.__spectra = Spectra(energy=energy, spectra=spectra)
            if dim1 is not None and dim2 is not None:
                self.__spectra.reshape((dim1, dim2))

    def get_spectrum(self, dim1_idx: int, dim2_idx: int) -> spectra:
        """Util function to access the spectrum at dim1_idx, dim2_idx"""
        return self.spectra[dim1_idx, dim2_idx]

    @property
    def energy(self) -> numpy.ndarray:
        """energy as a numpy array in eV.
        :note: cannot be with unit because use directly by xraylarch and pymca
        """
        return self.spectra.energy

    @property
    def configuration(self) -> dict:
        return self.__configuration

    @configuration.setter
    def configuration(self, configuration: dict):
        assert configuration is None or isinstance(configuration, dict)
        self.__configuration = configuration or {}

    def _create_saving_pt(self):
        if not self.has_linked_file():
            raise ValueError(
                "there is not where to create a saving pt"
                "(no h5 file linked to the XASObject)"
            )
        else:

            def get_list_spectra():
                res = {}

                for i_spectrum, spectrum in enumerate(self.spectra.data.flat):
                    res[i_spectrum] = spectrum.to_dict()
                return res

            from est.io import write_spectrum_saving_pt

            # save spectra
            entry = "/".join((self.entry, "est_saving_pt", "spectra"))
            for i_spectrum, spectrum in get_list_spectra().items():
                path = "/".join((entry, str(i_spectrum)))
                write_spectrum_saving_pt(
                    h5_file=self.linked_h5_file,
                    entry=path,
                    obj=spectrum,
                    overwrite=True,
                )
            # save channel
            with HDF5File(self.linked_h5_file, "a") as h5f:
                entry = "/".join((self.entry, "est_saving_pt", "channel"))
                if entry in h5f:
                    del h5f[entry]
                h5f[entry] = (
                    "None"
                    if self.energy is None
                    else convert_unit_to(self.energy, ur.eV).m_as(ur.eV)
                )

    def to_dict(self, with_process_details=True) -> dict:
        """convert the XAS object to a dict

        By default made to simply import raw data.

        :param with_process_details: used to embed a list of spectrum with
                                     intermediary result instead of only raw mu.
                                     This is needed especially for the
                                     pushworkflow actors to keep a trace of the
                                     processes.
        :type: bool
        """

        def get_spectra_and_processing():
            if not self.has_linked_file():
                raise ValueError(
                    "To get process details you should have a" "`process` link file"
                )
            else:
                # store the current spectra with processing information
                data_path = "/".join((self.entry, "est_saving_pt", "spectra"))
                return DataUrl(
                    file_path=self.linked_h5_file, data_path=data_path, scheme="est"
                ).path()

        def get_energy():
            if not self.has_linked_file():
                raise ValueError(
                    "To get process details you should have a" "`process` link file"
                )
            else:
                data_path = "/".join((self.entry, "est_saving_pt", "channel"))
                return DataUrl(
                    file_path=self.linked_h5_file, data_path=data_path, scheme="silx"
                ).path()

        self._create_saving_pt()
        spectra_ = get_spectra_and_processing()
        res = {
            "configuration": self.configuration,
            "spectra": spectra_,
            "energy": get_energy(),
            "dim1": self.spectra.shape[0],
            "dim2": self.spectra.shape[1],
        }
        if with_process_details is True:
            res["linked_h5_file"] = self.linked_h5_file
            res["current_processing_index"] = self.__processing_index

        return res

    def absorbed_beam(self) -> numpy.ndarray:
        return self.spectra.map_to(data_info="mu")

    def load_frm_dict(self, ddict: dict):
        """load XAS values from a dict"""
        dimensions = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)
        # default yay of storing data
        from est.io import load_data  # avoid cyclic import

        contains_config_spectrum = "configuration" in ddict or "spectra" in ddict
        """The dict can be on the scheme of the to_dict function, containing
        the spectra and the configuration. Otherwise we consider it is simply
        the spectra"""
        if "configuration" in ddict:
            self.configuration = ddict["configuration"]
        if "spectra" in ddict:
            self.spectra = Spectra.frm_dict(ddict["spectra"], dimensions=dimensions)
        else:
            self.spectra = None
        if "energy" in ddict:
            energy = ddict["energy"]
            if isinstance(energy, str):
                energy_url = DataUrl(path=energy)
                energy = load_data(
                    data_url=energy_url, name="energy", dimensions=dimensions
                )
        else:
            energy = None
        if "dim1" in ddict:
            dim1 = ddict["dim1"]
        else:
            dim1 = None
        if "dim2" in ddict:
            dim2 = ddict["dim2"]
        else:
            dim2 = None
        if "linked_h5_file" in ddict:
            assert "current_processing_index" in ddict
            self.link_to_h5(ddict["linked_h5_file"])
            self.__processing_index = ddict["current_processing_index"]
        self.spectra.reshape((dim1, dim2))
        return self

    @staticmethod
    def from_dict(ddict: dict):
        return XASObject().load_frm_dict(ddict=ddict)

    @staticmethod
    def from_file(
        h5_file,
        entry="scan1",
        spectra_path="data/absorbed_beam",
        energy_path="data/energy",
        configuration_path="configuration",
        dimensions=None,
    ):
        # load only mu and energy from the file
        spectra_url = DataUrl(
            file_path=h5_file, data_path="/".join((entry, spectra_path)), scheme="silx"
        )
        energy_url = DataUrl(
            file_path=h5_file, data_path="/".join((entry, energy_path)), scheme="silx"
        )
        if configuration_path is None:
            config_url = None
        else:
            config_url = DataUrl(
                file_path=h5_file,
                data_path="/".join((entry, configuration_path)),
                scheme="silx",
            )
        from est.io.utils.information import InputInformation

        sp, en, conf = est.io.read_xas(
            InputInformation(
                spectra_url=spectra_url,
                channel_url=energy_url,
                config_url=config_url,
                dimensions=dimensions,
            ),
        )
        return XASObject(spectra=sp, energy=en, configuration=conf)

    def dump(self, h5_file: str):
        """dump the XAS object to a file_path within the Nexus format"""
        from est.core.io import XASWriter  # avoid cyclic import

        writer = XASWriter()
        # dump raw data
        writer.output_file = h5_file
        writer.dump_xas(xas_obj=self, write_process=True)

    def copy(self, create_h5_file=False):
        """

        :param bool create_h5_file: True if we want to duplicate the h5 file
                                 This is the case for orange widget for example
                                 where some reprocessing can append and each
                                 process need to keep a clear history of
                                 processes, with no knowledge of next
                                 processing.
        """
        # To have dedicated h5 file we have to create one new h5 file for
        # for each process. For now there is no way to do it differently
        res = copy.copy(self)
        if create_h5_file is True:
            new_h5_file = os.path.join(
                tempfile.mkdtemp(), "_".join((self.__entry_name, "_flow.h5"))
            )
            if self.has_linked_file() and os.path.exists(self.linked_h5_file):
                shutil.copy(src=self.linked_h5_file, dst=new_h5_file)
            res.link_to_h5(new_h5_file)
        return res

    def __eq__(self, other):
        return (
            isinstance(other, XASObject)
            and (
                (self.energy is None and other.energy is None)
                or numpy.array_equal(self.energy, other.energy)  # noqa
            )  # noqa
            and self.configuration == other.configuration  # noqa
            and self.spectra,
            other.spectra,  # noqa
        )

    @property
    def n_spectrum(self) -> int:
        """return the number of spectra"""
        return len(self.spectra.data.flat)

    def spectra_keys(self) -> tuple:
        """keys contained by the spectrum object (energy, mu, normalizedmu...)"""
        return self.spectra.keys()

    @property
    def linked_h5_file(self):
        return self.__h5_file

    def link_to_h5(self, h5_file: str):
        """
        Associate a .h5 file to the XASObject. This can be used for storing
        process flow.

        :param h5_file:
        :return:
        """
        self.__h5_file = h5_file

    def has_linked_file(self) -> bool:
        return self.__h5_file is not None

    def get_next_processing_index(self) -> int:
        self.__processing_index += 1
        return self.__processing_index

    def register_processing(self, process, results, plots) -> None:
        """
        Register one process for the current xas object. This require to having
        link a h5file to this object

        :param process: process to be registred
        :type: :class:`.Process`
        :param results: result of the processing. If there is more than one
                     result then a dictionary with the key under which result
                     should be saved and a numpy.ndarray
        :type: Union[numpy.ndarray,dict]
        """
        est.io.write_xas_proc(
            self.linked_h5_file,
            entry=self.__entry_name,
            processing_order=self.get_next_processing_index(),
            process=process,
            results=results,
            plots=plots,
            overwrite=True,
        )

    def get_process_flow(self) -> dict:
        """

        :return: the dict of process information
        :rtype: dict
        """
        if not self.linked_h5_file:
            _logger.warning(
                "process flow is store in the linked .h5 file. If"
                "no link is defined then this information is not"
                "stored"
            )
            return {}
        else:
            recognized_process = est.io.get_xasproc(
                self.linked_h5_file, entry=self.__entry_name
            )
            know_process = (
                "pymca_normalization",
                "pymca_exafs",
                "pymca_ft",
                "pymca_k_weight",
                "larch_autobk",
                "larch_mback",
                "larch_mback_norm",
                "larch_pre_edge",
                "larch_xftf",
                "noise",
                "noise_savgol",
                "roi",
                "energy-roi",
            )

            def filter_recognized_process(process_list):
                res = []
                for process_ in process_list:
                    if (
                        "program" in process_.keys()
                        and h5py_read_dataset(process_["program"])
                        in know_process  # noqa
                    ):
                        res.append(process_)
                return res

            recognized_process = filter_recognized_process(recognized_process)

            def get_ordered_process(process_list):
                res = {}
                for process_ in process_list:
                    if "processing_order" not in process_:
                        _logger.warning(
                            "one processing has not processing order: "
                            + process_["program"]  # noqa
                        )
                    else:
                        processing_order = int(process_["processing_order"])
                        res[processing_order] = process_
                return res

            return get_ordered_process(recognized_process)

    def clean_process_flow(self) -> None:
        """
        Remove existing process flow
        """
        if not self.linked_h5_file:
            _logger.warning(
                "process flow is store in the linked .h5 file. If"
                "no link is defined then this information is not"
                "stored"
            )
        else:
            process_flow = self.get_process_flow()
            with HDF5File(self.linked_h5_file, "a") as h5f:
                for index, process_ in process_flow.items():
                    del h5f[process_["_h5py_path"]]

    def copy_process_flow_to(self, h5_file_target: str) -> None:
        """
        copy all the recognized process from self.__h5_file to h5_file_target

        :param str h5_file_target: path to the targeted file. Should be an
                                   existing hdf5 file.
        """
        assert os.path.exists(h5_file_target)
        assert h5py.is_hdf5(h5_file_target)

        flow = self.get_process_flow()
        entry = self.entry
        with HDF5File(self.__h5_file, "a") as source_hdf:
            with HDF5File(h5_file_target, "a") as target_hdf:
                target_entry = target_hdf.require_group(entry)

                def remove_entry_prefix(name):
                    return name.replace("/" + entry + "/", "", 1)

                for process_id, process in flow.items():
                    process_path = process["_h5py_path"]
                    dst_path = remove_entry_prefix(name=process_path)
                    target_entry.copy(source=source_hdf[process_path], dest=dst_path)
