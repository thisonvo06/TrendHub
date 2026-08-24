from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, general_exception_handler
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def register_exception_handler(app: FastAPI):
    """
    注册异常处理函数：子类在前，父类在后；具体在前，通用在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler) # 业务异常
    app.add_exception_handler(IntegrityError, integrity_error_handler) # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) # 数据库错误
    app.add_exception_handler(Exception, general_exception_handler) # 兜底异常
