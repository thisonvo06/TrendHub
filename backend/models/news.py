from datetime import datetime
from sqlalchemy import DateTime, Integer, String, VARCHAR, TEXT, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at : Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="创建时间"
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="更新时间"
    )

class NewsCategory(Base):
    __tablename__ = 'news_category'

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="分类ID")
    name : Mapped[str] = mapped_column(String,unique=True,nullable=False,comment="分类名称")
    sort_order : Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="排序")

    def __repr__(self):
        return f"<NewsCategory(id={self.id},name={self.name},sort_order={self.sort_order})>"


class NewsList(Base):
    __tablename__ = 'news'

    # 创建索引：提升查询速度 ->添加目录
    __table_args__ = (
        Index('idx_news_category_id', 'category_id'), # 高频查询字段
        Index('idx_news_publish_time', 'publish_time'),
    )

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="新闻ID")
    title : Mapped[str] = mapped_column(VARCHAR(255),nullable=False,comment="新闻标题")
    description : Mapped[str] = mapped_column(VARCHAR(500),nullable=False,comment="新闻简介")
    content : Mapped[str] = mapped_column(TEXT,nullable=False,comment="新闻内容")
    image : Mapped[str] = mapped_column(VARCHAR(255),nullable=False,comment="新闻图片")
    author : Mapped[str] = mapped_column(VARCHAR(50),nullable=False,comment="新闻作者")
    category_id : Mapped[int] = mapped_column(Integer,ForeignKey('news_category.id'),nullable=True,comment="分类ID")
    views : Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="点击量")
    publish_time : Mapped[datetime] = mapped_column(DateTime,nullable=False,comment="发布时间")

    def __repr__(self):
        return f"<NewsList(id={self.id},title={self.title},views={self.views})>"


