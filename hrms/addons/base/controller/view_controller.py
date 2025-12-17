from fastapi import APIRouter, Depends, HTTPException
from hrms.core.utilities.database import get_db
from hrms.addons.base.model.ir_hr_view import IrHrView
from hrms.addons.base.schema.view_schema import ReadViewSchema
from hrms.core.security import get_current_user
from hrms.core.utilities.all_modules_in_addons import get_all_modules_in_addons

router = APIRouter(prefix="/hrms", tags=["HRMS Views"])

@router.get("/{module_name}/{view_name}", response_model=ReadViewSchema)
def get_view(module_name: str, view_name: str, db=Depends(get_db), current_user: str = Depends(get_current_user)):
    if module_name not in get_all_modules_in_addons():
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found in addons")
    view = db.query(IrHrView).filter(IrHrView.name == view_name).first()

    if not view:
        raise HTTPException(status_code=404, detail=f"View '{view_name}' for module '{module_name}' not found")
    return view