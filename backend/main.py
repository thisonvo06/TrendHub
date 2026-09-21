from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

# 第一步：先加载 .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env") # 加载根目录 .env（必须在导入 routers/config 之前：db_conf 在导入时就读取 database_url）

# 第二步：再导入路由，确保 db_conf.py 读取时环境变量已就绪
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handler import register_exception_handler

app = FastAPI()

# 注册异常处理器
exception_handler = register_exception_handler(app)

origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite 开发服务器
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, # 允许访问的源
    allow_credentials=True, # 允许携带凭证（Cookie）
    allow_methods=["*"], # 允许的请求方法
    allow_headers=["*"] # 允许的请求头
    )

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
