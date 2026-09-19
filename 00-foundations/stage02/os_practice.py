import os

files=os.listdir("/")
"""
print("F盘AI agent文件夹里有：")
for f in files:
    print(" ",f)
"""
#print("ven这个文件夹存在吗？",os.path.exists("F:\\AI agent"))
"""
os.makedirs("F:\\AI agent\\测试文件夹",exist_ok=True)
print("已成功创建文件夹")
"""
print("F:\\AI agent\\00-foundations文件夹里有什么")
for f in os.listdir("/00-foundations"):
    print(" ",f)