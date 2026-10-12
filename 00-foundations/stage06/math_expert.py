import json
from llm import client0
from math_tools import tools,tool_function

MATH_HISTORY=[]
MATH_SYSTEM="你是数学专家，计算问题用工具解决"

def math_expert_agent(task):
    MATH_HISTORY.append({"role":"user","content":task})
    while 1:
        response = client0.chat.completions.create(
            model="deepseek-chat",
            messages=MATH_HISTORY+[{"role":"system","content":MATH_SYSTEM}],
            tools=tools
        )
        if response.choices[0].message.tool_calls:
            print("工具调用")
            MATH_HISTORY.append(response.choices[0].message.model_dump())
            for tc in response.choices[0].message.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                func = tool_function[name]
                result = func(**args)
                MATH_HISTORY.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": str(result)
                    }
                )
        else:
            MATH_HISTORY.append({"role": "assistant", "content": response.choices[0].message.content})
            break
    return response.choices[0].message.content