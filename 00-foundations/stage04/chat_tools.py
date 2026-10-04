from llm import client0
from conversation import HISTORY

def handle_chat(text):
    HISTORY.append({"role":"user","content":text})
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=HISTORY
    )
    answer=response.choices[0].message.content
    HISTORY.append({"role":"assistant","content":answer})
    return answer
