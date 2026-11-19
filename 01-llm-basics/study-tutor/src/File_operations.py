import os
import json

def load_ledger(path):#文件不存在→{}；读 JSON→dict；文件损坏 try/except→{}
    if not os.path.exists(path):
        return []
    try:
        with open(path,'r',encoding='utf-8') as f:
            data=json.load(f)
        return data
    except (json.JSONDecodeError,IOError):
        return []

def save_ledger(data,files):
    with open(files,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def append_topic(data,topic,field,value):
    for theme in data: #theme:大字典，列表中的一个元素
        if theme.get("topic")==topic:
            theme.setdefault(field, []).extend(value if isinstance(value, (list, tuple)) else [value])
            return data
    new_theme = {"topic": topic}
    new_theme[field] = value if isinstance(value, (list, tuple)) else [value]
    data.append(new_theme)
    return data

    #错题
def take_mistakes(data,topic,n=2):
    for theme in data:
        if theme.get("topic")==topic:
            return theme["Examination"][:n]
    return []

def drop_mistakes(data,topic,question):
    for item in data:
        if item.get("topic")==topic:
            item["Examination"]=[
                q for q in item.get("Examination",[])
                if q.get("question") !=question
            ]
            break
    return data