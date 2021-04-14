from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from pathlib import Path
from typing import BinaryIO
from typing import Type
from typing import Union

import numpy as np
from astropy.io import fits


def fits_dataclass(cls):
    """
    A specification of the builtin `dataclasses.dataclass` that allows for simple, terse definitions of FITS-header-based
    dataclasses. When writing a DKIST metadataclass the developer specifies the desired class properties with values
    corresponding to their source keyword in a FITS header. This function creates an __init__ that populates the
    dataclass properties with the correct values and the numpy array.

    For IDE support the developer must specify the correct type of the desired value.

    Examples
    --------
    # Define a simple class
    @fits_dataclass
    class MetaData:
        elevation: float = 'TELEVATN'

    # Use it to ingest a header
    MD = MetaData(data, header)
    # Then access the elevation property
    some_number = MD.elevation / 2

    # subclassing the resulting dataclasses is possible and encouraged:
    @fits_dataclass
    class InstMetaData(MetaData):
        current_spatial_step: int = 'INST_011'
        # You also get all the keys defined in the subclass for free
    """
    # Note for future self: We need this custom decorator because of how @dataclass handles subclasses. Tl;dr: we _could_
    # put this code directly as __init__ in CommonFitsData and just use the @dataclass decorator but then any subclasses
    # would need to use @dataclass(init=False) in order have access to the parent's __init__ function. This works, but
    # puts more burden on definers of child classes to not mess it up. Also, we're already abusing the idea of what a
    # @dataclass is by using the "class variables" to define a mapping, not the actual properties. I think both of these
    # reasons are strong arguments for using a custom decorator, even if technically this is possible in a different way
    # with less code.
    def init_func(self, data: np.ndarray, header: Union[fits.header.Header, dict] = None):
        if type(data) is not np.ndarray and header is None:
            raise TypeError(
                "Required parameters are missing or of the incorrect type. Did you mean to use an "
                "alternate, .from_*, constructor?"
            )

        self.data = data
        for f in fields(self):
            if f.name == "data":
                # 'data' is defined in the class but is not a header mapping, so ignore it. We don't use Initvar because
                # we want .data to get typed correctly by a linter.
                continue
            header_key = getattr(self, f.name)
            setattr(self, f.name, header[header_key])

    setattr(cls, "__init__", init_func)

    return dataclass(cls)


@fits_dataclass
class CommonFitsData:
    """
    By-frame header keywords that are not instrument specific
    """

    # Put any common keys here
    elevation: float = "TELEVATN"
    azimuth: float = "TAZIMUTH"
    table_angle: float = "TTBLANGL"
    time_obs: str = "DATE-OBS"
    ip_task_type: str = "DKIST004"
    ip_id: str = "ID___004"

    # Don't touch this. It's here so auto-complete knows we'll have a .data object after initialization
    data: np.ndarray = None

    @classmethod
    def from_hdu(cls, HDU: Union[fits.ImageHDU, fits.PrimaryHDU]) -> Type[CommonFitsData]:
        """
        Convert a single Image or Primary HDU to a CommonFitsData (or child) object

        Parameters
        ----------
        HDU
            A single `astropy.io.fits` HDU object.

        Returns
        ------
        CommonFitsData
            A CommonFitsData or child class. The Data array is accessed via the .data property, as are all other dataclass-like
            variables.
        """
        return cls(HDU.data, HDU.header)

    @classmethod
    def from_hdulist(cls, HDU_list: fits.HDUList) -> Type[CommonFitsData]:
        """
        Convert a `astropy.io.fits.HDUList` to a CommonFitsData (or child) object

        Parameters
        ----------
        HDU_list
            A single `astropy.io.fits.HDUList` object.

        Returns
        ------
        CommonFitsData
            A CommonFitsData or child class. The Data array is accessed via the .data property, as are all other dataclass-like
            variables.
        """
        # Count how many hdus have data in them
        data_hdus = [HDU_list[i].data is not None for i in range(len(HDU_list))]
        number_of_hdus_with_data = sum(data_hdus)
        # Raise errors when number of data arrays != 1
        if number_of_hdus_with_data == 0:
            raise ValueError(f"Fits file {HDU_list.filename()} does not contain a data array.")
        elif number_of_hdus_with_data > 1:
            raise ValueError(f"Fits file {HDU_list.filename()} contains more than one data array.")
        # Find the single hdu that contains data and yield that array
        target_hdu = HDU_list[np.where(data_hdus)[0][0]]
        return cls.from_hdu(target_hdu)

    @classmethod
    def from_file(cls, fits_filepath: Union[Path, str, BinaryIO]) -> Type[CommonFitsData]:
        """
        Convert a fits filepath or file-like object to a CommonFitsData (or child) object.

        I.e., load in the data as a numpy array and populate the keyword properties.

        Raises error when the number of data arrays in the fits file != 1

        Parameters
        ----------
        fits_filepath
            A path, str, or file-like object (basically anything that can be read with `astropy.io.fits.open`) corresponding
            to a FITS file.

        Returns
        ------
        CommonFitsData
            A CommonFitsData or child class. The Data array is accessed via the .data property, as are all other dataclass-like
            variables.
        """
        hdl = fits.open(fits_filepath)
        return cls.from_hdulist(hdl)
