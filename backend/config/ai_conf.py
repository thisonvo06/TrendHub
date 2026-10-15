import os
from dotenv import load_dotenv
from dashscope import DashScope

load_dotenv(override=True)

model = DashScope(
    model_name=os.getenv("AI_MODEL"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
