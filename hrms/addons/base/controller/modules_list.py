from fastapi import APIRouter, Depends, Request
from hrms.core.security.dependency import require_login
from hrms.core.boot.utils.addons_scanner import scan_addons
from hrms.core.utilities.topo_sort_module import topo_sort_modules
from pathlib import Path
import os
router = APIRouter(dependencies=[Depends(require_login)])

@router.get("/")
def module_list(request:Request):
    modules, addons_dir = scan_addons()
    base_url = str(request.base_url).rstrip("/")

    app_modules = filter(lambda x:x.get('manifest', {}).get('application') is True, modules.values())

    module_name = map(lambda x:x.get('manifest',{}).get('name'), modules.values())

    print(str(module_name))
    modules_cover_images=[]

    for module in app_modules:
        modules_cover_images.append({
            "module_name": module.get('name'),
            "app_name": module.get('manifest',{}).get('name'),
            "cover_image_url": (
                f"{base_url}/media/apps/{module['name']}/{module.get('manifest').get('cover_image')}" if module.get('manifest').get('cover_image') else None
            ),
        })

    return modules_cover_images
    