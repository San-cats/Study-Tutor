# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载 key + 创建客户端（照抄 hello_ai.py）
# 你的代码：
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)
# 2. 用 input() 获取用户输入的问题
# 你的代码：
question=input("请输入您的问题")
# 3. 把问题发给 DeepSeek
# 你的代码：
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": question},
    ],
)
# 4. 打印 AI 的回答
# 你的代码：
print(response.choices[0].message.content)