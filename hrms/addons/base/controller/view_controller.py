from fastapi import APIRouter, Depends, HTTPException
from hrms.core.utilities.database import get_db
from hrms.addons.base.model.ir_hr_view import IrHrView
from hrms.addons.base.model.ir_hr_model import IrHrModel
from hrms.addons.base.schema.view_schema import ReadViewSchema
from hrms.core.security.dependency import require_login
from hrms.core.utilities.all_modules_in_addons import get_all_modules_in_addons

router = APIRouter(prefix="/hrms", tags=["HRMS Views"], dependencies=[Depends(require_login)])

VIEW_PRIORITY={
    "list": 1,
    "kanban": 2,
    "form": 3
}

@router.get("/{module_name}")
def get_view(module_name: str,db=Depends(get_db)):
    if module_name not in get_all_modules_in_addons():
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found in addons")
    
    models = db.query(IrHrModel).filter(
        IrHrModel.module_name == module_name
    ).all()

    serialized_views = []
    view_type = set()
    for model in models:
        for v in model.views:
            serialized_views.append({
                "id": v.id,
                "name": v.name,
                "view_type": v.view_type,
                "priority": VIEW_PRIORITY.get(v.view_type, 99),
                "arch": v.json_data
            })
            view_type.add(v.view_type)

    if not serialized_views:
        raise HTTPException(404, "No views found for module")

    action = {
        "type": "ir.actions.act_window",
        "model": models[0].name,  # or pick whichever is correct
        "module": module_name,
        "views": serialized_views,
        "view_type": view_type
    }
    return action