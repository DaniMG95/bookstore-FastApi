from databases import Database
from utils.const import DB_URL, DB_URL_TEST, TESTING

if TESTING:
    db = Database(DB_URL_TEST)
else:
    db = Database(DB_URL)