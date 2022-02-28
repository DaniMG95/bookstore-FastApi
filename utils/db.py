from utils.db_object import db

async def execute(query: str, is_many: bool, values=None):
    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)



async def fetch(query: str,  is_one: bool, values=None):
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out=None
        else:
            out = []
            for row in result:
                out.append(dict(row))
    return out


