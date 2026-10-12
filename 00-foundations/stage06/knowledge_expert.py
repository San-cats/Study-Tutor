from llm import client0
from embedding_rag import load_chunks,retrieve,build_prompt,embed

KNOW_HISTORY=[]
KNOW_SYSTEM="你是知识专家，根据参考资料回答"
Knowledge_Tokens=0

chunks = load_chunks()
print(f"已加载 {len(chunks)}条知识")
chunk_vectors = [(name, text, embed(text)) for name, text in chunks]
print("全部向量化已完成！")

def get_knowledge_Tokens():
    return Knowledge_Tokens

def knowledge_expert_agent(task):
    global Knowledge_Tokens
    KNOW_HISTORY.append({"role":"user","content":task})
    results=retrieve(task,chunk_vectors)
    prompt=build_prompt(task,results)
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"system","content":KNOW_SYSTEM}]+KNOW_HISTORY+[{"role": "user", "content": prompt}]
    )
    Knowledge_Tokens +=response.usage.total_tokens
    KNOW_HISTORY.append({"role":"assistant","content":response.choices[0].message.content})
    return response.choices[0].message.content