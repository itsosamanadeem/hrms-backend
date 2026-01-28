from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.core.security.dependency import require_login
from hrms.addons.base.schema.search_read_schema import SearchReadPayload
from hrms.core.boot.registry.registory import get_model
from sqlalchemy import select
from sqlalchemy import or_, cast, String
from sqlalchemy.sql.sqltypes import Enum as PgEnum

router = APIRouter(prefix="/web/dataset", tags=["BASE"], dependencies=[Depends(require_login)])

def apply_domain_filters(db: Session, payload: SearchReadPayload):
    ModelCls = get_model(payload.model)
    query = db.query(ModelCls)

    or_conditions = []

    for token in payload.domain:
        print("Domain token:", token)
        # Ignore logical operators for now
        if token == "|":
            continue
        
        print("Processing token:", token)
        if not isinstance(token, list) or len(token) != 3:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain token: {token}"
            )

        field_name, operator, value = token


        if not hasattr(ModelCls, field_name):
            continue

        field = getattr(ModelCls, field_name)

        if operator == "ilike":
            if isinstance(field.type, PgEnum):
                or_conditions.append(cast(field, String).ilike(f"%{value}%"))
            else:
                or_conditions.append(field.ilike(f"%{value}%"))
            # or_conditions.append(field.ilike(f"%{value}%"))
        elif operator == "like":
            or_conditions.append(field.like(f"%{value}%"))
        elif operator == "=":
            or_conditions.append(field == value)
        elif operator == "!=":
            or_conditions.append(field != value)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported operator: {operator}"
            )

    if or_conditions:
        query = query.filter(or_(*or_conditions))

    return query

@router.post("/search_read", response_class=JSONResponse)
def search_read(payload: SearchReadPayload, db: Session = Depends(get_db)):
    ModelCls = get_model(payload.model)

    query = db.query(ModelCls)

    if payload.domain:
        query = apply_domain_filters(db, payload)

    total = query.count()

    results = query.offset(payload.offset).limit(payload.limit).all()

    records = [
        
        {field: getattr(r, field) for field in payload.fields }
        for r in results
    ]

    return {
        "records": records,
        "total_record": total,
    }
