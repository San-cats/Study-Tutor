# Python 核心语法笔记

## ① print vs return（最重要）

- `print()` = 显示给人看，函数"交出去"的是 None
- `return` = 把值交出去，可以赋值、传参、继续加工

```python
def add(a, b):
    print(a + b)        # 屏幕显示8，但 result 是 None

def add2(a, b):
    return a + b        # 屏幕无显示，但 result 是 8
```

**函数 = 加工厂：参数进（原料），return 出（产品）。print 只是车间墙上的显示器。**
工具函数的返回值是 AI 唯一的眼睛——return 文字给 AI 看，不是 print 给人看。

## ② f-string 格式化

```python
name = "小明"
print(f"{name} likes this")    # 小明 likes this
```

花括号里放变量，直接插入字符串。

## ③ 四种容器

| 类型 | 样子 | 特点 |
|------|------|------|
| 字符串 str | `"文字"` | 不可变 |
| 列表 list | `[1, 2, 3]` | 有序，可改 |
| 元组 tuple | `(1, 2)` | 有序，不可改 |
| 字典 dict | `{"key": "value"}` | 键值对，查表用 |

元组拆包：`for name, text in chunks:` 一次拆开两个值。

## ④ strip vs split

- `strip()` = **剥**掉两头空白 → 返回**字符串**
- `split()` = **劈**成列表 → 返回**列表**

```python
"  今天学了RAG  ".strip()    # "今天学了RAG"
"a b c".split()              # ['a', 'b', 'c']
```

## ⑤ join 拼接

```python
", ".join(["a", "b", "c"])   # "a, b, c"
"\n".join(files)             # 每个文件名一行
```

## ⑥ 列表推导式

```python
[x * 2 for x in [1, 2, 3]]              # [2, 4, 6]
[int(x) for x in ["1", "9", "3"]]       # [1, 9, 3]（字符串转数字）
[c for c in text if c not in "的了"]    # 带过滤条件
```

## ⑦ 字典安全取值

```python
d = {"a": 1}
d["b"]            # KeyError 崩溃！
d.get("b", 0)     # 0（没有就返回默认值，安全）
```

## ⑧ lambda 匿名函数

`scored.sort(key=lambda x: x[0], reverse=True)` 的意思：

- `scored` 是 `(score, name, text)` 元组的列表
- `key=lambda x: x[0]` — 按每个元组第0个元素（score）排序
- `reverse=True` — 从高到低

lambda 是一次性小函数：输入 x，返回 x[0]。

## ⑨ `**args` 拆包（工具分派核心）

```python
args = {"path": "F:\\x", "content": "你好"}
write_file(**args)
# 等价于 write_file(path="F:\\x", content="你好")
```

字典的键变成参数名，值变成参数值。**工具 schema 的参数名必须和函数参数名一致**，拆包才能对上。

## ⑩ 提前返回（early return）

```python
def delete_file(path):
    if 超出沙盒:
        return "拒绝"        # 门卫1
    if 是文件夹:
        return "拒绝"        # 门卫2
    if 不存在:
        return "错误"        # 门卫3
    os.remove(path)          # 全过关，才干活
    return "已删除"
```

检查放前面，不合格立刻 return，干活代码保持平坦。

## ⑪ with 语句读文件

```python
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
```

- `"r"` 读 / `"w"` 写
- `encoding="utf-8"` 必须有，否则中文乱码
- with 自动关文件

## ⑫ `if __name__ == "__main__":`

直接运行文件时执行里面的代码；被 import 时不执行。测试代码放这里。

## ⑬ for...else 的陷阱

```python
for x in items:
    ...
else:
    # 循环没有 break 时，else 永远会执行！
```

else 挂在 for 上，不是 if 上！缩进对齐决定了 else 属于谁。

## ⑭ 其他习惯

- 变量名别叫 `list`、`str` 等（遮蔽内置函数）
- `while True` 比 `while 1` 更标准
- set 的 in 判断比 list 快：`c not in STOPWORDS`
- 字符串比较是字典序，"10" < "9"，数字比较要先 int()
