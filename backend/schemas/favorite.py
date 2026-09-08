from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
from typing import List
from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

    model_config = ConfigDict(
        populate_by_name=True # 同时兼容 newsId / news_id
    )

# 添加收藏的响应：对应文档 data: {id, userId, newsId, createTime}
# 字段名必须与 ORM 属性名一致（from_attributes 按字段名取值），alias 负责输出 camelCase
class FavoriteAddResponse(BaseModel):
    id: int
    user_id: int = Field(...,alias="userId")
    news_id: int = Field(...,alias="newsId")
    created_at: datetime = Field(...,alias="createTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 规划两个类： 一个新闻模型类 + 一个收藏模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(...,alias="favoriteId")
    favorite_time: datetime = Field(...,alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 收藏列表接口模型响应类
# 注意：字段名必须是小写 list，与 API 文档和前端解构保持一致
class FavoriteListResponse(BaseModel):
    list: List[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(...,alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
