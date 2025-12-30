import importlib
import pkgutil
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

def include_routers(app: FastAPI, package_name: str = "hrms.addons"):
    """
    Automatically discover all controller modules in addons
    and include routers if they define `router`.
    """
    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if is_pkg:
            continue

        module = importlib.import_module(module_name)
        if hasattr(module, "router") and isinstance(getattr(module, "router"), APIRouter):
            origin = ['http://localhost:5173']
            app.add_middleware(
                CORSMiddleware,
                allow_origins=origin,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            app.include_router(getattr(module, "router"))
            print(f"Included router from: {module_name}")
