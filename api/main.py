from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from hrms.core.router.discover_router import include_routers

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

if not STATIC_DIR.exists():
    raise RuntimeError(f"Static directory does not exist: {STATIC_DIR}")

app = FastAPI(title="HRMS API", version="1.0")
include_routers(app)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")

# def start_app():
#     include_routers(app)
#     return app
    