from pydantic import BaseModel,Field


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

# 规划两个类： 一个新闻模型类 + 一个收藏模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(...,alias="favoriteId")
    favorite_time: datetime = Field(...,alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 收藏列表接口模型响应类
class FavoriteListResponse(BaseModel):
    List: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(...,alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
