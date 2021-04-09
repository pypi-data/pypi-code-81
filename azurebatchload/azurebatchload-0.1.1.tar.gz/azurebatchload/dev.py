# flake8: noqa
import time
import os
from azurebatchload import UploadBatch
from azurebatchload.download import DownloadBatch

from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

start = time.time()
# az_batch = DownloadBatch(
#     destination="data/",
#     source="twinfield",
#     folder="xml_responses/vrk/20210330/",
#     method="single",
# )
# az_batch.download()

UploadBatch(
    destination="test",
    folder="data/xml_responses/vrk/20210330",
    extension=".xml",
    method="batch"
).upload()
print(time.time() - start)

