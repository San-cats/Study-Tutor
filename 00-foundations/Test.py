# 写一个函数，统计一个字符串里有多少个元音字母(a e i o u)
# 例如：count_vowels("hello world") 返回 3

import os
KNOWLEDGE_DIR="F:\\AI agent\\sandbox\\knowledge"
def count_vowels(text):
    res=0
    for char in text:
        if char in "aeiou":
            res+=1
    return res

# 写一个函数，接收 "1 9 3 4 -5" 这样的字符串，返回 "9 -5"（最大和最小）
# 提示：.split() 可以把字符串按空格切成列表
def high_and_low(numbers):
    nums=[int(x) for x in numbers.split()]
    return f"{max(nums)} {min(nums)}"

# 写一个函数，把字符串里所有元音字母删掉
# 例如：disemvowel("This website is for losers!") 返回 "Ths wbst s fr lsrs!"
def disemvowel(text):
    num=[]
    for char in text:
        if char.lower() in "aeiou":
            continue
        else:
            num.append(char)
    return "".join(num)

# 写一个函数，接收名字列表，返回点赞文案：
# []                        → "no one likes this"
# ["小明"]                  → "小明 likes this"
# ["小明","小红"]           → "小明 and 小红 like this"
# ["小明","小红","小刚"]     → "小明, 小红 and 小刚 like this"
# 4个人以上                 → "小明, 小红 and 2 others like this"
def likes(names):
    if len(names)==0:
        return "no one likes this"
    elif len(names)==1:
        return f"{names[0]} likes this"
    elif len(names)==2:
        return f"{names[0]} and {names[1]} like this"
    elif len(names)==3:
        return f"{names[0]}, {names[1]} and {names[2]} like this"
    else:
        return f"{names[0]}, {names[1]} and 2 others like this"

# 写一个函数，把字符串里每个字符替换成 "(" 或 ")"：
# 出现一次的字符 → "("，出现多次的字符 → ")"
# 例如：duplicate_encode("din")      → "((("
#       duplicate_encode("recede")   → "()()()"
# 提示：先用字典统计每个字符出现次数
def duplicate_encode(word):
    num={chr(i): 0 for i in range(97,123)}
    res=[]
    for char in word:
        if char.lower() in num:
            num[char.lower()]+=1
    for char in word:
        if num[char.lower()]==1:
            res.append("(")
        else:
            res.append(")")
    return "".join(res)

def load_chunks():  #分片
    chunks=[]
    for filename in os.listdir(KNOWLEDGE_DIR):
        if not filename.endswith(".txt"):
            continue
        path=os.path.join(KNOWLEDGE_DIR,filename)
        with open(path,"r",encoding="utf-8") as f:
            content=f.read()
            chunks.append(content)
    return chunks
"""
print(duplicate_encode("din"))      # (((
print(duplicate_encode("recede"))   # ()()()
print(duplicate_encode("Success"))  # )())())  注意大小写不同算不同字符
"""

def try_1():
    explain={"explain":[{"【可取之处】":"...","【不足漏洞】":"...","【知识点温习】":"...","【修改引导】":"..."}]}
    return explain

if __name__=="__main__":
    for k,v in try_1()["explain"][0].items():
        print(k)
        print(v)