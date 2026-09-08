from utils.response import success_response
from crud.history import (
    add_history_news,
    get_history_list,
    delete_history_record,
    clear_history_news
)
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.history import (
    HistoryAddRequest,
    HistoryAddResponse,
    HistoryListResponse
)
from utils.auth import get_current_user
from config.db_conf import get_db

router = APIRouter(prefix="/api/history", tags=["history"])


# 添加浏览历史记录
@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    history = await add_history_news(db, data.news_id, user.id)
    # ORM 对象用 model_validate 转换，不能 **data.__dict__（含 _sa_instance_state 且是 snake_case）
    return success_response(message="添加成功", data=HistoryAddResponse.model_validate(history))


# 获取浏览历史列表
@router.get("/list")
async def list_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize")
):
    rows, total = await get_history_list(db, user.id, page, page_size)
    # 过滤 ORM 内部状态字段；id 用历史记录ID，news_id 用新闻ID（前端跳详情依赖它）
    history_list = [
        {
            **{k: v for k, v in news.__dict__.items() if not k.startswith("_")},
            "id": history_id,
            "news_id": news.id,
            "view_time": view_time,
        }
        for news, view_time, history_id in rows
    ]
    has_more = page * page_size < total

    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)
    return success_response(message="获取浏览历史成功", data=data)


# 删除单条浏览记录
@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    affected = await delete_history_record(db, history_id, user.id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="浏览记录不存在")
    return success_response(message="删除成功", data=None)


# 清空浏览历史
@router.delete("/clear")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    count = await clear_history_news(db, user.id)
    return success_response(message="清空成功", data=count)
