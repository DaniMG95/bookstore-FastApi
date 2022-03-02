import pickle

from fastapi import FastAPI, Depends, HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token, check_jwt_token
from models.jwt_user import JWTUser
from utils.const import DESCRIPTION_JWT_TOKEN, SUMMARY_JWT_TOKEN, REDIS_URL
from utils.db_object import db
import aioredis
import utils.redis_object as re
from utils.redis_object import check_test_redis

app = FastAPI(title="Bookstore API Documentation", description="It is an API is used for bookstores", version="1.0.0")

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])


@app.on_event("startup")
async def connect_db():
    await db.connect()
    re.redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()
    re.redis.close()
    await re.redis.wait_closed()

@app.post("/token",description=DESCRIPTION_JWT_TOKEN,summary=SUMMARY_JWT_TOKEN)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    redis_key = f"token:{form_data.username},{form_data.password}"
    await re.redis.delete(redis_key)
    user = await re.redis.get(redis_key)
    if not user:
        jwt_user_dict = {"username": form_data.username, "password": form_data.password}
        jwt_user = JWTUser(**jwt_user_dict)
        user = await authenticate_user(jwt_user)
        print(pickle.dumps(user, 0))
        await re.redis.set(redis_key, pickle.dumps(user), ex=10)
        if not user:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    else:
        user = pickle.loads(user)
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}



@app.middleware("http")
async def middleware(request: Request, call_next):
    star_time = datetime.utcnow()
    response = await call_next(request)
    execution_time = (datetime.utcnow() - star_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    # modify response
    return response

