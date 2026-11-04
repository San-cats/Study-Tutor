import json,os
from dotenv import load_dotenv
from openai import OpenAI
from embedding_rag import load_chunks,retrieve,build_prompt,embed

CHUNKS=load_chunks()
CHUNK_VECTORS=[(name,text,embed(text)) for name,text in CHUNKS]
load_dotenv("F:\\AI agent\\.env")

client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

CHAT_HISTORY=[]
MATH_HISTORY=[]
KNOW_HISTORY=[]

SYSTEM = """你是一个意图分类器。你的唯一任务是判断用户输入属于哪一个意图类别，并严格按指定 JSON 格式输出，不得输出任何多余内容。
[可选意图类别]
- math:和数字计算有关，涉及计算词：加，减，乘，除（比如4+6）
- chat：闲聊，打招呼，无关话题（比如“你好”）
- knowledge:查知识，问概念，不涉及计算词
[输出要求]
1.只输出 JSON对象，格式 {"intent": "math"}，禁止输出任何解释、思考过程、markdown代码标记块
2.JSON字段的“intent”，从上面3个类别中选且只选一个，值必须与类别名完全一致
3.禁止把"类别"当成值输出
[输出示例]
示例1:
输入:帮我计算5+8
输出：{"intent":"math"}

示例2:
输入:今天天气多云
输出:{"intent":"chat"}

示例3:
输入:RAG是什么意思
输出:{"intent":"knowledge"}
"""

def handle_chat(text):
    CHAT_HISTORY.append({"role":"user","content":text})
    response=client.chat.completions.create(
        model="deepseek-chat",
        messages=CHAT_HISTORY
    )
    answer=response.choices[0].message.content
    CHAT_HISTORY.append({"role":"assistant","content":answer})
    return answer

def handle_math(text):
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

    tool_funtion={
        "add":add,
        "subtract":subtract,
        "multiply":multiply,
        "divide":divide,
    }
    tools=[
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
    MATH_HISTORY.append({"role": "user", "content": text})
    while 1:
        response=client.chat.completions.create(
            model="deepseek-chat",
            messages=MATH_HISTORY,
            tools=tools
        )
        if response.choices[0].message.tool_calls:
            print("工具调用")
            MATH_HISTORY.append(response.choices[0].message)
            for tc in response.choices[0].message.tool_calls:
                name=tc.function.name
                args=json.loads(tc.function.arguments)
                func=tool_funtion[name]
                result=func(**args)
                MATH_HISTORY.append(
                    {
                        "role":"tool",
                        "tool_call_id":tc.id,
                        "content":str(result)
                    }
                )
        else:
            MATH_HISTORY.append({"role":"assistant","content":response.choices[0].message.content})
            break
    return response.choices[0].message.content


def handle_knowledge(text):
    results=retrieve(text,CHUNK_VECTORS)
    prompt=build_prompt(text,results)
    messages = [
                   {"role": "system", "content": "你是问答知识库，只根据参考资料回答"},
               ] + KNOW_HISTORY + [
                   {"role": "user", "content": prompt},
               ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    answers = response.choices[0].message.content
    KNOW_HISTORY.append({"role": "user", "content": text})
    KNOW_HISTORY.append({"role": "assistant", "content": answers})
    return answers


DISPATCH={
    "math":handle_math,
    "chat":handle_chat,
    "knowledge":handle_knowledge,
}

while 1:
    text=input()
    if text=="quit":
        break
    response=client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":text},
        ]
    )
    result=json.loads(response.choices[0].message.content)
    print(f"识别为 {result['intent']} 意图")
    func=DISPATCH[result["intent"]]
    answer=func(text)
    print(answer)