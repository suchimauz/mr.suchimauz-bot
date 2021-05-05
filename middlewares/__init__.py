from loader import dp
from .throttling import ThrottlingMiddleware
from .last_activity import LastActivityMiddleWare


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LastActivityMiddleWare())
