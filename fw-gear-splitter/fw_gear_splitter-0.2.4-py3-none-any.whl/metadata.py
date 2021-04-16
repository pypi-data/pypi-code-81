"""Metadata handling."""
import datetime
import re
import typing as t
from collections import Counter

from fw_file.dicom import DICOMCollection
from fw_file.dicom.utils import generate_uid
from fw_meta import fields
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from tzlocal import get_localzone

from . import __version__, pkg_name

VERSION = re.split(r"[^\d]+", __version__)


def add_contributing_equipment(dcm: DICOMCollection) -> None:
    """Helper function to populate ContributingEquipmentSequence."""
    cont_dat = Dataset()
    cont_dat.Manufacturer = "Flywheel"
    cont_dat.ManufacturerModelName = pkg_name
    cont_dat.SoftwareVersions = ".".join(VERSION)

    for dcm_slice in dcm:
        raw = dcm_slice.dataset.raw
        if not raw.get("ContributingEquipmentSequence"):
            raw.ContributingEquipmentSequence = Sequence()
        raw.ContributingEquipmentSequence.append(cont_dat)


def update_modified_attributes_sequence(
    dcm: DICOMCollection,
    modified: t.Dict[str, t.Any],
    mod_system: str = "fw_gear_splitter",
    source: t.Optional[str] = None,
    reason: str = "COERCE",
) -> None:
    """Update modified attributes sequence for a collection.

    Args:
        dcm (DICOMCollection): Collection to modify
        modified (t.Dict[str, Any]): key and value pairs to set.
        mod_system (t.Optional[str], optional): System doing modification.
            Defaults to None.
        source (t.Optional[str], optional): Original source of data.
            Defaults to None.
        reason (str, optional): Reason for modifying, either 'COERCE',
            or 'CORRECT' in order to comply with dicom standard.
                Defaults to 'COERCE'.
    """
    # Modified attributes dataset
    mod_dat = Dataset()
    for key, value in modified.items():
        setattr(mod_dat, key, value)
    # Original attributes dataset
    orig_dat = Dataset()
    # Add Modified attributes dataset as a sequence
    orig_dat.ModifiedAttributesSequence = Sequence([mod_dat])
    if mod_system:
        orig_dat.ModifyingSystem = mod_system
    if source:
        orig_dat.SourceOfPreviousValues = source
    orig_dat.ReasonForTheAttributeModification = reason
    time_zone = get_localzone()
    curr_dt = time_zone.localize(datetime.datetime.now())
    curr_dt_str = curr_dt.strftime("%Y%m%d%H%M%S.%f%z")
    orig_dat.AttributeModificationDateTime = curr_dt_str

    for dcm_slice in dcm:
        # Append original attributes sequence dataset for each dicom
        #   in archive
        raw = dcm_slice.dataset.raw

        if not raw.get("OriginalAttributesSequence", None):
            raw.OriginalAttributesSequence = Sequence()
        raw.OriginalAttributesSequence.append(orig_dat)


def series_nmbr_handle(series_nmbr: t.Optional[str]) -> str:
    """Simple helper to generate and set uid."""
    if series_nmbr:
        return "series-" + str(series_nmbr)
    return "series-1"


def gen_series_uid(dcm: DICOMCollection):
    """Simple helper to generate and set uid."""
    uid = generate_uid()
    dcm.bulk_set("SeriesInstanceUID", uid)


def gen_suffix(dcm: DICOMCollection, series_nmbr: t.Optional[str] = None):
    """Utility to generate suffix from metadata values."""
    series_descr: t.Optional[str] = Counter(
        dcm.bulk_get("SeriesDescription")
    ).most_common()[0][0]
    modality: t.Optional[str] = Counter(
        dcm.bulk_get("Modality")
    ).most_common()[0][0]
    if not series_nmbr:
        series_nmbr = Counter(dcm.bulk_get("SeriesNumber")).most_common()[0][0]
    series_nmbr = series_nmbr_handle(series_nmbr)

    prefix = "_"
    modality = (str(modality) + "-") if modality else ""
    series_descr = ("-" + str(series_descr)) if series_descr else ""

    name = prefix + modality + series_nmbr + series_descr
    return fields.validate_filename(name)


# def add_gear_info(
#    metadata: t.Dict[str, Any],
#    job
# ) -> t.Dict[str, Any]:
#    for file in metadata:
#        file.get('info',{})
#            .get('gears',{})
#            .get('splitter',{})
#            .get(splitter.__version__,[])
#            .append({
#                'job': job.id,
#                'created': job.create_datetime
#            })
# def gen_metadata()
