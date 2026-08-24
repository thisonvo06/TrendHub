from fastapi import APIRouter,Depends
from models.users import User
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import create_user, get_user_by_username, create_user_token
from schemas.users import UserRequest
from fastapi import HTTPException
from schemas.users import UserResponse,UserInfoResponse
from utils.response import success_response



router = APIRouter(prefix="/api/users",tags=["Users"])

@router.post("/register")
async def register_user(user_data: UserRequest, db:AsyncSession=Depends(get_db)):
    # 注册逻辑：验证用户名是否存在 -> 创建用户 -> 生成token -> 响应结果
    existing_user = await get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    UserData = await create_user(user_data, db)
    user_token = await create_user_token(db, UserData.id)

    # 通用成功响应结果 + 全局异常处理器（全局配置在utils.exception_handler.py）：
    # - 成功：抽取响应结果模板 -> 定义数据类型 -> 调用模板和工具函数响应结果
    # - 异常：定义异常处理器 -> 全局注册异常处理器 
    resp = UserResponse(
        token=user_token.token,
        userInfo=UserInfoResponse.model_validate(UserData)
    )

    return success_response(message="注册成功",data=resp)
