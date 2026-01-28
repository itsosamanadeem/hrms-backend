from pydantic import BaseModel
from typing import List, Any

class SearchReadPayload(BaseModel):
    model: str
    fields: List[str]
    domain: List[Any] = []
    limit: int = 20
    offset: int = 0
