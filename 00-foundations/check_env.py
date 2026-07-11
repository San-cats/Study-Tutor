# -*- coding: utf-8 -*-
"""
环境检查脚本
运行: python check_env.py
检查你的开发环境是否准备就绪
"""

import sys
import os

# 强制 stdout 用 UTF-8, 解决中文 Windows 控制台乱码
sys.stdout.reconfigure(encoding='utf-8')

def check_python():
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 10:
        print("  [OK] Python 版本满足要求 (>= 3.10)")
        return True
    else:
        print("  [FAIL] Python 版本过低, 请安装 Python 3.10+")
        return False

def check_packages():
    packages = ["openai", "dotenv", "httpx"]
    all_ok = True
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"  [OK] {pkg} 已安装")
        except ImportError:
            print(f"  [FAIL] {pkg} 未安装 -- 运行: pip install {pkg}")
            all_ok = False
    return all_ok

def check_api_key():
    from dotenv import load_dotenv

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(project_root, ".env")

    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        load_dotenv()

    key = os.getenv("DEEPSEEK_API_KEY")
    if key and key.startswith("sk-"):
        masked = key[:8] + "..." + key[-4:]
        print(f"  [OK] DeepSeek API Key 已配置: {masked}")
        return True
    else:
        print("  [WARN] DeepSeek API Key 未配置")
        print("     在项目根目录创建 .env 文件, 写入:")
        print("     DEEPSEEK_API_KEY=sk-你的密钥")
        return False

def check_git():
    import subprocess
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"  [OK] Git 已安装: {result.stdout.strip()}")
            return True
    except Exception:
        pass
    print("  [FAIL] Git 未安装")
    return False

def main():
    print("=" * 50)
    print("AI Agent 学习环境检查")
    print("=" * 50)

    print("\n>> Python 环境:")
    py_ok = check_python()

    print("\n>> 依赖包:")
    pkg_ok = check_packages()

    print("\n>> Git:")
    git_ok = check_git()

    print("\n>> API Key:")
    key_ok = check_api_key()

    print("\n" + "=" * 50)
    results = [py_ok, pkg_ok, git_ok, key_ok]
    passed = sum(results)
    total = len(results)
    print(f"结果: {passed}/{total} 项通过")

    if passed == total:
        print("\n环境完全就绪, 可以开始 Stage 1 了!")
    elif key_ok and py_ok:
        print("\n基础环境没问题, 安装缺失的包即可开始")
    else:
        print("\n请先完成上面的检查项, 再进入下一阶段")

    print("=" * 50)

if __name__ == "__main__":
    main()
