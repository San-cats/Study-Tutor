import os

SANDBOX = os.path.normpath("F:\\AI agent\\sandbox")   # 沙盒根目录

def check_safe(path):
    """检查路径是否在沙盒内。安全返回None，危险返回错误字符串"""
    real = os.path.normpath(path)  #**规范化路径字符串**，清理路径里多余的 `.`、`..`、多余的 `/` 或 `\`，返回简化后的路径
    if not real.startswith(SANDBOX):
        return "拒绝：路径超出沙盒范围"
    return None   # None 表示安全

def list_files(path):
    # 1. 先安全检查
    # 2. 如果文件不存在，返回提示
    # 3. os.listdir 列出来，用换行符 \n 拼成一个字符串返回
    # 你的代码：
    if check_safe(path):
        return "拒绝：路径超出沙盒范围"
    else:
        if os.path.exists(path):
            files=os.listdir(path)
            return "\n".join(files)
        else:
            return "错误！路径不存在"

def create_folder(path):
    # 1. 安全检查
    # 2. os.makedirs(path, exist_ok=True)
    # 3. 返回 "已创建：路径"
    # 你的代码：
    if check_safe(path):
        return "拒绝：路径超出沙盒范围"
    else:
        os.makedirs(path,exist_ok=True)
        return "文件夹已创建:"+path

def write_file(path, content):
    # 1. 安全检查
    # 2. open(path, "w", encoding="utf-8") 写入
    # 3. 返回 "已写入：路径"
    # 你的代码：
    if check_safe(path):
        return "拒绝：路径超出沙盒范围"
    else:
        with open(path,"w",encoding="utf-8") as f:
            f.write(content)
            return "文件已写入："+path

def read_file(path):
    # 1. 安全检查
    # 2. 不存在 → 返回错误
    # 3. open(path, "r", encoding="utf-8") 读内容
    # 4. 返回文件内容
    if check_safe(path):
        return "拒绝：路径超出沙盒范围"
    else:
        if not os.path.exists(path):
            return "错误！文件不存在"
        else:
            with open(path,"r",encoding="utf-8") as f:
                content=f.read()
                return content
def delete_file(path):
    # 保险1：安全检查（沙盒）
    # 保险2：只删文件，不删文件夹
    #       提示：os.path.isdir(path) 判断是不是文件夹，是 → 拒绝
    # 保险3：文件不存在 → 返回提示，不报错
    # 执行：os.remove(path)
    # 返回："已删除：path"
    if check_safe(path):
        return "拒绝：路径超出沙盒范围"
    else:
        if os.path.isdir(path):
            return "只能删除文件，不可删除文件夹"
        else:
            if not os.path.exists(path):
                return "错误！文件不存在"
            else:
                os.remove(path)
                return "已删除：" + path
# 测试代码
if __name__ == "__main__":
    print(list_files("F:\\AI agent\\sandbox"))          # 沙盒还不存在，应该报错
    print(create_folder("F:\\AI agent\\sandbox"))       # 创建沙盒
    print(list_files("F:\\AI agent\\sandbox"))          # 空文件夹，输出空
    print(write_file("F:\\AI agent\\sandbox\\笔记.txt", "你好，AI助手"))
    print(list_files("F:\\AI agent\\sandbox"))          # 应该看到 笔记.txt
    print(list_files("C:\\Windows"))                    # 应该被拒绝
