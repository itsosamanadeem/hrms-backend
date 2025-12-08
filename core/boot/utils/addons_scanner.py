from pathlib import Path
from hrms.core.utilities.discover_manifest import discover_manifests

def scan_addons():
    addons_dir = Path(__file__).resolve().parent.parent.parent.parent / "addons"

    modules = {}
    for addon in addons_dir.iterdir():
        if addon.is_dir() and (addon / "__init__.py").exists():
            module = discover_manifests(addon.name)
            modules[addon.name] = module

    return modules, addons_dir