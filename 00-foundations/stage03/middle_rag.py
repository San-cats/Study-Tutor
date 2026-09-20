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

def load_chunks():
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

def retrieve(question,chunks,vocab,top_k=3):
    q_text="".join(c for c in question if c not in STOPWORDS)
    q_vec=text_to_vector(q_text,vocab)
    scored=[]
    for name,text in chunks:
        v=text_to_vector(text,vocab)
        sim=cosine(q_vec,v)
        scored.append((sim,name,text))
    scored.sort(key=lambda x:x[0],reverse=True)
    return scored[:top_k]

def build_prompt(question,results):
    lines=[f"-{name}:{text}"for _,name,text in results]
    context="\n".join(lines)
    return f"""
参考资料:{context}
用户提问:{question}
请根据参考资料回答。如果资料中没有相关信息，就说"资料中没有相关信息"，不要编造。"""

def make_vocab(chunks):
    vocab=set()
    for name,text in chunks:
        for c in text:
            vocab.add(c)
    return sorted(vocab)

def text_to_vector(text,vocab):
    filtered = "".join(c for c in text if c not in STOPWORDS)
    return [filtered.count(c) for c in vocab]

def cosine(a,b):
    dot=sum(x * y for x,y in zip(a,b))
    len_a=sum(x * x for x in a)**0.5
    len_b=sum(x * x for x in b)**0.5
    if len_a==0 or len_b==0:
        return 0
    return dot/(len_a * len_b)

def main():
    chunk=load_chunks()
    vocab=make_vocab(chunk)
    print(f"已加载 {len(chunk)}条知识")
    print("输入问题开始，quit结束对话")
    while 1:
        question=input()
        if question=="quit":
            break
        results=retrieve(question,chunk,vocab)
        print(f"[检索到{len(results)}块]")
        for sim,name,text in results:
            print(f" 相似度{sim:.2f} | {name} | {text}")
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
