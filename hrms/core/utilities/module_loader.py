from .topo_sort_module import topo_sort_modules
from sqlalchemy.orm import configure_mappers
from .read_init_file import import_models_for_module
from .database import Base, engine
import logging
from hrms.core.boot.utils.addons_scanner import scan_addons

log = logging.getLogger("hrms.module_loader")
log.setLevel(logging.INFO)

def loader():
    print("Scanning all manifests...")
    
    modules, addons_dir = scan_addons()

    print("Sorting modules by dependencies...",)
    try:
        load_order = topo_sort_modules(modules)
        print("Module load order:", " -> ".join(load_order))
    except Exception as e:
        log.error("Error sorting modules: %s", e)
    
    for module_name in load_order:
        import_models_for_module(module_name)
        
    configure_mappers()
    log.info("SQLAlchemy mappers configured")