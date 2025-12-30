from fastapi import APIRouter, Depends
from hrms.core.security.dependency import require_login
from hrms.core.boot.utils.addons_scanner import scan_addons
from hrms.core.utilities.topo_sort_module import topo_sort_modules

router = APIRouter(dependencies=[Depends(require_login)])

@router.get("/")
def module_list():
    modules, addons_dir = scan_addons()
    addons = topo_sort_modules(modules)

    return addons
