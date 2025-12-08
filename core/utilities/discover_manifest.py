import importlib
import pkgutil
import os

def discover_manifests(base_module):
    """
    Scan all modules inside addons and return:
    {
        module_name: {
            "path": module_path,
            "manifest": manifest_dict
        }
    }
    """
    # print(base_module)
    module_path = ".".join(("hrms","addons",base_module))
    # print(base_module)
    pkg = importlib.import_module(module_path)
    pkg_dir = pkg.__path__[0]  # actual directory on disk

    manifest_file = os.path.join(pkg_dir, "__manifest__.py")

    if not os.path.exists(manifest_file):
        print(f"No manifest for {module_path}")
        return {}

    spec = importlib.util.spec_from_file_location(
        f"{module_path}.__manifest__", manifest_file
    )
    manifest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manifest_module)

    manifest = getattr(manifest_module, "manifest", None)

    return {
        "name": base_module,
        "path": pkg_dir,
        "manifest": manifest,
        "depends": manifest.get("depends", [])        
    }
