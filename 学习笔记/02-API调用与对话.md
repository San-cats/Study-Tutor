# API 调用与对话

## ① 调用 AI 的固定四步

```python
from dotenv import load_dotenv
from openai import OpenAI
import os

# 1. 读密钥（.env 文件里存着 DEEPSEEK_API_KEY）
load_dotenv("F:\\AI agent\\.env")
api_key = os.getenv("DEEPSEEK_API_KEY")

# 2. 创建客户端（通信管道）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",   # DeepSeek 兼容 OpenAI 接口
)

# 3. 发请求
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[...],
)

# 4. 取回答
print(response.choices[0].message.content)
```

## ② 三种 role

| role | 谁说的话 | 作用 |
|------|---------|------|
| `system` | 开发者 | 定人格、定规则，永远在最前面 |
| `user` | 用户 | 用户说的话 |
| `assistant` | AI | AI 自己说的话 |

**system 是"最高指令"**：每次生成前 AI 都会读它。换一行 system，同一个程序从"聊天机器人"变"数学老师"。

system 的局限：太长会被忽略、可以被用户绕过去（prompt injection）、管不了事实。

## ③ AI 没有记忆——记忆 = 反复重发历史

```python
messages = [
    {"role": "system", "content": "你是一个助手"},
]

while True:
    question = input()
    messages.append({"role": "user", "content": question})        # 用户的话入库
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,       # 每次把整段历史都发一遍
    )
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})     # AI的话也入库
    print(answer)
```

AI 是金鱼：每次都要把前文完整塞给它，它才"记得"。

## ④ AI 的本质：只会生成文字

- 看不见你的电脑、不知道实时信息、数学靠猜、知识有截止日期
- 答不出时会**编造**（幻觉），不会老实说不知道
- 工具调用 = 给它装上缺失的器官（眼睛、手、计算器）

## ⑤ 提示词加工

发给 AI 的 content 不一定是用户原话，可以先加工：

```python
question = input()                       # 用户原话
prompt = f"参考资料：\n{note}\n\n问题：{question}"   # 加工后
# 发给 AI 的是 prompt，不是 question
```

AI 不关心是谁说的，你塞什么它看什么——RAG 的原理就在这。
