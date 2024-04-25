from src.app import app
from src.bible.router import bible_router


@app.route("/")
def root():
    return "Welcome to holy-text"


app.include_router(bible_router)
