from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class OutputOptions:
    output_file_path: Optional[Path] = None
    console: bool = False
    scale: bool = False
    log_reading: bool = False
    save_reading: bool = True
    omit_zero_readings: bool = True
    omit_none_readings: bool = True
    add_timestamp_to_reading: bool = False
    add_timestamp_to_filename: bool = True
