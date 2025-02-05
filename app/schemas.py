from pydantic import BaseModel
from typing import Optional

class ItemRequest(BaseModel):
    text: str

class ItemResponse(BaseModel):
    id: int
    text: str
    Location: Optional[str]
    geometry: Optional[str]