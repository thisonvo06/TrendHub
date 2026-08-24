from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from sqlalchemy import select
from schemas.users import UserRequest
from utils.security import get_password_hash,verify_password
import uuid
from datetime import datetime, timedelta



# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    user = await db.execute(
        select(User).where(User.username == username)
    )
    return user.scalar_one_or_none()

# 创建用户
async def create_user(user_data: UserRequest, db: AsyncSession):
    # 密码加密 -> 存储到数据库中
    password_hash = get_password_hash(user_data.password)
    user = User(username=user_data.username, password=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库读回用户信息，确保密码已加密存储
    return user

# 生成Token
async def create_user_token(db: AsyncSession,user_id:int):
    # 生成Token + 设置过期时间 -> 查询数据库当前用户有无token -> 有则更新token;无则创建token
    token=str(uuid.uuid4())
    # timedelta(days=7, hours=24, minutes=0, seconds=0, microseconds=0, nanoseconds=0)
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(token)
    await db.commit()
    return user_token

# 检验用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    # 检查用户是否存在
    if not user:
        return None
    # 验证密码
    if not verify_password(password, user.password):
        return None
    return user








