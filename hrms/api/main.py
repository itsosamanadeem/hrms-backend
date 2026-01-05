from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from hrms.core.router.discover_router import include_routers

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

MEDIA_DIRECTORY = os.getenv('MEDIA_DIRECTORY')

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

if not STATIC_DIR.exists():
    raise RuntimeError(f"Static directory does not exist: {STATIC_DIR}")

app = FastAPI(title="HRMS API", version="1.0")
origin = ['http://localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    '/media/apps',
    StaticFiles(directory=MEDIA_DIRECTORY),
    name="apps_media"
)
include_routers(app)
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse(STATIC_DIR / "favicon.ico")
