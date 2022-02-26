from fastapi import FastAPI, Body, Header, File
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

app_v1 = FastAPI(root_path="/v1")

@app_v1.get("/user")
async def check_user(password: str):
    return {"request": password}


@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def create_user(user: User, x_custom:str = Header("default")):
    return {"request": user, "header": x_custom}


@app_v1.put("/user")
async def update_user():
    return {"Hello World"}


@app_v1.delete("/user")
async def delete_user():
    return {"Hello World"}


@app_v1.get('/book/{isbn}', response_model=Book, response_model_include=["name","year"])
async def get_book_isbn(isbn: str):
    author_dict = {
        "name": "aaaaaaaaaa",
        "book": ["sddsa","sdasads"]
    }
    book_dict ={
        "isb": "sdasasda",
        "name": "sadsaddsa",
        "author": author_dict,
        "year": 2019
    }
    book = Book(**book_dict)
    return book


@app_v1.get('/author/{id}/book')
async def get_books_author_category(id: str, order: str, category: str):
    return {"path": id, "path_query": [order, category]}


@app_v1.patch("/author/name")
async def patch_author_name(name: str =Body(..., embed=True)):
    return {"name in body": name}


@app_v1.post('/user/author')
async def create_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore": bookstore_name}



@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file_size": len(profile_photo)}