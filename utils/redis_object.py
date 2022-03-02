import aioredis
from utils.const import TESTING, REDIS_URL
redis = None

async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
