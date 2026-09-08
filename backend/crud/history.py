from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import NewsList
from datetime import datetime


# 查询当前用户对某条新闻的浏览记录
async def get_history_record(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 添加浏览历史记录：已浏览过则刷新浏览时间，否则新增一条
async def add_history_news(db: AsyncSession, news_id: int, user_id: int):
    record = await get_history_record(db, user_id, news_id)
    if record:
        # 直接改 ORM 属性，由 SQLAlchemy 在 commit 时生成 UPDATE
        record.view_time = datetime.now()
        await db.commit()
        await db.refresh(record)
        return record

    history = History(user_id=user_id, news_id=news_id)
    # AsyncSession.add() 是同步方法，不能 await，且返回 None
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# 获取浏览历史列表（联表新闻 + 按浏览时间倒序 + 分页）
async def get_history_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    count = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count)
    total = count_result.scalar_one()

    # 得到元组列表 [(新闻对象，浏览时间，历史ID)]
    query = (select(NewsList, History.view_time.label("view_time"), History.id.label("history_id"))
             .join(History, NewsList.id == History.news_id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset((page - 1) * page_size)
             .limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 删除单条浏览记录（同时限定 user_id，避免越权删除他人记录）
async def delete_history_record(db: AsyncSession, history_id: int, user_id: int):
    query = delete(History).where(History.id == history_id, History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0


# 清空当前用户浏览历史
async def clear_history_news(db: AsyncSession, user_id: int):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0
