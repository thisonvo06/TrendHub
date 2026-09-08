# 统一导出所有 ORM 模型：
# 1) 保证任意导入顺序下，Base.metadata 都能解析跨表外键
# 2) 支持 from models import User, NewsList, ... 的写法
from models.base import Base
from models.users import User, UserToken
from models.news import NewsCategory, NewsList
from models.favorite import Favorite
from models.history import History

__all__ = [
    "Base",
    "User",
    "UserToken",
    "NewsCategory",
    "NewsList",
    "Favorite",
    "History",
]
