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