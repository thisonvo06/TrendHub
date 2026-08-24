from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str="success", data=None):
    content = {
        "code": 200, 
        "message": message, 
        "data": data
    }
    # 把任何FastAPI、Pydantic、ORM对象转换成可以被Json安全序列化的数据结构
    return JSONResponse(content=jsonable_encoder(content))
