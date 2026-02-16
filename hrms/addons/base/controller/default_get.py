from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.core.security.dependency import require_login
from hrms.addons.base.schema.default_get_schema import DefaultGetPayload
from hrms.core.boot.registry.registory import get_model

router = APIRouter(
    prefix="/web/dataset",
    tags=["BASE"],
    dependencies=[Depends(require_login)]
)


def get_defaults_for_model(ModelCls, requested_fields=None):
    """
    Generate default values for a model using SQLAlchemy ORM introspection.
    Includes columns and empty lists for one2many/many2many relationships.
    """
    defaults = {}

    # --- 1. Regular columns ---
    for column in ModelCls.__table__.columns:
        if requested_fields and column.name not in requested_fields:
            continue
        if column.default is not None:
            # Handle SQLAlchemy default (call if callable)
            defaults[column.name] = column.default.arg \
                if not callable(column.default.arg) else column.default.arg()
        else:
            defaults[column.name] = None

    # --- 2. Relationships ---
    for rel_name, rel in ModelCls.__mapper__.relationships.items():
        if requested_fields and rel_name not in requested_fields:
            continue

        # one2many / many2many → empty list
        if rel.direction.name in ("ONETOMANY", "MANYTOMANY"):
            # Optional: nested defaults for child model
            child_cls = rel.mapper.class_
            child_defaults = {}
            for col in child_cls.__table__.columns:
                child_defaults[col.name] = None
            # Pre-fill with one empty row
            defaults[rel_name] = [child_defaults]
        elif rel.direction.name == "MANYTOONE":
            defaults[rel_name] = None

    return defaults


@router.post("/default_get", response_class=JSONResponse)
def default_get(payload: DefaultGetPayload, db: Session = Depends(get_db)):
    print('this is the payload', payload)
    ModelCls = get_model(payload.model)
    requested_fields = set(payload.fields) if payload.fields else None
    
    defaults = get_defaults_for_model(ModelCls, requested_fields=requested_fields)

    # Optional: context-based overrides
    context = payload.context or {}
    if "user_id" in context and hasattr(ModelCls, "user_id"):
        defaults["user_id"] = context["user_id"]
    
    print('this is the default', defaults)
    return {
        "id": None,
        "mode": "create",
        "data": defaults,
    }
