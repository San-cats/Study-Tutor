# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

def multiply(a,b):
    return a*b

# 1. 加载 key + 创建客户端（照抄 hello_ai.py）
# 你的代码：
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)
message=[
    {"role":"system","content":"你是一个数学助手。用户给你一道数学题，你要一步一步思考，像老师给学生讲题一样，展现每一步推理过程。最后给出答案。"}
]
print("开始对话，请输入题目：")
print("输入quit结束对话")

while 1:
    question=input()
    if question=="quit":
        print("See You~")
        break
    else:
        message.append({"role":"user","content":question})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
        )
        message.append({"role":"assistant","content":response.choices[0].message.content}) #幽灵消息，此时content=None，应删除
        if response.choices[0].message.tool_calls:
            args=response.choices[0].message.tool_calls[0].function.arguments
            args=json.loads(args)  #JSON 字符串 → Python 对象（dict / 列表）
            result=multiply(args["a"],args["b"])
            message.append({
                "role":"tool",
                "tool_call_id":response.choices[0].message.tool_calls[0].id,
                "content":result #str(result)
            })
            print(response.choices[0].message.content)
        else:
            print(response.choices[0].message.content)