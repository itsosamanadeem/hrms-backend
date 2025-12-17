from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional

class ReadViewSchema(BaseModel):
    view_id: str
    name: str
    model_id: int
    view_type: str
    json_data: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)