"""imaging tables
"""

import datajoint as dj

from loris.database.schema import (
    subjects, anatomy, equipment, recordings, core
)
from loris.database.attributes import truebool, attachplaceholder, tags
from loris.database.attributes import lookupname, folderpath
from loris.database.schema.base import (
    COMMENTS, NEURAL_RECORDING, ManualLookup,
    FilesMixin, DataMixin, ExtensionMixin
)


schema = dj.Schema('imaging')


@schema
class TwoPhotonRecording(dj.Manual):
    definition = f"""
    {NEURAL_RECORDING}
    -> [nullable] anatomy.NeuronSection
    -> [nullable] anatomy.BrainArea
    voltage_input = 0 : <truebool> # whether voltage input was recorded
    voltage_output = 0 : <truebool> # whether voltage output was recorded
    linescan = 0 : <truebool> # whether linescan was captured or not
    manual_start_time = null : float # manual start time of recording, if offset
    manual_end_time = null : float # manual end time of recording, if offset
    """

    class Files(FilesMixin, dj.Part):
        pass

    class Data(DataMixin, dj.Part):
        pass


@schema
class RawTwoPhotonData(dj.AutoImported):
    definition = """
    -> TwoPhotonRecording
    ---
    rate : float # in Hz
    timestamps : blob@datastore # in seconds
    movie : blob@datastore
    tiff_folder_location = null : <folderpath>
    imaging_offset = null : float #offset of image acquisition in s
    trigger = null : blob@datastore  # recorded trigger
    trigger_timestamps = null : blob@datastore
    field_of_view = null : blob # width, height and depth of image in um
    pmt_gain = null : float # photomultiplier gain
    scan_line_rate = null : float # lines imaged per second
    dimension = null : blob # number of pixels on x, y, and z axes
    location = null : longblob # x, y, and z position of microscope
    laser_power = null : float # pockels
    laser_wavelength = null : float # in nm
    dwell_time = null : float # in s
    microns_per_pixel = null : blob # x, y, z um/px
    metadata_collection = null : blob@datastore
    """


@schema
class MotionCorrectedData(dj.AutoComputed):
    definition = """
    -> RawTwoPhotonData
    ---
    rate : float # in Hz
    timestamps : blob@datastore # in seconds
    movie : blob@datastore
    """


@schema
class ExtractedData(dj.AutoComputed):
    definition = """
    -> MotionCorrectedData
    ---
    """

    class Roi(dj.Part):
        definition = """
        -> ExtractedData
        cell_id : int
        ---
        label = null : varchar(51) # label for Roi
        mask : blob@datastore # array of roi mask (boolean or weighted)
        rate : float # in Hz
        timestamps : blob@datastore # in seconds
        signal : blob@datastore
        metadata = null : blob@datastore # additional data to describe mask
        """
