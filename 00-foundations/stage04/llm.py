import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("F:\\AI agent\\.env")
client0 = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)
client1=OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
)