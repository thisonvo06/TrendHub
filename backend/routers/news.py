from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news


# 创建API实例
router = APIRouter(prefix="/api/news",tags=["News"])

# 接口实现流程
# 1. 模块化路由 -> API接口规范文档
# 2. 定义模型类 数据库表（数据库设计文档）
# 3. 在 crud文件夹里创建文件，封装操作数据库的方法
# 4. 在路由处理函数里调用crud封装的方法，响应结果

# 定义路由
@router.get("/categories")
async def get_news_categories(db:AsyncSession=Depends(get_db),skip : int=0,limit : int=100):
    categories = await news.get_categories(db,skip,limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
    db:AsyncSession=Depends(get_db),
    category_id : int = Query(...,alias="categoryId"), 
    page : int = Query(1), 
    page_size : int = Query(10, le=100, alias="pageSize")
):
    # 思路：处理分页规则 -> 查询新闻列表 -> 计算总量 -> 计算是否有更多
    # 查询新闻列表
    new_list = await news.get_list(db,category_id,page,page_size)
    # 计算总量
    total = await news.get_total(db,category_id)
    # 计算是否有更多
    has_more = page*page_size + len(new_list) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": new_list,
            "total": total,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(db:AsyncSession=Depends(get_db),id:int=1):
    # 获取新闻详情 + 浏览数+1 + 相关新闻
    detail = await news.get_detail(db,id)
    if not detail:
        raise HTTPException(
            status_code=404,
            detail="news not found"
        )
    await news.update_views(db,detail.id)
    related_news = await news.get_related_news(db,detail.category_id,detail.id)
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "author": detail.author,
            "publishTime": detail.publish_time,
            "categoryId": detail.category_id,
            "views": detail.views,
            "relatedNews": related_news
        }
    }