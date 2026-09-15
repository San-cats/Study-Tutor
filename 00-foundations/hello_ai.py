# -*- coding: utf-8 -*-
"""
环境验证脚本 —— 测试 AI 是否通
运行: python hello_ai.py
"""

"""
和 hello_ai.py 唯一的区别是：hello_ai 的问题是写死在代码里的，你改成了让用户输入。

这一行就是最核心的变化：


question = input("请输入你的问题：")
其余都是搭建通信通道的固定写法，以后写一百个 AI 脚本，开头那几行基本都不变。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 读取 API Key
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
api_key = os.getenv("DEEPSEEK_API_KEY")

# 2. 创建客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

# 3. 发送请求
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，用一句话介绍你自己"},
    ],
)

# 4. 打印回答
print(response.choices[0].message.content)
