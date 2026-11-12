import os
from dotenv import load_dotenv
from openai import OpenAI
from config import ENV_FILE

load_dotenv(ENV_FILE)

client0=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)
client1=OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
)