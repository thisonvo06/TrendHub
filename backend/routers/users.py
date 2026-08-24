from fastapi import APIRouter,Depends,HTTPException
from models.users import User,UserToken
from schemas.users import UserResponse,UserInfoResponse,UserRequest
from crud.users import create_user, get_user_by_username, create_user_token,authenticate_user
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
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


@router.post("/login")
async def login_user(user_data: UserRequest,db:AsyncSession=Depends(get_db)):
    user = await authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=HTTPException.status_code_401_UNAUTHORIZED, detail="用户名或密码错误")
    user_token = await create_user_token(db, user.id)
    resp = UserResponse(
        token=user_token.token,
        userInfo=UserInfoResponse.model_validate(user)
    )
    return success_response(message="登录成功",data=resp)
    # 登录逻辑：验证用户是否在数据库中 -> 有用户则验证密码；无则提示注册 -> 生成访问令牌 -> 响应结果
    # token检查，若用户有token则直接登录 -> 无token则提示登录响应结果
    # existing_user = await db.execute(select(UserToken).where(UserToken.token != None))
    # if existing_user:
    #     return success_response(message="登录成功",data=existing_user)
    # return HTTPException(status_code=400, detail="用户名不存在,请前往注册")
