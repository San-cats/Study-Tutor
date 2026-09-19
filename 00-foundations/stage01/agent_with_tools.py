# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if b==0:
        return "错误，除数不能为0"
    else:
        return a/b

tool_funtion={
    "add":add,
    "subtract":subtract,
    "multiply":multiply,
    "divide":divide,
}
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
tool=[
    {
        "type":"function",
        "function":{
            "name":"multiply",
            "description":"计算两个数的乘积",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number","description":"第一个数"},
                    "b":{"type":"number","description":"第二个数"},
                },
                "required":["a","b"],
            },
        },
    },
{
        "type":"function",
        "function":{
            "name":"add",
            "description":"计算两个数的和值",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number","description":"第一个数"},
                    "b":{"type":"number","description":"第二个数"},
                },
                "required":["a","b"],
            },
        },
    },
{
        "type":"function",
        "function":{
            "name":"subtract",
            "description":"计算两个数的差值",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number","description":"第一个数"},
                    "b":{"type":"number","description":"第二个数"},
                },
                "required":["a","b"],
            },
        },
    },
{
        "type":"function",
        "function":{
            "name":"divide",
            "description":"计算两个数的商值",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"number","description":"第一个数"},
                    "b":{"type":"number","description":"第二个数"},
                },
                "required":["a","b"],
            },
        },
    },
]
print("开始对话，请输入题目：")
print("输入quit结束对话")
while 1:
    question=input()
    if question=="quit":
        print("See You~")
        break
    else:
        message.append({"role": "user", "content": question})
        while 1:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=message,
                tools=tool
            )
            if response.choices[0].message.tool_calls:
                print("AI大爷准备调用工具啦！")
                message.append(response.choices[0].message)
                for tc in response.choices[0].message.tool_calls:
                    name = tc.function.name
                    args = json.loads(tc.function.arguments)
                    func = tool_funtion[name]
                    result = func(args["a"], args["b"])
                    message.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": str(result),
                    })
            else:
                print(response.choices[0].message.content)
                message.append({"role": "assistant", "content": response.choices[0].message.content})
                break