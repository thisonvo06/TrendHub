from fastapi import APIRouter,Depends,HTTPException
from models.users import User,UserToken
from schemas.users import UserResponse,UserInfoResponse,UserRequest,UserUpdateRequest
from crud.users import create_user, get_user_by_username, create_user_token,authenticate_user
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.response import success_response
from utils.auth import get_current_user
from crud.users import update_user



router = APIRouter(prefix="/api/user",tags=["Users"])

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


@router.post("/login")
async def login_user(user_data: UserRequest,db:AsyncSession=Depends(get_db)):
    user = await authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    user_token = await create_user_token(db, user.id)
    resp = UserResponse(
        token=user_token.token,
        userInfo=UserInfoResponse.model_validate(user)
    )
    return success_response(message="登录成功",data=resp)


# 查Token查用户 -> 封装crud -> 功能整合成一个工具函数 -> 路由调用工具函数：注入依赖
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))
    

# 修改用户信息：验证token -> 更新用户信息（put提交） -> 请求体参数 -> 定义Pydantic模型类 -> 响应结果
# 参数
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await update_user(user_data, user, db)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))
    
