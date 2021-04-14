"""
The 'other side' of communications for MMLibraryViaVolume.  Watches for requests appearing in a folder as JSON
files, and transmits them to a remote REST API.
"""
import os
import json
import time

from ..to_rest import DSLibraryViaREST


class VolumeWatcher(object):
    def __init__(self, volume: str, mmlibrary_rest: DSLibraryViaREST):
        self._volume = volume
        self._mm = mmlibrary_rest

    def scan_forever(self, callback=None, interval: float=0.05):
        """
        Scan repeatedly.  The supplied callback can raise an exception to stop the process.
        """
        while True:
            time.sleep(interval)
            if callback:
                callback()
            self.scan_once()

    def scan_once(self):
        """
        Scan for new requests.
        """
        for f in os.listdir(self._volume):
            if not f.endswith(".json"):
                continue
            try:
                fn = os.path.join(self._volume, f)
                with open(fn) as f_r:
                    request = json.load(f_r)
            except ValueError:
                continue
            response = self.process(request)
            # send response (if request file still exists)
            if os.path.exists(fn):
                response_fn = fn + ".response"
                response_tmp = fn + ".tmp"
                # write to temporary file
                with open(response_tmp, 'wb') as f_w:
                    if isinstance(response, (bytes, bytearray)):
                        f_w.write(response)
                    elif isinstance(response, str):
                        f_w.write(response.encode("utf-8"))
                    else:
                        json.dump(response, f_w)
                # rename to expected location
                os.rename(response_tmp, response_fn)

    def process(self, request: dict):
        return self._mm._do_comm(
            method=request["method"], path=request["path"], params=request["params"],
            data=request["data"], as_json=request["as_json"]
        )
