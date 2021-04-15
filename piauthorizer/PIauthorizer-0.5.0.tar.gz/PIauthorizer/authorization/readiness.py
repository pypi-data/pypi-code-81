from fastapi import APIRouter

readiness_router = APIRouter()


# Liveness probe for kubernetes status service
@readiness_router.get("/ready", tags=["Readyness"])
def get_readyness():
    return {"status": "ready"}
