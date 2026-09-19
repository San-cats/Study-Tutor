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
messages=[
    {"role":"system","content":"你是一个暴躁的东北大哥，充分体现东北人的豪爽和直性子"}
]
print("开始对话，输入quit退出")
while 1:
    question=input()
    if question=="quit":
        break
    else:
        messages.append({"role":"user","content":question})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        messages.append({"role":"assistant","content":response.choices[0].message.content})
        print(response.choices[0].message.content)