from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

# 数据库URL
database_url = os.getenv("database_url")

# 创建异步引擎
async_engine = create_async_engine(
    database_url,
    echo=True, # 输出sql日志
    pool_size=10, #设置连接池中保持的持久连接数
    max_overflow=10 # 设置连接池允许创建的额外连接数
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker[AsyncSession](
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
