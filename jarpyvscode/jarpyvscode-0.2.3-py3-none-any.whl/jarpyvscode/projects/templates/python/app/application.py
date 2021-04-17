"""FastAPI app."""

# Standard library:
import typing as t
from pathlib import Path

# 3rd party:
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# local:
import ${PROJECT_NAME}.constants as c
from ${PROJECT_NAME}.log import logger, logwrap

app = FastAPI()
app.logger = logger  # type: ignore
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
if c.FRONTEND_DIR.is_dir():
    app.mount(
        f"/{c.FRONTEND_DIR}",
        StaticFiles(directory=str(c.FRONTEND_DIR)),
        name="ui",
    )


@app.on_event("startup")
@logwrap()
def startup_event():
    """Handle startup of FastAPI app."""
    logger.info("Startup of FastAPI app server.")


@app.on_event("shutdown")
@logwrap()
def shutdown_event():
    """Handle shutdown."""
    app.logger.info("Application shutdown")


HEROES: t.List[t.Dict[str, t.Union[int, str]]] = [
    {"id": 11, "name": "Dr Nice"},
    {"id": 12, "name": "Narco"},
    {"id": 13, "name": "Bombasto"},
    {"id": 14, "name": "Celeritas"},
    {"id": 15, "name": "Magneta"},
    {"id": 16, "name": "RubberMan"},
    {"id": 17, "name": "Dynama"},
    {"id": 18, "name": "Dr IQ"},
    {"id": 19, "name": "Magma"},
    {"id": 20, "name": "Tornado"},
]


@app.get("/api/hero")
# @logwrap()
async def get_heroes() -> t.List[t.Dict[str, t.Union[int, str]]]:
    """Return list of heroes."""
    logger.info("Request heroes ...")
    return HEROES


@app.get("/api/hero/{hero_id}")
# @logwrap()
async def get_hero(hero_id: int) -> t.Dict[str, t.Union[int, str]]:
    """Return specified hero."""
    hero: t.Dict[str, t.Union[int, str]] = [
        hero for hero in HEROES if hero["id"] == hero_id
    ][0]
    return hero


@app.get("/")
@app.get("/ui/")
@app.get("/ui/{filename}")
# @logwrap()
async def ui(filename: str = "index.html") -> FileResponse:
    """Serve Angular UI."""
    if not Path(c.FRONTEND_DIR / filename).is_file():
        filename = "index.html"
    file_path: Path = Path(c.FRONTEND_DIR / filename)
    return FileResponse(str(file_path))
