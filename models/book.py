from pydantic import BaseModel, Field
from models.author import Author


class Book(BaseModel):
    isb: str = Field(None, description="This is isbn book")
    name: str
    author: Author
    year: int = Field(None, gt=1900, lt=2100)