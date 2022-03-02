from starlette.testclient import TestClient
from run import app
from utils.db import fetch, execute
import asyncio
from utils.security import get_hashed_password
from models.user import User

client = TestClient(app)
loop = asyncio.get_event_loop()


def insert_user(username, password):
    query = """insert into users(username, password) values(:username, :password)"""
    password = get_hashed_password(password)
    values = {"username": username, "password": password}
    loop.run_until_complete(execute(query, False, values))


def check_personel(username, mail):
    query = """select * from personel where username=:username and mail=:mail"""
    values = {"username": username, "mail": mail}
    result = loop.run_until_complete(fetch(query, True, values))
    if result is None:
        return False
    return True


def get_auth_header():
    insert_user("test", "test")
    response = client.post("/token", dict(username="test", password="test"))
    jwt_token = response.json()["access_token"]
    auth_header = {"Authorization": f"Bearer {jwt_token}"}
    return auth_header


def clear_db():
    tables = ["users", "authors", "books", "personel"]
    for table in tables:
        query = f"""delete from {table};"""
        loop.run_until_complete(execute(query, False))


def test_token_succesful():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass1"))

    assert response.status_code == 200
    assert "access_token" in response.json()

    clear_db()


def test_token_unathorized():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass"))

    assert response.status_code == 401

    clear_db()


def test_post_user():
    auth_header = get_auth_header()

    user_dict = {"name": "user1", "password": "secret", "mail": "a@b.com", "role": "admin"}
    response = client.post("/v1/user", json=user_dict, headers=auth_header)

    assert response.status_code == 201
    assert check_personel("user1", "a@b.com") == True

    clear_db()

def test_post_user_wrong_email():
    auth_header = get_auth_header()

    user_dict = {"name": "user1", "password": "secret", "mail": "a@basdsadm", "role": "admin"}
    response = client.post("/v1/user", json=user_dict, headers=auth_header)

    assert response.status_code == 422

    clear_db()




