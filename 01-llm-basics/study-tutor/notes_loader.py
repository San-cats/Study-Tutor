import os
import time
import chromadb
from llm import client1

NOTES_DIR="F:\\AI agent\\学习笔记"

def read_notes():  #读文件
    files=[]
    for filename in os.listdir(NOTES_DIR):
        if not filename.endswith(".md"):
            continue
        path=os.path.join(NOTES_DIR,filename)
        with open(path,"r",encoding="utf-8") as f:
            files.append((filename,f.read()))
    return files

def split_by_heading(text):  #以“#”来切片
    blocks=[]
    current=""
    for line in text.split("\n"):
        if line.strip().startswith("#"):
            if current:
                blocks.append(current)
            current=line+"\n"
        else:
            current +=line+"\n"
    blocks.append(current)
    return blocks  #返回blocks列表，每个索引是一个切片块

def embed(question):  #Ebedding
    response=client1.embeddings.create(
        model="BAAI/bge-m3",
        input=question,
    )
    return response.data[0].embedding

def embed_many(texts):
    response=client1.embeddings.create(
        model="BAAI/bge-m3",
        input=texts
    )
    return [d.embedding for d in response.data]

db=chromadb.PersistentClient(path="./chroma_notes")
collections=db.get_or_create_collection("study_notes",metadata={"hnsw:space":"cosine"})
if collections.count()==0:
    X=0
    All_times=0
    notes=[(name,content) for name, content in read_notes()]
    chunks = [(name, block) for name, full_text in notes for block in split_by_heading(full_text)]
    for i in range(0,len(chunks),16):
        start = time.time()
        batch=chunks[i:i+16]
        name_items=[items[0] for items in batch]
        text_items=[items[1] for items in batch]
        vec_items=embed_many(text_items)
        ids_items=[f"{name}:{i+offset}" for offset,name in enumerate(name_items)]
        meta_items=[{"source":name} for name in name_items]
        collections.add(
            ids=ids_items,
            documents=text_items,
            embeddings=vec_items,
            metadatas=meta_items
        )
        end=time.time()
        times=end-start
        All_times+=times
        X+=len(batch)
        print(f"已入库{X}/{len(chunks)}条，耗时{times:.2f}秒")
    print(f"已向量化入库{collections.count()}条,共耗时{All_times:.2f}秒")
else:
    print(f"集合已有{collections.count()}条，跳过向量化")

def retrieve(question):
    q_vec=embed(question)
    result=collections.query(
        query_embeddings=[q_vec],
        n_results=3,
    )
    result_list=[]
    for i in range(len(result["ids"][0])):
        distance=result["distances"][0][i]
        name=result["metadatas"][0][i]["source"]
        text=result["documents"][0][i]
        result_list.append((distance,name,text))
    return result_list

def build_prompt(question,results,right):
    lines=[f"-{name}:{text}" for _,name,text in results]
    context="\n".join(lines)
    return f"""
参考资料:{context}
用户提问:{question}
RIGHT:{right}
"""

def match_topic(topic):
    results=retrieve(topic)
    candidates=[]
    if results[0][0]<=0.48:
        print(f"已找到【{topic}】主题")
        return True,[]
    else:
        print(f"笔记里没有关于【{topic}】的主题")
        print(f"以下有3条候选，可能是你想问:")
        for idx,(distance,name,_) in enumerate(results[:3]):
            candidates.append((idx,distance,name))
        return False,candidates

if __name__=="__main__":
    ok,candidates=match_topic("量子力学")
    for idx, dist, name in candidates:
        print(f"{idx+1}:--{name}(距离{dist:.2f})")

