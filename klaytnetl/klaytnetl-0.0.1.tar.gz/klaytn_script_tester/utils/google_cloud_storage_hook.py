# %%
from google.cloud import storage
import google.auth
import os

# %%
class SimpleGoogleCloudStorageHook:

    _conn = None
    _project_id = None
    _credentials = None
    MEGABYTE = 1024 * 1024

    def __init__(self, credentials, project_id):
        self._credentials = credentials
        self._project_id = project_id
        self._conn = storage.Client(credentials=self._credentials,
                                    project=self._project_id)

    def get_conn(self):
        if self._conn is None:
            self._conn = storage.Client(credentials=self._credentials,
                                        project=self._project_id)
        return self._conn

    # Helps avoid OverflowError: https://stackoverflow.com/questions/47610283/cant-upload-2gb-to-google-cloud-storage
    # https://developers.google.com/api-client-library/python/guide/media_upload#resumable-media-chunked-upload
    def upload_to_gcs(self, gcs_hook, bucket, object, filename, mime_type='application/octet-stream'):
        storage_client = gcs_hook.get_conn()

        bucket = storage_client.bucket(bucket)

        if os.path.getsize(filename) > 10 * self.MEGABYTE:
            blob = bucket.blob(object, chunk_size=10 * self.MEGABYTE)
        else:
            blob = bucket.blob(object)

        blob.upload_from_filename(filename)


    # Can download big files unlike gcs_hook.download which saves files in memory first
    def download_from_gcs(self, gcs_hook, bucket, object, filename):
        storage_client = gcs_hook.get_conn()

        bucket = storage_client.get_bucket(bucket)
        blob_meta = bucket.get_blob(object)

        if blob_meta.size > 10 * self.MEGABYTE:
            blob = bucket.blob(object, chunk_size=10 * self.MEGABYTE)
        else:
            blob = bucket.blob(object)

        blob.download_to_filename(filename)
