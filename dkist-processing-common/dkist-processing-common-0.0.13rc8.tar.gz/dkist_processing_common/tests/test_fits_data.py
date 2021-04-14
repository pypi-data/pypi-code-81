from pathlib import Path
from uuid import uuid4

import numpy as np
import pytest
from astropy.io import fits

from dkist_processing_common.fits_data import CommonFitsData
from dkist_processing_common.fits_data import fits_dataclass


@pytest.fixture()
def fits_path_with_complete_common_header(tmp_path, complete_common_header):
    """
    A file with data and a header with some common by-frame keywords and a single instrument specific one
    """
    data = np.arange(9).reshape(3, 3)
    hdu = fits.PrimaryHDU(data, header=complete_common_header)
    file_path = tmp_path / Path(f"{uuid4().hex[:6]}.FITS")
    hdu.writeto(file_path)
    yield file_path
    file_path.unlink()
    tmp_path.rmdir()


@pytest.fixture()
def fits_path_with_incomplete_common_header(tmp_path):
    """
    A file with data and a header missing one of the expected common by-frame keywords
    """
    data = np.arange(9).reshape(3, 3)
    hdu = fits.PrimaryHDU(data)
    hdu.header["TELEVATN"] = 6.28
    hdu.header["TAZIMUTH"] = 3.14
    file_path = tmp_path / Path(f"{uuid4().hex[:6]}.FITS")
    hdu.writeto(file_path)
    yield file_path
    file_path.unlink()
    tmp_path.rmdir()


def test_from_path(fits_path_with_complete_common_header):
    """
    Given: a fits file with expected, common by-frame keywords
    When: loading the file with the CommonFitsData class
    Then: all values for common keywords are exposed as properties on the fits_obj class
    """
    fits_obj = CommonFitsData.from_file(fits_path_with_complete_common_header)
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))
    with pytest.raises(AttributeError):
        # Just to make sure this behaves like any other class
        _ = fits_obj.foo


def test_from_HDUList(fits_path_with_complete_common_header):
    """
    Given: a fits file with expected, common by-frame keywords
    When: loading the file with the CommonFitsData class
    Then: all values for common keywords are exposed as properties on the fits_obj class
    """
    hdl = fits.open(fits_path_with_complete_common_header)
    fits_obj = CommonFitsData.from_hdulist(hdl)
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))
    with pytest.raises(AttributeError):
        # Just to make sure this behaves like any other class
        _ = fits_obj.foo


def test_from_single_HDU(fits_path_with_complete_common_header):
    """
    Given: a fits file with expected, common by-frame keywords
    When: loading the file with the CommonFitsData class
    Then: all values for common keywords are exposed as properties on the fits_obj class
    """
    hdu = fits.open(fits_path_with_complete_common_header)[0]
    fits_obj = CommonFitsData.from_hdu(hdu)
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))
    with pytest.raises(AttributeError):
        # Just to make sure this behaves like any other class
        _ = fits_obj.foo


def test_no_header_value(fits_path_with_incomplete_common_header):
    """
    Given: a file with a header with missing common by-frame keywrods
    When: processing the file with the CommonFitsData class
    Then: a KeyError is raised
    """
    with pytest.raises(KeyError):
        metadata = CommonFitsData.from_file(fits_path_with_incomplete_common_header)


def test_as_subclass(fits_path_with_complete_common_header):
    """
    Given: an instrument-specific fits_obj class that subclasses CommonFrameMetadata
    When: processing a file with instrument-specific keywords
    Then: both the common and instrument specific keywords values are available as properties in the derived class
    """

    @fits_dataclass
    class InstFitsData(CommonFitsData):
        foo: str = "INST_FOO"

    fits_obj = InstFitsData.from_file(fits_path_with_complete_common_header)
    assert fits_obj.foo == "bar"
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))


def test_instantiation_with_path():
    with pytest.raises(TypeError):
        CommonFitsData("a/path")


def test_direct_instantiation_header(fits_path_with_complete_common_header):
    """
    Given: a numpy array and a fits Header
    When: instantiating a CommonFitsData object directly
    Then: the resulting object is has the correct properties
    """
    hdu = fits.open(fits_path_with_complete_common_header)[0]
    fits_obj = CommonFitsData(hdu.data, hdu.header)
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))
    with pytest.raises(AttributeError):
        # Just to make sure this behaves like any other class
        _ = fits_obj.foo


def test_direct_instantiation_dictionary(fits_path_with_complete_common_header):
    """
    Given: a numpy array and a fits Header
    When: instantiating a CommonFitsData object directly
    Then: the resulting object is has the correct properties
    """
    hdu = fits.open(fits_path_with_complete_common_header)[0]
    header_dict = dict(hdu.header)
    fits_obj = CommonFitsData(hdu.data, header_dict)
    assert fits_obj.elevation == 6.28
    assert fits_obj.azimuth == 3.14
    assert fits_obj.table_angle == 1.23
    assert fits_obj.time_obs == "1988-05-25T01:23:45.678"
    np.testing.assert_equal(fits_obj.data, np.arange(9).reshape(3, 3))
    with pytest.raises(AttributeError):
        # Just to make sure this behaves like any other class
        _ = fits_obj.foo
