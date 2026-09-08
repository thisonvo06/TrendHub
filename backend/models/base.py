from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 全局唯一的 ORM 基类
# 所有模型必须继承同一个 Base，否则各自的 MetaData 相互独立，
# 会导致 create_all 只能建出部分表、跨表关系无法解析
class Base(DeclarativeBase):
    pass


# 创建/更新时间混入类：仅给数据库中确实存在这两个字段的表使用
# （news、news_category、user、user_token 有此两列；favorite 只有 created_at；history 只有 view_time）
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,  # 传函数而非 datetime.now()，否则取的是服务启动时刻
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )
