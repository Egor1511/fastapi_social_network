from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.controllers import article_controller, comment_controller, user_controller
from app.core.config.database.db_helper import db_helper
from app.core.logging_config import setup_logging
from app.core.telegram_logger import setup_telegram_logging

setup_logging()
setup_telegram_logging()

app = FastAPI()

app.include_router(user_controller.router, prefix="/users", tags=["Users"])
app.include_router(article_controller.router, prefix="/articles", tags=["Articles"])
app.include_router(comment_controller.router, prefix="/comments", tags=["Comments"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog Service API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
