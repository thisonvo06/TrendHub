from fastapi import APIRouter,Query,Depends
from utils.response import success_response
from utils.auth import get_current_user
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from crud.favorite import (
    is_news_favorite,
    add_favorite_news,
    remove_favorite_news,
    get_favorite_list as query_favorite_list,
    clear_favorite_news
)
from schemas.favorite import (
    FavoriteCheckResponse,
    FavoriteAddRequest,
    FavoriteAddResponse,
    FavoriteListResponse
)


router = APIRouter(prefix="/api/favorite", tags=["Favorite"])

@router.get("/check")
async def check_favorite(
    db:AsyncSession=Depends(get_db),
    news_id: int=Query(...,alias="newsId"),
    user:User=Depends(get_current_user)
    ):
    is_favorite = await is_news_favorite(db,user.id,news_id)
    return success_response(message="检查收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorite))

@router.post("/add")
async def add_favorite(
    data:FavoriteAddRequest,
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
    ):
    favorite = await add_favorite_news(db,user.id,data.news_id)
    # ORM 对象不能直接 JSON 序列化（__dict__ 含 _sa_instance_state），用 model_validate 转换
    return success_response(message="收藏成功",data=FavoriteAddResponse.model_validate(favorite))

@router.delete("/remove")
async def remove_favorite(
    news_id: int=Query(...,alias="newsId"),
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
    ):
    # 与 API 文档、前端一致：newsId 走 query 参数而非 JSON body
    await remove_favorite_news(db,user.id,news_id)
    return success_response(message="取消收藏成功",data=None)

@router.get("/list")
async def list_favorite(
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user),
    page: int=Query(1,ge=1),
    page_size: int=Query(10,ge=1,le=100,alias="pageSize")
):
    # 注意：crud 导入时已改名 query_favorite_list，避免与本函数同名导致递归
    rows,total = await query_favorite_list(db,user.id,page,page_size)
    # 过滤 ORM 内部状态字段 _sa_instance_state，再补上收藏自身的时间与ID
    favorite_list = [
        {
            **{k: v for k, v in news.__dict__.items() if not k.startswith("_")},
            "favorite_id": favorite_id,
            "favorite_time": favorite_time,
        }
        for news, favorite_time, favorite_id in rows
    ]
    has_more = page * page_size < total

    data = FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功",data=data)

@router.delete("/clear")
async def clear_favorite(
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
    ):
    count = await clear_favorite_news(db,user.id)
    return success_response(message=f"成功删除{count}条收藏记录",data=None)
