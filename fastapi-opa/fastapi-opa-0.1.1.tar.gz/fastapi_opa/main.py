from typing import Dict

from fastapi import FastAPI

from fastapi_opa import OPAConfig
from fastapi_opa import OPAMiddleware
from fastapi_opa.auth import OIDCAuthentication
from fastapi_opa.auth import OIDCConfig

opa_host = "http://localhost:8181"
oidc_config = OIDCConfig(
    host="http://localhost:8080",
    realm="example-realm",
    app_uri="http://localhost:4000",
    client_id="example-client",
    client_secret="bbb765cd-20ba-44a3-9291-136307a36906",
)  # nosec
oidc_auth = OIDCAuthentication(oidc_config)
opa_config = OPAConfig(authentication=oidc_auth, opa_host=opa_host)

app = FastAPI()
app.add_middleware(OPAMiddleware, config=opa_config)


@app.get("/")
async def root() -> Dict:
    return {
        "msg": "success",
    }


@app.get("/finance/salary/{name}")
async def salary(name: str) -> Dict:
    return {"msg": "success", "name": name}
