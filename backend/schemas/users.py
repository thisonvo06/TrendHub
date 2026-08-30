from pydantic import BaseModel,Field,ConfigDict
from typing import Optional


class UserRequest(BaseModel):
    username: str 
    password: str 

# user_info 对应的类：基础类 + Info类
class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")


class UserInfoResponse(UserInfoBase):
    """
    ⽤户信息Info数据模型
    """
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")

    model_config = ConfigDict(
        from_attributes=True  # 允许从 SQLAlchemy ORM 对象直接取值
    )


class UserResponse(BaseModel):
    """
    用户响应数据模型
    """
    token: str
    user_info: UserInfoResponse = Field(...,alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True, # alias/字段名兼容
        from_attributes=True # 允许从ORM对象属性直接取值
    )


# 更新用户信息：基础类 + Info类
class UserUpdateRequest(BaseModel):
    """
    更新用户信息请求数据模型
    """
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


class PasswordUpdateRequest(BaseModel):
    """
    更新密码请求数据模型
    """
    old_password:str = Field(..., description="旧密码")
    new_password:str = Field(..., min_length=6, max_length=20, description="新密码")
