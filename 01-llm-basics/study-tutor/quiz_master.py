import json
from llm import client0
from notes_loader import retrieve,build_prompt
from File_operations import load_ledger

QUIZ_SYSTEM="""你是出题专家，根据知识库提出问题
【要点】
1.只根据参考资料出题，禁止编造资料里没有的内容
2.出3道简答题
3.只输出JSON格式:{"Examination":[{"question":"...","answer":"..."},*3]}
4.如果资料库没有该主题，Examination输出空列表
5.出题前检查【RIGHT】列表，不得出与其中任何一道语义相近或高度相似的题
6.如果资料中能出的新题不足3道，允许少出。若一道都输出不了，输出{"Examination":[]}
7.禁止输出 markdown 代码块标记
"""

Quiz_Tokens=0
RIGHT=[]
def get_Quiz_Tokens():
    return Quiz_Tokens

def quiz_master(topic):
    #已经出过并做对的题目
    RIGHT.clear()
    data=load_ledger("mastery.json")
    for item in data:
        if item.get("topic")==topic:
            for idx,q in enumerate(item["results"]):
                if q=="对":
                    RIGHT.append(item["Examination"][idx]["question"])
    #向量化
    global Quiz_Tokens
    results=retrieve(topic)
    prompt=build_prompt(topic,results,RIGHT)
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"system","content":QUIZ_SYSTEM}]+[{"role":"user","content":prompt}]
    )
    Quiz_Tokens+=response.usage.total_tokens
    try:
        data = json.loads(response.choices[0].message.content)
        Quiz=data.get("Examination")
        if not isinstance(Quiz,list):
            print(f"【警告】出题专家输出结构异常")
            return []
        return Quiz
    except Exception:
        print(f"【警告】出题专家出题解析失败")
        return []

if __name__=="__main__":
    pass