import json
from llm import client0
from math_expert import math_expert_agent
from knowledge_expert import knowledge_expert_agent

SYSTEM="""你是主管Agent，有两个手下:
1.数学专家:处理计算问题
2.知识专家：根据资料库回答知识问题
【规则】
1.闲聊你亲自回答，不用派人
2.一个用户的消息可能需要派多个专家
3.把专家的回答转述给用户，除非用户要求，不然不要暴露你派了谁
【输出示例】
示例1:
输入:帮我计算3+5
输出:调用math_expert_agent函数，进行计算并给出用户答案

示例2:
输入:什么是嵌入
输出:调用knowledge_expert_agent函数，对资料库进行查询并回答用户

示例3:
输入:算一下6+8，再查RAG
输出:调用math_expert_agent函数进行计算，再调用knowledge_expert_agent函数，对资料库进行查询，汇总答案并回答用户
"""

message=[
    {"role":"system","content":SYSTEM}
]

tool_function={
    "math_expert_agent":math_expert_agent,
    "knowledge_expert_agent":knowledge_expert_agent
}

tool=[
    {
        "type":"function",
        "function":{
            "name":"math_expert_agent",
            "description":"数学专家，负责处理计算问题",
            "parameters":{
                "type":"object",
                "properties":{
                    "task":{"type":"string","description":"用户的问题"},
                },
                "required":["task"],
            },
        },
    },
    {
        "type":"function",
        "function":{
            "name":"knowledge_expert_agent",
            "description":"知识专家，负责查询资料库回答知识问题",
            "parameters":{
                "type":"object",
                "properties":{
                    "task":{"type":"string","description":"用户的问题"},
                },
                "required":["task"],
            },
        },
    },
]
while 1:
    task=input()
    if task=="quit":
        break
    message.append({"role":"user","content":task})
    while 1:
        response=client0.chat.completions.create(
            model="deepseek-chat",
            messages=message,
            tools=tool
        )
        if response.choices[0].message.tool_calls:
            message.append(response.choices[0].message.model_dump())
            for tc in response.choices[0].message.tool_calls:
                name=tc.function.name
                args=json.loads(tc.function.arguments)
                func=tool_function[name]
                result=func(**args)
                message.append({
                    "role":"tool",
                    "tool_call_id":tc.id,
                    "content":str(result),
                })
        else:
            print(response.choices[0].message.content)
            message.append({"role":"assistant","content":response.choices[0].message.content})
            break
