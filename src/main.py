from src.app import app
from src.bible.router import bible_router


@app.get("/")
def root():
    return "Welcome to bible-api"


app.include_router(bible_router, prefix="/api/v1")
