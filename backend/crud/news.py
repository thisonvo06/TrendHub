from sqlalchemy import select, func ,update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import NewsCategory,NewsList


async def get_categories(db:AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(NewsCategory).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_list(db:AsyncSession,category_id:int=0,page:int=1,page_size:int=10):
    stmt = select(NewsList).where(NewsList.category_id == category_id).offset((page-1)*page_size).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_total(db:AsyncSession,category_id:int):
    stmt = select(func.count(NewsList.id))
    if category_id:
        stmt = stmt.where(NewsList.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_detail(db:AsyncSession,id:int):
    stmt = select(NewsList).where(NewsList.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_views(db:AsyncSession,news_id:int):
    stmt = update(NewsList).where(NewsList.id == news_id).values(views=NewsList.views+1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的命中了数据 -> 命中返回True
    return result.rowcount > 0

async def get_related_news(db:AsyncSession,category_id:int,news_id:int,limit:int=5):
    # order_by排序 -> 浏览量和发布时间
    stmt = select(NewsList).order_by(
        NewsList.views.desc(), # 默认升序，desc降序
        NewsList.publish_time.desc()).where(
            NewsList.category_id == category_id, 
            NewsList.id != news_id).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式 推导出新闻的核心数据，然后再return
    return [
        {
            "id": news.id,
            "title": news.title,
            "image": news.image,
            "publishTime": news.publish_time,
            "views": news.views,
        }
        for news in related_news
    ]
