# RAG 知识库

## ① RAG 是什么

**R**etrieval-**A**ugmented **G**eneration（检索增强生成）

开卷考试比喻：提问前先把小抄（相关资料）递到 AI 眼前。

```
资料 → 切块 → 存储
提问 → 检索（找相关块） → 拼接（塞进提示词） → 生成（AI照着答）
```

为什么必须切块：AI 上下文有长度限制，资料塞不下，也没必要全塞。

## ② 切块

按行切（每条事实一行）：

```python
for line in content.split("\n"):
    line = line.strip()
    if line:
        chunks.append((filename, line))   # (文件名, 内容) 元组
```

## ③ 关键词检索（简化版）

1. 问题拆字符，过滤停用词
2. 给每块打分：块里包含多少个问题字符
3. 排序取前 top_k 条

```python
STOPWORDS = set("的我了是的地得你在吗什么怎么一个这那和")

def retrieve(question, chunks, top_k=3):
    q_chars = [c for c in question if c not in STOPWORDS]
    scored = []
    for name, text in chunks:
        score = sum(1 for c in q_chars if c in text)
        scored.append((score, name, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
```

**局限：只认字，不认意思。** "有啥新知识入库"和"今日的学习内容是RAG"一字不重合，得 0 分。

## ④ 向量检索（升级版）

**万物皆向量**：文字 → 一串数字，意思相近 → 数字相近。

```
"猫"   → [2.1, 3.5]
"狗"   → [2.3, 3.2]     ← 挨得近
"汽车" → [8.9, 1.2]     ← 离得远
```

"意思相近"变成数学题："坐标相近"。找离问题坐标最近的笔记块。

## ⑤ 余弦相似度

量两个向量**方向的夹角**：

```
cosine(A, B) = 点积 / (A的长度 × B的长度)
```

- 结果 -1 到 1，1 = 最相似，0 = 无关
- 只看方向不看长度："猫猫猫猫"和"猫"方向一样，cosine 是 1

手写版：

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))       # 点积
    len_a = sum(x * x for x in a) ** 0.5         # 勾股定理求长
    len_b = sum(x * x for x in b) ** 0.5
    if len_a == 0 or len_b == 0:
        return 0
    return dot / (len_a * len_b)
```

## ⑥ 字符向量（Bag of Words 简化）

```python
def make_vocab(chunks):
    vocab = set()
    for name, text in chunks:
        vocab.update(text)
    return sorted(vocab)

def text_to_vector(text, vocab):
    return [text.count(c) for c in vocab]   # 每个词表字符出现几次
```

## ⑦ 提示词拼接

```python
def build_prompt(question, results):
    lines = [f"- {name}: {text}" for _, name, text in results]
    context = "\n".join(lines)
    return f"""参考资料：
{context}

用户问题：{question}

请根据参考资料回答。如果资料中没有相关信息，就说"资料中没有相关信息"，不要编造。"""
```

**RAG 最重要的质量指标：宁可说不知道，不许编造。**

## ⑧ 还没学的（下一步）

- 真正的 embedding：神经网络学出的向量，同义词天生挨得近（字符向量做不到）
- 向量数据库：存几百万向量的专用数据库
