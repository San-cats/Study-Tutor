import json
from llm import client0

EXP_SYSTEM="""你是私教老师，根据参考答案评价学生答案的不足和错误，引导学生进行查漏补缺和巩固知识点进行讲解和改正
【要点】
1.首先肯定学生答对的方面。再对照参考答案找出学生回答的不足，说明问题，进行针对性的温习并补充对应知识点
2.只输出JSON格式:{explain:[{"【可取之处】":"...","【不足漏洞】":"...","【知识点温习】":"...","【修改引导】":"..."}]},
4.不足漏洞可分为:概念错误(知识点本身理解错)，要点遗漏(参考答案里有、学生没写到的得分点)，逻辑漏洞(推导链条跳步、因果颠倒、论证不成立)，
审题偏差(看错题干要求、答非所问、范围跑偏)和表述问题(术语不规范、模糊、缺少关键限定条件)
2.学生答案全对时，给予肯定并复盘知识点，只输出{explain:[{"【可取之处】":"...","【知识点温习】":"..."}]}
5.禁止输出markdown代码块
"""
Explainer_Token=0
def get_Explainer_Token():
    return Explainer_Token

def explain_master(question,ref_answer,user_answer,results):
    global Explainer_Token
    content=(
        f"题目:{question}\n"
        f"参考答案:{ref_answer}\n"
        f"学生答案:{user_answer}\n"
        f"答题正误:{results}"
    )
    response=client0.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"system","content":EXP_SYSTEM}]+\
        [{"role":"user","content":content}]
    )
    Explainer_Token+=response.usage.total_tokens
    try:
        data=json.loads(response.choices[0].message.content)
        if isinstance(data,dict) and "explain" in data:
            return data
        else:
            return {"explain": [{"【讲解】": "本次讲评解析失败,请重新拉起讲解专家"}]}
    except Exception:
        return {"explain": [{"【讲解】": "本次讲评解析失败,请重新拉起讲解专家"}]}
