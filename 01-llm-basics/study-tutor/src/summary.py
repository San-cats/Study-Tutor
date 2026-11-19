import json
from concurrent.futures import ThreadPoolExecutor
from llm import client0

SYSTEM="""你是一个关键词抽取助手。你的任务是根据用户提供的一段文本切片，总结出 1 个或几个最能代表其核心内容的关键词。
【要求】
1. 关键词必须是能独立表达主题的词或名词性短语，不要输出句子、解释、标点或编号。
2. 优先使用原文中出现的词或短语；如果原文没有合适表达，可以用最简洁的通用词概括，但不要编造事实。
3. 关键词数量根据切片内容决定：默认 1-3 个；内容明显包含多个并列主题时最多 5 个；不要为了凑数量输出弱相关词。
4. 按重要性从高到低排序，第一个是最核心关键词。
5. 去除重复、近义重复和过于宽泛的词，例如“内容”“问题”“情况”“相关”等，除非它们确实是核心主题。
6. 保留专有名词、产品名、人名、机构名、技术名等关键实体；不要把实体和泛化主题混为一谈。
7. 如果切片过短、噪声大或无法判断主题，输出空数组。
8. 输入是什么语言，关键词就用什么语言；中文输入输出中文关键词，英文输入输出英文关键词。
9. 禁止输出Markdown格式，也不要输出任何额外说明
10.只输出 JSON，不要任何解释：{"Summary": ["关键字1", "关键字2", "关键字3"]}
"""

def refine_topics_parallel(texts, max_workers=8):
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(refine_topic, texts))

def refine_topic(data):
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"system","content":SYSTEM}] +\
                 [{"role":"user","content":data}],
    )
    try:
        data=json.loads(response.choices[0].message.content)
        if isinstance(data,dict) and isinstance(data.get("Summary"), list):
            return {"Summary": data["Summary"]}
    except Exception:
        pass
    return {"Summary":["【错误】！未分类"]}

if __name__=="__main__":
    pass