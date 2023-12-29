from core.database import Database


async def get_db():
    db = Database()
    try:
        yield db
    finally:
        # Close the database connection when the request is done
        db.close()
