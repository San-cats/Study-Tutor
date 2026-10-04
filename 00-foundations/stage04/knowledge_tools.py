from llm import client0
from embedding_rag import load_chunks,retrieve,build_prompt,embed
from conversation import HISTORY

CHUNKS=load_chunks()
CHUNK_VECTORS=[(name,text,embed(text)) for name,text in CHUNKS]

def handle_knowledge(text):
    results=retrieve(text,CHUNK_VECTORS)
    prompt=build_prompt(text,results)
    messages = [
                   {"role": "system", "content": "你是问答知识库，优先根据参考资料回答。若参考资料中未提及，不禁止其他来源"},
               ] + HISTORY + [
                   {"role": "user", "content": prompt},
               ]
    response = client0.chat.completions.create(model="deepseek-chat", messages=messages)
    answers = response.choices[0].message.content
    HISTORY.append({"role": "user", "content": text})
    HISTORY.append({"role": "assistant", "content": answers})
    return answers