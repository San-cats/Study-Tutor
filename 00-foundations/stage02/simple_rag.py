import os
from dotenv import load_dotenv
from openai import OpenAI

KNOWLEDGE_DIR="F:\\AI agent\\sandbox\\knowledge"
STOPWORDS=set("的我了是的地得你在吗什么怎么一个这那和")

load_dotenv("F:\\AI agent\\.env")
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def load_chunks():  #分片
    chunks=[]
    for filename in os.listdir(KNOWLEDGE_DIR):
        if not filename.endswith(".txt"):
            continue
        path=os.path.join(KNOWLEDGE_DIR,filename)
        with open(path,"r",encoding="utf-8") as f:
            content=f.read()
        for line in content.split("\n"):
            line=line.strip()
            if line:
                chunks.append((filename,line))
    return chunks

def retrieve(question,chunks,top_k=3):  #召回+索引
    q_chars=[c for c in question if c not in STOPWORDS]
    scored=[]
    for name,text in chunks:  #索引
        score=0
        for c in q_chars:
            if c in text:
                score+=1
        scored.append((score,name,text))  #得分，文件名，内容
    scored.sort(key=lambda x:x[0],reverse=True)
    return scored[:top_k]

def build_prompt(question,results):  #生成
    lines=[f"-{name}:{text}"for _,name,text in results] #忽略分数，输出示例:  文件1：ABC
    context="\n".join(lines) #将lines列表里每个元素通过\n拼接，最终是一个完整字符串
    return f"""
    参考资料:{context}
    用户提问:{question}
    请根据参考资料回答。如果资料中没有相关信息，就说"资料中没有相关信息"，不要编造。"""

def main():
    chunk=load_chunks()
    print(f"已加载 {len(chunk)}条知识")
    print("输入问题开始，quit结束对话")
    while 1:
        question=input()
        if question=="quit":
            break
        results=retrieve(question,chunk) #向量知识库：已将每个切片和用户问题进行相似度计算
        prompt=build_prompt(question,results)
        response=client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role":"system","content":"你是问答知识库，只根据参考资料回答"},
                {"role":"user","content":prompt},
            ]
        )
        print(response.choices[0].message.content)
if __name__ == "__main__":
    main()
