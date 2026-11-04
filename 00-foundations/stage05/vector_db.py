import chromadb
from llm import client0
from embedding_rag import embed,load_chunks,build_prompt

db=chromadb.PersistentClient(path="./chroma_data")  #持久化，向量库数据**保存到硬盘文件夹 `./chroma_data`**，程序重启之后，知识库还在
collection=db.get_or_create_collection("knowledge",metadata={"hnsw:space":"cosine"})
#先去数据库查找名字叫 `"knowledge"` 的集合；如果存在：直接取出这个集合；如果不存在：自动新建一个名叫 knowledge 的集合
#- `hnsw`：Chroma 默认的向量索引算法（HNSW）；`hnsw:space`：指定**向量之间距离计算方式**
if collection.count()==0:
    chunks=load_chunks()
    for idx,(name,text) in enumerate(chunks):
        vec=embed(text)
        collection.add(
            ids=[f"{name}:{idx}"],  #文件名:序号
            documents=[text],  #原始分片文本，召回成功后取出拼接 prompt
            embeddings=[vec],  #文本对应的语义向量
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
        result=collection.query(  #召回
            query_embeddings=[q_vec],
            n_results=3
        )
        result_list=[]
        for i in range(len(result["ids"][0])):  #召回的数据打包成元组放入result_list
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


