import logging
from typing import Iterable
import importlib
import pkgutil
log = logging.getLogger("hrms.dynamic_loader")
log.setLevel(logging.INFO)

def _iter_model_submodules(addon_name: str) -> Iterable[str]:
    pkg_name = f"addons.{addon_name}.model"
    try:
        pkg = importlib.import_module(pkg_name)
    except ModuleNotFoundError:
        return []


    if not hasattr(pkg, "__path__"):
        return []


    for finder, mod_name, ispkg in pkgutil.iter_modules(pkg.__path__):
        yield f"{pkg_name}.{mod_name}"