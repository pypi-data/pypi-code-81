from os.path import splitext
from pathlib import Path


def add_timestamp_to_filename(output_options, reading_time):
    if output_options.add_timestamp_to_filename:
        path_without_extension = splitext(output_options.output_file_path)[0]
        epoch_seconds = int(reading_time.timestamp())
        file_date_str = reading_time.strftime("%Y-%m-%d_%H-%M-%S")
        return Path(path_without_extension + "_d_" + file_date_str + "_e_" + str(epoch_seconds) + ".json")
    else:
        return output_options.output_file_path
