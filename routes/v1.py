import json

from fastapi import Body, Header, File, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response
from utils.db_functions import db_insert_personal, db_check_personel, get_book_with_isbn, get_author, get_author_from_id, patch_author_name
from utils.helper_functions import upload_image_to_server
import utils.redis_object as re

app_v1 = APIRouter()

@app_v1.get("/user", tags=["User"])
async def check_user(password: str):
    return {"request": password}


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def create_user(user: User, x_custom:str = Header("default")):
    await db_insert_personal(user)
    return {"result": "personel is created"}

@app_v1.post("/login", status_code=HTTP_201_CREATED, tags=["Personel"])
async def get_user_validation(username:str = Body(...), password:str = Body(...)):
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)
    if result:
        msg = "is valid (redis)"
        result = bool(result)
    else:
        msg = "is valid (db)"
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), ex=10)
    return {msg: result}


@app_v1.put("/user", tags=["User"])
async def update_user():
    return {"Hello World"}


@app_v1.delete("/user", tags=["User"])
async def delete_user():
    return {"Hello World"}


@app_v1.get('/book/{isbn}', response_model=Book, response_model_include=["name", "year"], tags=["Book"])
async def get_book_isbn(isbn: str):
    book = await re.redis.get(isbn)
    if book:
        book = json.loads(book)
    else:
        book = await get_book_with_isbn(isbn)
        author = await get_author(book["author"])
        author_obj = Author(**author)
        book["author"] = author
        await re.redis.set(isbn, json.dumps(dict(book)), ex=10)
        book["author"] = author_obj
        book = Book(**book)
    return book


@app_v1.get('/author/{id}/book', tags=["Book"])
async def get_books_author_category(id: str, order: str = "asc"):
    author = await get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}
    else:
        return {"result": "not exist author"}


@app_v1.patch("/author/{id}/name", tags=["Author"])
async def patch_author_name(id: int, name: str =Body(..., embed=True)):
    await patch_author_name(id, name)
    return {"result": "author updated"}


@app_v1.post('/user/author', tags=["Author"])
async def create_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore": bookstore_name}



@app_v1.post("/user/photo", tags=["User"])
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    await upload_image_to_server(profile_photo)
    return {"file_size": len(profile_photo)}




