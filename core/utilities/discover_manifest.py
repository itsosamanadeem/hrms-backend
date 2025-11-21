import importlib
import pkgutil
import os

def discover_manifests(base_module="addons"):
    """
    Scan all modules inside addons and return:
    {
        module_name: {
            "path": module_path,
            "manifest": manifest_dict
        }
    }
    """
    modules = {}

    package = importlib.import_module(base_module)

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue

        module_path = os.path.join(package.__path__[0], module_name)
        manifest_path = os.path.join(module_path, "__manifest__.py")

        if not os.path.exists(manifest_path):
            print(f"No manifest for {module_name}")
            continue

        spec = importlib.util.spec_from_file_location(
            f"{base_module}.{module_name}.__manifest__", manifest_path
        )
        manifest_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(manifest_module)

        manifest = getattr(manifest_module, "manifest", None)
        if not manifest:
            print(f"Manifest for {module_name} has no variable 'manifest'")
            continue

        modules[module_name] = {
            "path": module_path,
            "manifest": manifest,
            "depends": manifest.get("depends", [])
        }

    return modules
