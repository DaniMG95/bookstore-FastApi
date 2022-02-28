
from utils.db import execute, fetch
from models.jwt_user import JWTUser


async def db_check_token_user(user: JWTUser):
    query = """select * from users where username = :username"""
    values = {"username": user.username}
    result = await fetch(query, False, values)
    if result is None:
        return None
    return result


async def check_jwt_username(username: str):
    query = """select * from users where username = :username"""
    values = {"username": username}
    result = await fetch(query, True, values)
    if result is None:
        return False
    return True


async def db_insert_personal(user):
    query = """insert into personel(username, password, mail, role) values(:name, :password, :email, :role)"""
    values = dict(user)
    await execute(query, False, values)


async def db_check_personel(username, password):
    query = """select * from personel where username = :username and password = :password"""
    values = {"username": username, "password": password}
    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True


async def get_book_with_isbn(isbn):
    query = """select * from books where isbn=:isbn"""
    values = {"isbn": isbn}
    book = await fetch(query, True, values)
    return book

async def get_author(name):
    query = """select * from authors where name=:name"""
    values = {"name": name}
    author = await fetch(query, True, values)
    return author


async def get_author_from_id(id):
    query = """select * from authors where id=:id"""
    values = {"id": int(id)}
    author = await fetch(query, True, values)
    return author

async def patch_author_name(id, name):
    query = """update authors set name=:name where id=:id"""
    values = {"name": name, "id":id}
    await execute(query, False, values)

