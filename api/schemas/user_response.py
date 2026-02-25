from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    roles: list[str]
