from .utilities.database import SessionLocal
from .utilities.view_loader_utility import view
from .models.db import DynamicDBSaveForModules as DDSFM
from core.utilities.discover_manifest import discover_manifests
from core.utilities.topo_sort_module import topo_sort_modules
from sqlalchemy.orm import configure_mappers, registry

def loader(base_module="addons"):
    db = SessionLocal()

    print("Scanning all manifests...")
    modules = discover_manifests(base_module)

    print("Sorting modules by dependencies...")
    load_order = topo_sort_modules(modules)

    print("Final Module Load Order:")
    for m in load_order:
        print(f" → {m}")

    for module_name in load_order:
        module_data = modules[module_name]
        manifest_data = module_data["manifest"]

        try:
            print(f"Loading module: {module_name}")

            DDSFM.save_model_to_db(db, module_name)

        except Exception as e:
            print(f"Failed loading {module_name}: {e}")

    print("Finalizing ORM mappings...")


    for module_name in load_order:
        module_data = modules[module_name]
        manifest_data = module_data["manifest"]

        try:
            view(db, module_name, manifest_data, f"{base_module}.{module_name}")
        except Exception as e:
            print(f"Failed loading views for {module_name}: {e}")
