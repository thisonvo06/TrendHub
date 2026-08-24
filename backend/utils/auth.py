from fastapi import HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from datetime import datetime, timedelta
from crud.users import get_user_by_token
from config.db_conf import get_db


# # 从请求头中获取token
# async def get_token_from_header(authorization: str = Header(...,alias="Authorization")):
#     # Authorization: Bearer <token>
#     token = authorization.split(" ")[1]
#     return token

# 整合 根据token查询用户，返回用户
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(...,alias="Authorization")
):
    token = authorization.replace("Bearer ", "")
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="token无效")
    return user