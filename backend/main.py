from fastapi import FastAPI
from routers import news,users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
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
