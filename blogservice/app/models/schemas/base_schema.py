from datetime import datetime
from typing import NewType

from pydantic import BaseModel

PyModel = NewType("PyModel", BaseModel)


class BaseSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
