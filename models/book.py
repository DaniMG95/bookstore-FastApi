from pydantic import BaseModel
from models.author import Author


class Book(BaseModel):
    isb: str
    name: str
    author: Author
    year: int