from fastapi import APIRouter,Depends
from models.users import User
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import create_user, get_user_by_username, create_user_token
from schemas.users import UserRequest
from fastapi import HTTPException


router = APIRouter(prefix="/api/users",tags=["Users"])

@router.post("/register")
async def register_user(user_data: UserRequest, db:AsyncSession=Depends(get_db)):
    # 注册逻辑：验证用户名是否存在 -> 创建用户 -> 生成token -> 响应结果
    existing_user = await get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    UserData = await create_user(user_data, db)
    token = await create_user_token(db, UserData.id)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "id": UserData.id,
            "username": UserData.username,
            "bio": UserData.bio,
            "avatar": UserData.avatar,
        }
    }

    