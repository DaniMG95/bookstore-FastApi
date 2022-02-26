from pydantic import BaseModel
import enum
from fastapi import Query


class Role(enum.Enum):
    admin = "admin"
    personal = "personal"


class User(BaseModel):
    name: str
    password: str
    email: str = Query(..., regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    role: Role