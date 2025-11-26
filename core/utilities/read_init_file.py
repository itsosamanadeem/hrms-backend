import importlib
import logging
from typing import Iterable
import pkgutil
# from .iterate_submodules import _iter_model_submodules

log = logging.getLogger("hrms.read_init_file")
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

def import_models_for_module(addon_name: str) -> None:
    pkg_name = f"addons.{addon_name}.model"
    try:
        importlib.import_module(pkg_name)
        log.info(f"Imported package: {pkg_name}")
    except ModuleNotFoundError:
        log.debug(f"No model package: {pkg_name}")


    for sub in _iter_model_submodules(addon_name):
        try:
            importlib.import_module(sub)
            log.info(f"Imported models: {sub}")
        except Exception:
            log.exception(f"Failed importing model submodule {sub}")