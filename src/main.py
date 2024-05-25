from src.app import app
from src.bible.router import bible_router
from src.bible_v2.router import router as bible_router_v2


@app.get("/")
def root():
    return "Welcome to bible-api"


app.include_router(bible_router, prefix="/api/v1")
app.include_router(bible_router_v2, prefix="/api/v2")
