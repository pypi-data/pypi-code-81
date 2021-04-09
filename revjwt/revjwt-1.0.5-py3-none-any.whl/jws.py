import json
from typing import Any, Dict, List
from urllib.parse import urlparse

import requests
from jwcrypto.jwk import JWK
from jwt.api_jws import PyJWS
from jwt.exceptions import DecodeError

from revjwt.algorithms import KMSAlgorithm

PUB_URL = "https://keys.revtel-api.com/certs.json"
PUB_STG_URL = "https://keys.revtel-api.com/certs-stg.json"
DEP_URL = "https://keys.revtel-api.com/pub.json"


class JWS(PyJWS):
    def __init__(self, options: Any = None) -> None:
        super().__init__(options)  # type: ignore
        self._algorithms = {"RS256": KMSAlgorithm()}

    def decode_complete(
        self,
        jwt: str,
        key: str = "",
        algorithms: List[str] = ["RS256"],
        options: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if options is None:
            options = {}
        merged_options = {**self.options, **options}
        verify_signature = merged_options["verify_signature"]

        if verify_signature and not algorithms:
            raise DecodeError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        payload, signing_input, header, signature = self._load(jwt)  # type: ignore

        json_payload = json.loads(payload.decode())
        iss: str = json_payload["iss"]

        if not iss.startswith("https"):
            iss = "https://" + iss

        try:
            parsed = urlparse(iss)
            host, version = parsed.netloc, parsed.path[-2:]
        except ValueError:
            host, version = DEP_URL, "v1"

        kid = header["kid"]

        if version == "v4":
            env = json_payload["env"]
        elif version == "v3":
            env = host.split(".")[0][-3:]

        if version not in ["v2", "v1"]:
            url = PUB_STG_URL if env == "stg" else PUB_URL
            resp = requests.get(url).json()["keys"]
            try:
                key = [key for key in resp if key["kid"] == kid][0]
            except IndexError:
                raise DecodeError(f"key: {kid} not found")
        else:
            resp = requests.get(DEP_URL).json()
            try:
                key = [key for key in resp if key["kid"] == kid][0]
            except IndexError:
                raise DecodeError(f"key: {kid} not found")

        key_json = JWK.from_json(json.dumps(key))
        key_pem = key_json.export_to_pem()

        self._verify_signature(signing_input, header, signature, key_pem, algorithms)  # type: ignore

        return {
            "payload": payload,
            "header": header,
            "signature": signature,
        }


_jws = JWS()
encode = _jws.encode
decode = _jws.decode_complete
