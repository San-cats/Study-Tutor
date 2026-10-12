import sys
from main import answer,get_all_Tokens
from llm import client0

Judge_Tokens=0

TEST_SET=[
    ("3+5等于多少","exact","8"),
    ("你好","judge","回答礼貌友好即可"),
    ("什么是RAG","judge","要点:检索增强生成"),
    ("8-3等于多少","exact","5"),
    ("3*6等于多少，再帮我查一查什么是RAG","judge","要点:18和检索增强生成都要出现"),
]

def judge_exact(answer_text,standard):
    return standard in answer_text

def judge_by_llm(question,answer_text,standard):
    global Judge_Tokens
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":"你是阅卷老师，只输出'对'和‘错’,不要任何其他内容"},
            {"role":"user","content":f"标准答案要点:{standard} \n 学生回答:{answer_text} \n 学生回答是否覆盖了要点？"},
        ],
    )
    Judge_Tokens +=response.usage.total_tokens
    return response.choices[0].message.content

correct=0
for question,method,standard in TEST_SET:
    print(f"[题目]{question}")
    result=answer(question)
    print(f"[回答]{result[:80]}")
    if method=="exact":
        ok=judge_exact(result,standard)
    else:
        ok="对" in judge_by_llm(question,result,standard)
    print("√" if ok else "×")
    correct+=ok
    print(f"成绩单:{correct}/{len(TEST_SET)},准确率:{correct/len(TEST_SET)*100:.0f}%")
    print(f"本次测试消耗{get_all_Tokens()+Judge_Tokens} Tokens")
