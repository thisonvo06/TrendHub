from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from sqlalchemy import select,update
from schemas.users import UserRequest,UserUpdateRequest
from utils.security import get_password_hash,verify_password
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException



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
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
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

# 根据token查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if not user_token:
        return None
    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息：update更新 -> 检查是否命中 -> 获取更新后的用户返回
async def update_user(user_data: UserUpdateRequest, user: User, db: AsyncSession):
    #update(User).where(User.id == user.id).values(字段=值,字段=值,...)
    # user_data是一个Pydantic类型，得到字典 -> **解包
    # 没有设置值的不更新
    query = update(User).where(User.id == user.id).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
        ))
    result = await db.execute(query)
    await db.commit()
    # 检查更新是否命中数据库
    if result.rowcount == 0:
        return HTTPException(status_code=404, detail="用户不存在")
    # 获取更新后的用户
    updated_user = await get_user_by_username(db, user.username)
    return updated_user

async def change_password(old_password: str, new_password: str, user: User, db: AsyncSession):
    # 验证旧密码
    if not verify_password(old_password, user.password):
        return False
    # 密码加密 -> 存储到数据库中
    password_hashed = get_password_hash(new_password)
    user.password = password_hashed
    # 更新：由SQLAlchemy真正接管这个User对象，确保可以commit
    # 规避session过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库读回用户信息，确保密码已加密存储
    return True

