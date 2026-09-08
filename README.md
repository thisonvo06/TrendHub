# TrendHub 新闻资讯应用

前后端分离的新闻资讯 Web 应用：前端使用 Vue 3 + Vant 4，后端使用 FastAPI + SQLAlchemy（异步）+ MySQL。

## 技术栈

| 端 | 技术 |
| --- | --- |
| 前端 | Vue 3、Vite 7、Pinia、Vue Router、Vant 4、Axios |
| 后端 | FastAPI、SQLAlchemy 2.0（async）、aiomysql、bcrypt、Uvicorn |
| 数据库 | MySQL 8.0+（库名 `news_app`） |

## 目录结构

```
TrendHub/
├── backend/            # FastAPI 后端
│   ├── main.py         # 应用入口（FastAPI 实例、CORS、路由注册）
│   ├── routers/        # 路由层（news / users / favorite / history）
│   ├── crud/           # 数据库操作封装
│   ├── models/         # ORM 模型
│   ├── schemas/        # Pydantic 请求/响应模型
│   ├── config/         # 数据库连接配置
│   └── requirements.txt
├── frontend/           # Vue 3 前端
├── data/
│   └── database.sql    # 数据库初始化脚本（建库建表）
├── docs/               # API 规范、设计文档
└── .env.example        # 环境变量示例
```

## 环境要求

- Python 3.13+
- Node.js 18+
- MySQL 8.0+

## 启动步骤

### 1. 初始化数据库

启动本地 MySQL，然后导入初始化脚本（会自动创建 `news_app` 库及全部表）：

```bash
mysql -u root -p < data/database.sql
```

或使用 Navicat 等工具直接运行 `data/database.sql`。

### 2. 配置环境变量

在项目根目录创建 `.env` 文件（可参考 [.env.example](.env.example)），写入数据库连接：

```ini
database_url=mysql+aiomysql://root:你的密码@localhost:3306/news_app?charset=utf8
```

### 3. 启动后端（端口 8000）

```bash
# ① 进入后端目录，创建并激活虚拟环境
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

# ② 安装依赖
pip install -r requirements.txt

# ③ 启动（入口已自动加载根目录 .env）
uvicorn main:app --reload
```

> `.env` 由 `main.py` 顶部的 `load_dotenv` 自动加载，也可在终端手动设置环境变量，优先级高于 `.env`。

启动成功后可访问：

- 接口文档（Swagger UI）：http://localhost:8000/docs
- 备用文档（ReDoc）：http://localhost:8000/redoc

### 4. 启动前端（端口 5173）

新开一个终端：

```bash
cd frontend
npm install
npm run dev
```

启动后访问：http://localhost:5173

前端开发服务器已配置代理（见 `frontend/vite.config.js`），所有 `/api` 请求会自动转发到 `http://localhost:8000`，无需处理跨域。

## 常见问题

| 现象 | 原因 / 解决办法 |
| --- | --- |
| 后端启动报 `database_url` 为 None | 确认根目录存在 `.env` 文件且包含 `database_url=...`（参考 `.env.example`） |
| 后端连不上数据库 | 确认 MySQL 已启动、`.env` 中密码正确、`news_app` 库已通过 `data/database.sql` 创建 |
| 前端接口全部失败 | 先确认后端已在 8000 端口启动（打开 http://localhost:8000/docs 验证） |
| 前端页面能开但样式异常 | 重新 `npm install` 后重启 `npm run dev` |
