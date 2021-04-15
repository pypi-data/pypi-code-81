"""intracellular tables
"""

import datajoint as dj

from loris.database.schema import (
    subjects, anatomy, equipment, recordings, core
)
from loris.database.attributes import truebool, attachplaceholder, tags
from loris.database.attributes import lookupname, listintervals
from loris.database.schema.base import (
    COMMENTS, NEURAL_RECORDING, ManualLookup, TAGS,
    FilesMixin, DataMixin, ExtensionMixin, DICTTAGS
)


schema = dj.Schema('intracellular')


@schema
class WholeCellRecording(dj.Manual):
    definition = f"""
    # Whole-Cell Patch recordings in Current Clamp.
    recording_id : int auto_increment # integer id number
    ---
    recording_file_id : varchar(63) # custom recording file identifier
    -> subjects.FlySubject
    -> recordings.RecordingSolution
    electrode_resistance: float # resistance in ΜΩ
    access_resistance: float # resistance in ΜΩ
    membrane_resistance: float # resistance in GΩ
    current_injection = 0 : float # current in pA
    recording_temperature = null : float # temperature in Celsius
    recording_time = CURRENT_TIMESTAMP : timestamp # time of recording
    completed = 0 : <truebool> # was the recording completed as intended
    manual_start_time = null : float # in seconds
    manual_end_time = null : float # in seconds
    remove_intervals = null : <listintervals> # list of intervals to remove in seconds
    {TAGS}
    {DICTTAGS}
    {COMMENTS}
    """

    class Files(FilesMixin, dj.Part):
        pass

    class Data(DataMixin, dj.Part):
        pass
