from fastapi import APIRouter

from app.api.controllers import article_controller, comment_controller, user_controller

router = APIRouter()
router.include_router(user_controller.router, prefix="/users", tags=["users"])
router.include_router(article_controller.router, prefix="/articles", tags=["articles"])
router.include_router(comment_controller.router, prefix="/comments", tags=["comments"])
