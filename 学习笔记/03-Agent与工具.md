# Agent 与工具调用

## ① 聊天机器人 vs Agent

| | 聊天机器人 | Agent |
|------|------|------|
| 谁主导 | 你问它答 | 它自己思考、行动 |
| 流程 | 输入→回复→等输入 | 目标→思考→行动→观察→再思考... |
| 结束 | 你退出 | 它自己判断"做完了" |

Agent 的核心循环：**思考 → 行动 → 观察结果 → 再思考 → ... → 完成**

## ② 函数调用完整流程

```
用户："384729乘以9283741"
  ↓
发给AI（带 tools 工具清单）
  ↓
AI回复：不是文字，是"调用请求"（tool_calls）
  ↓
你的Python真正执行计算
  ↓
把结果发回AI（role="tool"）
  ↓
AI组织最终回答
```

**AI 负责决策（用什么工具、传什么参数），你的代码负责执行。**

## ③ 工具 schema（说明书）

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",                    # 工具名
            "description": "计算两个数的乘积",      # AI靠它判断何时用
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"},
                },
                "required": ["a", "b"],            # ← 和 properties 平级！
            },
        },
    },
]
```

**⚠️ required 是 properties 的兄弟，不是儿子。** 写错 API 报 400 错。

description 是 AI 的"使用手册"，写得好 AI 才选得对。

## ④ 处理工具调用

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,               # 每次请求都要带！
)

if response.choices[0].message.tool_calls:
    # AI要干活
    messages.append(response.choices[0].message)   # 调用请求入库
    for tc in response.choices[0].message.tool_calls:   # 循环处理每一次调用
        name = tc.function.name                     # 工具名
        args = json.loads(tc.function.arguments)    # JSON文本→字典
        func = tool_functions[name]                 # 查分派表
        result = func(**args)                       # 拆包调用
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,                  # ID一一对应
            "content": str(result),                 # 必须字符串
        })
else:
    # AI直接回答了
    print(response.choices[0].message.content)
```

**铁律：AI 请求几次调用，就回几条 tool 消息，tool_call_id 一一对应。** 对不上 API 报 "insufficient tool messages"。

## ⑤ 分派表

```python
tool_functions = {
    "multiply": multiply,     # 不带括号！存的是函数本身
    "add": add,
    "write_file": write_file,
}
```

字典存函数本身（不带括号），用的时候才加括号调用。**AI 指哪打哪**。

## ⑥ Agent 循环（两层循环）

```python
while True:                     # 外层：对话循环（每轮一个问题）
    question = input()
    if question == "quit":
        break
    messages.append({"role": "user", "content": question})

    while True:                 # 内层：Agent循环（反复问AI直到完成）
        response = client.chat.completions.create(
            messages=messages, tools=tools,
        )
        if response.choices[0].message.tool_calls:
            # 执行工具，存结果，回到循环开头再问
            ...
        else:
            # 不要工具了 = 完成
            print(response.choices[0].message.content)
            messages.append({"role": "assistant", "content": ...})
            break
```

**有工具 → 需要 Agent 循环。没工具 → 一轮问答就完，别加循环。**

## ⑦ 工具函数的设计铁律

1. **返回字符串**（AI 唯一的眼睛，返回 None 会让 AI 懵）
2. **失败不崩溃**（返回错误文字，比如除零、"文件不存在"）
3. **消息准确具体**（"文件夹已创建"不是"文件已创建"——AI 靠消息做下一步决策）
4. **先门卫后干活**（early return 检查安全）

## ⑧ 沙盒安全

AI 不可信，工具必须有缰绳：

```python
SANDBOX = os.path.normpath("F:\\AI agent\\sandbox")

def check_safe(path):
    real = os.path.normpath(path)
    if not real.startswith(SANDBOX):
        return "拒绝：路径超出沙盒范围"
    return None
```

`os.path.normpath()` 把路径标准化（防止 `..` 绕出沙盒），`startswith` 检查前缀。

危险操作多道保险：删文件 → 沙盒检查 + 拒绝删文件夹 + 存在性检查。

## ⑨ 探针打印（调试基本功）

```python
if response.choices[0].message.tool_calls:
    print("[AI 要调用工具]")
    print(response.choices[0].message.tool_calls)   # 看AI到底要干什么
```

Agent 错了，看不到内部动作就不知道错在哪。真实项目里这叫 logging（日志）。

## ⑩ 判断力：操作需要 AI 决定吗？

- **需要**（AI 自己判断用什么工具）→ 做成工具 schema + 分派 + Agent 循环
- **不需要**（程序固定读某文件）→ 代码直接调函数，别绕道 AI

## ⑪ json 基础

- JSON = "把数据写成文本"的格式，长得像 Python 字典但是字符串
- `json.loads(文本)` → 字典（AI 给的一切都是文本，取用前先翻译）
- `json.dumps(字典)` → 文本
- 网络只能传文字，所以 AI 的参数是 JSON 文本
