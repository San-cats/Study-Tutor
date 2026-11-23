# AI Agent 开发学习仓库

从零开始的 AI Agent 开发学习总仓库。旗舰项目是 **[学习管家 Study-Tutor](01-llm-basics/study-tutor/README.md)**——基于个人学习笔记的 AI 私教。

**参考路线**: [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)

## 仓库结构

```
00-foundations/            # 基础环境与热身练习(环境搭建、API 初体验)
01-llm-basics/study-tutor/ # ★ 旗舰项目:学习管家(见项目 README)
sandbox/                   # 沙盒实验代码
学习笔记/                  # 配套学习笔记 10 篇(语法/API/工具/RAG/踩坑/提示词/多Agent/SSH/安全/项目实战)
```

## 旗舰项目:学习管家 Study-Tutor

基于自身学习笔记的 AI 私教——自动出题、三态判分、错题复盘、讲解教学、掌握度记忆,并提供 CLI 与 streamlit 网页双界面。

- **技术栈**: 自研 RAG(ChromaDB + bge-m3 向量化)、多 Agent(出题/判分/讲解三专家)、JSON 账本记忆、回归测试三件套、streamlit 前端
- **完整文档**: [01-llm-basics/study-tutor/README.md](01-llm-basics/study-tutor/README.md)
- **快速开始**: 克隆后 `cd 01-llm-basics/study-tutor`,配置 `.env`(DeepSeek + SiliconFlow 双 Key),然后:

```bash
streamlit run ui/app.py        # 网页版(推荐)
python src/main.py             # CLI 黑窗口版
```

## 学习轨迹

路线图 8 阶段已全部完成(基础环境 → API 调用 → 提示词工程 → 工具调用 → 记忆与 RAG → 向量数据库 → 多 Agent → 安全与评估),学习过程与踩坑沉淀在 [学习笔记/](学习笔记/) 中——每篇笔记都是一段真实学费。
