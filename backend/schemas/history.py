from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
from typing import List, Optional


class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

    model_config = ConfigDict(
        populate_by_name=True # 同时兼容 newsId / news_id
    )

class HistoryAddResponse(BaseModel):
    id: int = Field(...,alias="id")
    user_id: int = Field(...,alias="userId")
    news_id: int = Field(...,alias="newsId")
    view_time: datetime = Field(...,alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 列表项：新闻核心字段 + 历史记录自身信息
# 注意：id 按 API 文档语义表示「历史记录ID」（前端删除时取 item.history_id || item.id）
#      newsId 单独返回，供前端跳转新闻详情使用（否则会用历史ID跳详情而跳错）
class HistoryNewsItemResponse(BaseModel):
    id: int = Field(..., description="历史记录ID")
    news_id: int = Field(..., alias="newsId")
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(..., alias="publishTime")
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryListResponse(BaseModel):
    list: List[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(...,alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
