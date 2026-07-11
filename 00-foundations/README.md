# Stage 0：基础环境搭建

> 目标：让电脑具备开发 AI Agent 的基本环境

## 学什么

1. 命令行基础（PowerShell）
2. Python 虚拟环境
3. Git 基本操作
4. 获取 API Key

---

## 一、PowerShell 基础

PowerShell 是 Windows 的命令行工具，你会在这里敲代码。

### 打开方式

- 搜素框输入 `powershell` → 回车
- 或者在文件夹里按住 Shift + 右键 → "在此处打开 PowerShell 窗口"

### 基本命令

```powershell
# 查看当前位置
Get-Location        # 缩写: pwd

# 查看当前目录的文件
Get-ChildItem       # 缩写: ls 或 dir

# 进入某个文件夹
cd 文件夹名字

# 返回上一级
cd ..

# 创建文件夹
New-Item -ItemType Directory 文件夹名    # 缩写: mkdir 文件夹名

# 运行 Python 脚本
python 文件名.py

# 清屏
Clear-Host          # 缩写: cls
```

---

## 二、Python 虚拟环境

虚拟环境让每个项目有独立的 Python 包，不会互相干扰。

### 创建虚拟环境

在项目根目录打开 PowerShell，运行：

```powershell
cd "F:\AI agent"
python -m venv venv
```

### 激活虚拟环境

```powershell
.\venv\Scripts\Activate.ps1
```

激活成功后，命令行前面会出现 `(venv)` 标记。

### 退出虚拟环境

```powershell
deactivate
```

---

## 三、Git 基础

Git 是代码版本管理工具。

### 配置你的身份（只需做一次）

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

### 常用操作

```powershell
# 把当前文件夹变成 Git 仓库
git init

# 查看改了哪些文件
git status

# 把所有改动暂存
git add .

# 提交（保存一个版本）
git commit -m "描述这次改了什么"

# 查看提交历史
git log --oneline
```

---

## 四、安装 Python 依赖包

先激活虚拟环境，然后装这些后续会用的包：

```powershell
.\venv\Scripts\Activate.ps1
pip install openai python-dotenv httpx
```

- **openai**: 调用 OpenAI API（也兼容很多国产模型）
- **python-dotenv**: 管理 API Key，不让密钥泄露到代码里
- **httpx**: 发 HTTP 请求

---

## 五、获取 API Key

AI Agent 需要一个"大脑"，也就是大语言模型（LLM）。你需要一个 API Key 才能调用它。

### 推荐渠道（选一个就行）

| 平台 | 获取地址 | 免费额度 | 适合 |
|------|---------|---------|------|
| DeepSeek | platform.deepseek.com | 送额度 | ⭐ 首选，便宜好用 |
| 阿里百炼 | dashscope.aliyun.com | 送额度 | 国内稳定 |
| OpenAI | platform.openai.com | 需绑卡 | 原版 GPT |
| Anthropic | console.anthropic.com | 需绑卡 | Claude |

**推荐你注册 DeepSeek**：国内注册方便，价格低，中文效果好，兼容 OpenAI SDK。

### 如何保存 API Key

1. 在项目根目录创建 `.env` 文件：

```powershell
cd "F:\AI agent"
New-Item -ItemType File .env
```

2. 用记事本打开 `.env`，写入（替换成你自己的 key）：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

3. 代码里这样读取：

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
```

---

## 六、验证环境

运行下面的测试脚本，确认一切就绪：

```powershell
cd "F:\AI agent\00-foundations"
python check_env.py
```

---

## 你现在要做的事

按顺序来：

1. ✅ Git 已安装 → 配置 `git config --global user.name` 和 `user.email`
2. 创建 Python 虚拟环境
3. 安装依赖包
4. 注册 DeepSeek 获取 API Key
5. 创建 `.env` 文件保存 Key
6. 运行 `check_env.py` 验证

做完一步告诉我，有问题随时问。
