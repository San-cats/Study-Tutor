import chromadb
from llm import client0
from embedding_rag import embed,load_chunks,build_prompt

db=chromadb.PersistentClient(path="./chroma_data")
collection=db.get_or_create_collection("knowledge",metadata={"hnsw:space":"cosine"})

if collection.count()==0:
    chunks=load_chunks()
    for idx,(name,text) in enumerate(chunks):
        vec=embed(text)
        collection.add(
            ids=[f"{name}:{idx}"],
            documents=[text],
            embeddings=[vec],
            metadatas=[{"file":name}]
        )
    print(f"已向量化入库{collection.count()}条")
else:
    print(f"集合已有{collection.count()}条，跳过向量化")

def main():
    while 1:
        question = input()
        if question == "quit":
            break
        q_vec=embed(question)
        result=collection.query(
            query_embeddings=[q_vec],
            n_results=3
        )
        result_list=[]
        for i in range(len(result["ids"][0])):
            distance=result["distances"][0][i]
            name=result["metadatas"][0][i]["file"]
            text=result["documents"][0][i]
            result_list.append((distance,name,text))
            print(f"相似度距离:{distance:.4f}|文件:{name}|文本:{text}")
        prompt=build_prompt(question,result_list)
        response=client0.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role":"system","content":"你是问答知识库，根据参考资料回答"},
                {"role":"user","content":prompt},
            ]
        )
        print(response.choices[0].message.content)
if __name__=="__main__":
    main()


