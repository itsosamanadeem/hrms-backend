from .discover_manifest import discover_manifests
from .topo_sort_module import topo_sort_modules
from sqlalchemy.orm import configure_mappers, registry
from .read_init_file import import_models_for_module
from .database import Base, engine
import logging

log = logging.getLogger("hrms.module_loader")
log.setLevel(logging.INFO)

def loader(base_module="addons"):
    print("Scanning all manifests...")
    modules = discover_manifests(base_module)

    print("Sorting modules by dependencies...",)
    try:
        load_order = topo_sort_modules(modules)
    except Exception as e:
        log.error(e)

    print("Module load order:", " -> ".join(load_order))
    
    for module_name in load_order:
        import_models_for_module(module_name)
        
    configure_mappers()
    log.info("SQLAlchemy mappers configured")