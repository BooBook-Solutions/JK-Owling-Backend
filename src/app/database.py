from app.settings import DB_TYPE
from core.database.database import get_database


async def get_db():
    db = get_database(DB_TYPE)
    try:
        yield db
    finally:
        # Close the database connection when the request is done
        db.close()
