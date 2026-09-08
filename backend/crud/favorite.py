from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import NewsList
from sqlalchemy import func, select, delete


# 查询当前用户对某条新闻的收藏记录（没有则返回 None）
async def get_favorite_record(db: AsyncSession, user_id: int, news_id: int):
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 检查收藏状态：当前用户是否收藏了这一条新闻
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    record = await get_favorite_record(db, user_id, news_id)
    # 是否有收藏记录
    return record is not None


# 添加收藏新闻
async def add_favorite_news(db: AsyncSession, user_id: int, news_id: int):
    # 幂等处理：已收藏过则直接返回已有记录，避免触发 user_news_unique 唯一约束
    existed = await get_favorite_record(db, user_id, news_id)
    if existed:
        return existed

    favorite = Favorite(user_id=user_id, news_id=news_id)
    # AsyncSession.add() 是同步方法，不能 await
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 删除收藏新闻
async def remove_favorite_news(db: AsyncSession, user_id: int, news_id: int):
    # 必须查出 ORM 对象再 delete（is_news_favorite 返回的是 bool，不能直接删）
    favorite = await get_favorite_record(db, user_id, news_id)
    if favorite:
        await db.delete(favorite)
        await db.commit()
        return favorite
    else:
        return None


# 获取收藏新闻列表
async def get_favorite_list(
    db: AsyncSession,
    user_id: int,
    page: int,
    page_size: int
):
    # 总量 + 收藏的新闻列表
    count = select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
    count_result = await db.execute(count)
    total = count_result.scalar_one()

    # 收藏的新闻列表 - 联表查询 join() + 收藏时间排序 + 分页
    # select(查询主体模型类，字段别名).join(联合查询模型类，关联条件).where().order_by().offset().limit()
    # 得到的是元组列表 [(新闻对象，收藏时间，收藏ID)]
    query = (select(NewsList, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
            .join(Favorite, NewsList.id == Favorite.news_id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 清空收藏新闻:清空当前用户收藏列表
async def clear_favorite_news(db: AsyncSession, user_id: int):
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    # 返回一个删除的数量
    return result.rowcount or 0
