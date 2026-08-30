from fastapi import APIRouter,Query,Depends
from utils.response import success_response
from routers.users import get_current_user
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from crud.favorite import is_news_favorite,add_favorite_news,remove_favorite_news,get_favorite_list,clear_favorite_news
from schemas.favorite import FavoriteCheckResponse,FavoriteAddRequest,FavoriteListResponse


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
    result = await add_favorite_news(db,user.id,data.news_id)
    return success_response(message="收藏成功",data=result)

@router.delete("/remove")
async def remove_favorite(
    data:FavoriteAddRequest,
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
    ):
    result = await remove_favorite_news(db,user.id,data.news_id)
    return success_response(message="取消收藏成功")

@router.get("/list")
async def get_favorite_list(
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user),
    page: int=Query(1,ge=1),
    page_size: int=Query(10,ge=1,le=100,alias="pageSize")
):  
    rows,total = await get_favorite_list(db,user.id,page,page_size)
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news,favorite_time,favorite_id in rows]
    has_more = total > page * page_size

    data = FavoriteListResponse(List=favorite_list,total=total,has_more=has_more)
    return success_response(message="获取收藏列表成功",data=data)

@router.delete("/clear")
async def clear_favorite(
    db:AsyncSession=Depends(get_db),
    user:User=Depends(get_current_user)
    ):
    count = await clear_favorite_news(db,user.id)
    return success_response(message=f"成功删除{count}条收藏记录")

