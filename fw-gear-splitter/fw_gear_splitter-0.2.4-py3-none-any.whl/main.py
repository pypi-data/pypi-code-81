"""Module to run gear."""
import logging
import typing as t
from pathlib import Path

import pandas as pd
from fw_file.dicom import DICOMCollection

from .metadata import (
    add_contributing_equipment,
    gen_series_uid,
    gen_suffix,
    update_modified_attributes_sequence,
)
from .splitter.base import Splitter
from .splitters import (
    EuclideanSplitter,
    JensenShannonDICOMSplitter,
    UniqueTagMultiSplitter,
    UniqueTagSingleSplitter,
)
from .utils import collection_from_df, collection_to_df

log = logging.getLogger(__name__)

SCORE_THRESH = 0.5


def run_individual_split(
    splitter: Splitter, dataframe: pd.DataFrame, **kwargs: t.Any
) -> None:
    """Helper function to run one splitter algorithm."""
    split = splitter.split(dataframe, **kwargs)
    frames_found = split[split["decision"] > 0]
    log.debug(
        "%s found %d localizer frames",
        splitter.__class__.__name__,
        frames_found.shape[0],
    )
    dataframe.loc[dataframe["path"] == split["path"], "score"] += split["decision"]  # type: ignore


def gen_split_score(dcm: DICOMCollection) -> pd.DataFrame:
    """Generate 'voting' score for each frame in DICOM.

    Voting score comes from multiple splitting algorithms and tries to
    find a concensus among these different methods.

    Methods so far:
        1. Split on change in neighboring frames 'ImageOrientationPatient'.
        2. Split on change in neighboring frames 'ImagePositionPatient'.
        3. Split on change in neighboring frames pixel intensity distribution.
        4. Split on unique combo of 'Rows', 'Columns' tags across archive.
        5. Split on unique value of 'ImageType' across archive.
    """
    total: int = 0
    # Need ordering for pairwise splitters
    if all(dcm.bulk_get("InstanceNumber")):
        dcm.sort(key=lambda x: x.InstanceNumber)
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0

        if all(dcm.bulk_get("ImageOrientationPatient")):
            log.debug(
                "ImageOrientationPatient tag present, attempting localizer split.."
            )
            iop_splitter = EuclideanSplitter(
                dcm, decision_val=30, tag="ImageOrientationPatient"
            )
            run_individual_split(iop_splitter, dataframe)
            total += iop_splitter.decision_val
        else:
            log.debug("ImageOrientationPatient tags not all present.")

        if all(dcm.bulk_get("ImagePositionPatient")):
            log.debug(
                "ImagePositionPatient tag present, attempting localizer split.."
            )
            ipp_splitter = EuclideanSplitter(
                dcm, decision_val=30, tag="ImagePositionPatient"
            )
            run_individual_split(ipp_splitter, dataframe)
            total += ipp_splitter.decision_val
        else:
            log.debug("ImagePositionPatient tags not all present.")

        log.debug("Attempting Jensen-Shannon localizer splitter")
        js_splitter = JensenShannonDICOMSplitter(dcm, decision_val=20)
        run_individual_split(js_splitter, dataframe)
        total += js_splitter.decision_val
    else:
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0
    # Try splitting by rows and columns
    if all(dcm.bulk_get("Rows")) and all(dcm.bulk_get("Columns")):
        log.debug("Row and Column tags present, attempting localizer split...")
        row_col_splitter = UniqueTagSingleSplitter(
            dcm, decision_val=30, tags=["Rows", "Columns"]
        )
        run_individual_split(row_col_splitter, dataframe)
        total += row_col_splitter.decision_val
    else:
        log.debug("Row and Column tags not all present.")

    # Try splitting by image type
    # TODO: Leave out for now, refine heuristic looking specificall for
    # 'LOCALIZER' or other manufacturer specific codewords for Localizer
    # frames.
    #    if all(dcm.bulk_get("ImageType")):
    #        log.debug("ImageType tag present, attempting localizer split..")
    #        image_type_splitter = UniqueTagSingleSplitter(
    #            dcm, tags=["ImageType"]
    #        )
    #        run_individual_split(image_type_splitter, dataframe)
    #        total += image_type_splitter.decision_val
    #    else:
    #        log.debug("Row and Column tags not all present.")

    dataframe["score"] /= total
    return dataframe


def run_split_localizer(
    dcm: DICOMCollection,
) -> t.Tuple[DICOMCollection, ...]:
    """Split localizer from dicom archive.

    Args:
        dcm (DICOMCollection): Dicom Archive

    Returns:
        t.Tuple[DICOMCollection, ...]: Tuple of dicom collections,
            first is the main archive, second is the localizer if any.
    """
    log.debug("Generating splitting score")
    score_dataframe = gen_split_score(dcm)

    dicom_dataframe = score_dataframe[score_dataframe["score"] < SCORE_THRESH]
    localizer_dataframe = score_dataframe[
        score_dataframe["score"] >= SCORE_THRESH
    ]
    log.debug("Found %d localizer frames", localizer_dataframe.shape[0])

    if localizer_dataframe.shape[0] >= dicom_dataframe.shape[0] * 0.5:
        log.error("Splitting localizer may have failed...")

    dicom_coll = collection_from_df(dcm, dicom_dataframe)
    localizer_coll = collection_from_df(dcm, localizer_dataframe)
    return (dicom_coll, localizer_coll)


def split_dicom(  # pylint: disable=too-many-locals
    dcm: DICOMCollection,
    file_name: str,
    group_by: t.Optional[t.List[str]],
    split_localizer: bool,
) -> t.Dict[str, DICOMCollection]:
    """Split the dicom archive by tags or localizer.

    Args:
        dcm (DICOMCollection): Dicom archive
        file_name (str): File name of input dicom archive
        group_by (t.Optional[t.List[str]]): List of tags to split by.
        split_localizer (bool): Whether or not to split localizer.

    Returns:
        t.Dict[str, DICOMCollection]: Dictionary with output filenames as
            keys, and Dicom collections.
    """
    outputs = {}

    if group_by:
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0
        tag_splitter = UniqueTagMultiSplitter(dcm, 10, tags=group_by)
        out_dfs = list(tag_splitter.split(dataframe))
        # Sort by number of frames
        out_dfs.sort(key=lambda out_df: out_df.shape[0], reverse=True)
        primary = collection_from_df(dcm, out_dfs[0])
        outputs[file_name] = primary
        if len(out_dfs) > 1:
            for i, out_df in enumerate(out_dfs[1:]):
                secondary = collection_from_df(dcm, out_df)
                series = str(i + 1000)
                name = file_name + gen_suffix(secondary, series_nmbr=series)
                log.info("Added secondary collection named: %s", name)
                outputs[name] = secondary
    else:
        # Add input to outputs dict to have localizer split
        outputs[file_name] = dcm

    if split_localizer:
        localizer_outputs = {}
        for name, archive in outputs.items():
            log.info("Splitting collection %s", name)
            dicom, localizer = run_split_localizer(archive)
            localizer_outputs[name] = dicom
            if localizer and len(localizer) > 0:
                log.info(
                    "Updating modified attributes sequence with original "
                    + "SeriesInstanceUID: %s",
                    dicom[0].SeriesInstanceUID,
                )
                update_modified_attributes_sequence(
                    localizer,
                    modified={"SeriesInstanceUID": dicom[0].SeriesInstanceUID},
                )
                gen_series_uid(localizer)
                log.info(
                    "Adding new SeriesInstanceUID: %s",
                    localizer[0].SeriesInstanceUID,
                )
                localizer_outputs[name + "_localizer"] = localizer
        outputs.update(localizer_outputs)

    return outputs


# Most of this function is already tested in fw_file
def run(
    dcm_path: Path,
    output_dir: Path,
    group_by: t.List[str],
    split_localizer: bool,
) -> t.Tuple[Path, ...]:  # pragma: no cover
    """Main function of module.

    Args:
        dcm_path (Path): Dicom file path
        output_dir (Path): Gear output directory.
        group_by (t.List[str]): List of tags to split by.
        split_localizer (bool): Whether or not to split localizer out.

    Returns:
        t.Tuple[Path]: Tuple of saved output paths.
    """
    with DICOMCollection.from_zip(dcm_path, force=True, stop_when=None) as dcm:
        filename = ""
        if dcm_path.name.endswith(".zip"):
            filename = dcm_path.name.split(".zip")[0]
        if filename.endswith(".dcm"):
            filename = filename.split(".dcm")[0]
        elif filename.endswith(".dicom"):
            filename = filename.split(".dicom")[0]
        suffix = dcm_path.name.split(filename)[1]
        log.debug("Found path stem: %s, suffix: %s", filename, suffix)

        # Don't try to split if there is only one slice.
        if len(dcm) == 1:
            log.info("Only one slice present in archive.")
            return tuple()

        collections = split_dicom(dcm, filename, group_by, split_localizer)
        # If nothing was split out
        if len(collections.items()) == 1:
            log.info("Archive was not split.")
            # Return an empty tuple
            return tuple()
        # Otherwise populate output dir and return saved paths.
        else:
            save_paths = []
            for path, collection in collections.items():
                log.info(
                    "Adding contributing equipment to collection: %s",
                    str(path),
                )
                add_contributing_equipment(collection)
                # save and name
                save_path = output_dir / (path + suffix)
                save_paths.append(save_path)
                collection.to_zip(save_path)

            return tuple(save_paths)
