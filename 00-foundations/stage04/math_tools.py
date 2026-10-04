import json
from llm import client0
from conversation import HISTORY

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "错误，除数不能为0"
    else:
        return a / b

tool_function = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数的和值",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "计算两个数的差值",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "计算两个数的乘积",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "计算两个数的商值",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"},
                },
                "required": ["a", "b"],
            },
        },
    },
]
def handle_math(text):
    HISTORY.append({"role": "user", "content": text})
    while 1:
        response = client0.chat.completions.create(
            model="deepseek-chat",
            messages=HISTORY,
            tools=tools
        )
        if response.choices[0].message.tool_calls:
            print("工具调用")
            HISTORY.append(response.choices[0].message.model_dump())
            for tc in response.choices[0].message.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                func = tool_function[name]
                result = func(**args)
                HISTORY.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": str(result)
                    }
                )
        else:
            HISTORY.append({"role": "assistant", "content": response.choices[0].message.content})
            break
    return response.choices[0].message.content