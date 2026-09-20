import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import read_file

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),".env"))
api_key=os.getenv("DEEPSEEK_API_KEY")
client=OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)
message=[
    {"role":"system","content":"你要根据提供的笔记回答用户问题。如果笔记里没有答案，就说'笔记里没有提到'，不要编造。"}
]
print("AI大爷来啦! ! !")
print("输入quit结束对话")
while 1:
    question=input()
    if question=="quit":
        break
    note=read_file("F:\\AI agent\\sandbox\\笔记.txt")
    prompt=f"我的笔记内容是:\n{note}\n\n用户的问题是:{question}"
    message.append({"role":"user","content":prompt})
    response=client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        )
    print(response.choices[0].message.content)
    message.append({"role": "assistant", "content": response.choices[0].message.content})


