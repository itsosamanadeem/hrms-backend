# hrms/addons/base/schema/default_get_schema.py
from pydantic import BaseModel
from typing import List, Dict, Any

class DefaultGetPayload(BaseModel):
    model: str
    fields: List[str] | None = None
    context: Dict[str, Any] | None = None
