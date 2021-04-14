from fastapi import APIRouter

readyness_router = APIRouter()


# Liveness probe for kubernetes status service
@readyness_router.get("/ready", tags=["Readyness"])
def get_readyness():
    return {"status": "ready"}
