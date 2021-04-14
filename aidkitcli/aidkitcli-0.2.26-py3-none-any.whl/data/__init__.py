"""To upload a new data set to aidkit, it has to be compressed as a zip file.
The zip file must contain a folder with the future name of the data set and two
subfolders (INPUT and OUTPUT) with the corresponding CSV files inside.

A data set can consist of multiple files but the number of files in the INPUT
and OUTPUT subfolders must be the same. Moreover, the matching files must be
named the same but with the word INPUT or OUTPUT at the beginning as
appropriate (:ref:`example-structure-data-set`).

Regarding the structure of the CSV files, every row will represent a data
point and every column a different variable.

Once the data set is structured adequately, you only need to upload it once
and then you'll be able to reuse it for future quality analyses
(:ref:`example-upload-data-set`).
"""
from aidkitcli.data_access.upload import upload_data, list_data
