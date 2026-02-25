from typing import Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None
    roles: list[str] = []
