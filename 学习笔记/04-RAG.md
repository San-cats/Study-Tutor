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

## ⑧ 真 embedding（2026-09-21 已学 ✅）

**字符向量看长相，embedding 看用法。**

embedding 也是一个函数（文字 → 1024 个数字），但这个函数不是人写的规则，是神经网络在几十亿句话里**训练**出来的。"嵌入"和"embedding"总出现在相同语境，它们的向量就被拉得很近——不用查字表，天生知道是一回事。

**调用方式**（SiliconFlow，OpenAI 兼容，和聊天调用是孪生兄弟）：

```python
sf = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url="https://api.siliconflow.cn/v1")

def embed(text):
    response = sf.embeddings.create(model="BAAI/bge-m3", input=text)
    return response.data[0].embedding    # 1024 个数字
```

**实战结果**（同一道题，只换引擎，框架一行没动）：

| 版本 | "解释一下嵌入" 检索得分 |
|------|------------------------|
| 字符向量 | 0.00 全盲 |
| embedding | 0.58 第一名 ✅ |

**缓存**：启动时把全部资料块 embed 一次（9 次 API），之后每个问题只 embed 1 次。API 调用是网络请求，比本地计算慢千百倍——"词表只算一次"的升级版。

**两个判断**：
1. embedding 模型没有大脑（不会思考、不用工具）——它是**工具不是 Agent**，所以这仍是单 Agent 架构
2. embedding 的相似度是"语义温度"：短句子都挤在一片语义区，分差小（0.58 vs 0.55），噪音块混进 top3 很正常——所以 top_k 取 3 让 AI 自己挑，而不是只取第 1 名

## ⑨ 还没学的（下一步）

- 重排序 / 相似度阈值：把噪音块挡在提示词外面
- 语义切块：按意思切块，不是按行

## ⑩ 向量数据库（2026-10-04 已学 ✅）

**为什么**：内存列表三宗罪——每次启动重新 embed（烧钱）、全塞内存（装不下）、for 循环逐个比 O(N)（慢）。向量数据库一次解决：**持久化、索引、增删查**。

**本质 = 持久化**：向量躺在磁盘文件夹里，程序关了还在。集合 = **模糊字典**：向量是钥匙（key），原文是答案（value），查询就是"找意思最近的钥匙"。

**选型**：ChromaDB（纯 Python、持久化+索引都内置）→ 入门首选；FAISS 只管索引不管存储；Milvus 要 Docker 太重。

**概念链（每一级返回值都要接住）**：

```python
db = chromadb.PersistentClient(path="./chroma_data")      # 开库房门
collection = db.get_or_create_collection("knowledge",     # 拿/建集合
    metadata={"hnsw:space": "cosine"})
collection.add(...) / collection.query(...) / collection.count()
```

- **get_or_create 名字即答案**：先 get，找到旧集合就用旧的——所以重启后集合还在
- `hnsw:space: cosine`：和手写 cosine 同一标准，但**距离 = 1 − 相似度，越小越好**（方向反了！0.25 是好成绩）
- 入库三件套：ids（门牌号，唯一）、documents（原文）、embeddings（向量）+ metadatas（来源文件名）

**首次入库开关（幂等）**：

```python
if collection.count() == 0:    # 空盒子 = 从没入过库
    逐条 embed + add           # 唯一花钱的一步
else:
    跳过向量化                  # 启动两次 = 启动一次的效果
```

**实战数据**（两次运行对比）：

| | 第一次（删库从零） | 第二次（重启） |
|---|---|---|
| 启动 | 已向量化入库9条，4.1秒 | 跳过向量化，2.6秒 |
| 检索 | 距离 0.2488 / 0.2819 / 0.4455 | **分毫不差** |

**坑**：Chroma 返回的是字典套列表，build_prompt 要的是三元组列表——中间加**适配器**（收集循环）。适配器第三次见面：chat_view 过滤 / model_dump / 收集循环。

**git**：chroma_data/ 进 .gitignore——数据库文件夹是**可再生数据**（随时能重新 embed 出来），和 __pycache__ 同类，不进仓库。

**HNSW 索引**（知道即可）：把向量建成"高速公路网"，查询走近路，不逐个比。O(N) → O(log N)。

## ⑪ 还没学的（下一步）

- 重排序 / 相似度阈值
- 语义切块
- 多 Agent 协作
- 评估与监控
