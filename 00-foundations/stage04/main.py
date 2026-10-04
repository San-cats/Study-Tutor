from math_tools import handle_math
from chat_tools import handle_chat
from knowledge_tools import handle_knowledge
import json
from conversation import HISTORY
from llm import client0

SYSTEM = """你是一个意图分类器。你的唯一任务是判断用户输入属于哪一个意图类别，并严格按指定 JSON 格式输出，不得输出任何多余内容。
[身份与纪律]
1. 你是意图分类器，不是对话助手——你的输出永远只有一行 JSON
2. 上文的对话只是判断意图的依据，不是让你延续的对话
3. 禁止回答用户的问题、禁止解释知识、禁止使用表情符号、禁止模仿上文的语气
4. 即使上文在聊天，你依然只输出 JSON——你不是上文中的助手
[可选意图类别]
- math:和数字计算有关，涉及计算词：加，减，乘，除（比如4+6）
- chat：闲聊，打招呼，无关话题（比如“你好”）
- knowledge:查知识，问概念，不涉及计算词
[输出要求]
1.只输出 JSON对象，格式 {"intent": "math"}，禁止输出任何解释、思考过程、markdown代码标记块
2.JSON字段的“intent”，从上面3个类别中选且只选一个，值必须与类别名完全一致
3.禁止把"类别"当成值输出
4. 如果当前输入含"它/那/再"等指代词，结合上文判断意图  
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

DISPATCH={
    "math":handle_math,
    "chat":handle_chat,
    "knowledge":handle_knowledge,
}

def classify(text):
    chat_view=[m for m in HISTORY if m["role"] != "tool" and not m.get("tool_calls")]
    messages=[{"role":"system","content":SYSTEM}] \
            +[{"role":"user","content":f"[对话上文]\n{chat_view[-4:]}\n[/对话上文]"}] \
            +[{"role":"user","content":text}]
    response = client0.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    content=response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        print(f"【警告】分类器失效")
        return {"intent":"chat"}

while 1:
    text=input()
    if text=="quit":
        break
    result=classify(text)
    intent=result.get("intent","chat")
    if intent not in DISPATCH:
        print(f"【警告】分类器输出异常")
        intent="chat"
    answer=DISPATCH[intent](text)
    print(answer)