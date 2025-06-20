from flask_sqlalchemy import SQLAlchemy
from functools import lru_cache


# using a singelton for getting the db.
@lru_cache(maxsize=1)
def get_db_connection():
    return SQLAlchemy()