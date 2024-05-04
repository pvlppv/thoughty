from .root import root_router
from .user import user_router
from .post import post_router
from .answer import answer_router

routers = (
    root_router,
    user_router,
    post_router,
    answer_router
)