from fastapi import FastAPI, Body, Header, File, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

app_v2 = APIRouter()

@app_v2.get("/user")
async def check_user(password: str):
    return {"request": password}

