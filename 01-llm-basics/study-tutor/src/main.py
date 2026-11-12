import time
from quiz_master import quiz_master
from grader import Judge
from File_operations import load_ledger,save_ledger
from explainer_expert import explain_master
from notes_loader import match_topic
from review_map import show_map
from config import MASTERY_FILE,MISTAKE_FILE

FIELDS = ["Examination", "answer", "results", "score"]
Examination_paper = {"topic": "", "Examination": [], "answer": [], "results": [],  "score": []}
Mistake_Note={"topic": "", "Examination": [],"history":[]}

    #账本
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

    #考试
def start_quiz(topic):
    Exam=quiz_master(topic)
    if not Exam:
        print("笔记里没有这个主题")
        return None
    else:
        Examination_paper["Examination"].extend(Exam)
        print("考试开始，共3道题")
        return Exam #包含新试题

def ask_one(question,ref_answer): # 一题一问一判
    user_answer = input("【回答】:\n")
    Examination_paper["answer"].append(user_answer)
    result=Judge(question,ref_answer,user_answer)
    Examination_paper["results"].append(result["result"])
    result["history"]=user_answer
    return result

if __name__=="__main__":
    score = 0
    data = load_ledger(MASTERY_FILE)
    mistake = load_ledger(MISTAKE_FILE)

    topic = input("请输入本次考试的主题:\n")
    print(f"----------正在查询资料库----------")
    has_topic,candidates=match_topic(topic)
    if not has_topic:
        print(f"笔记里没有关于【{topic}】的主题")
        print(f"以下有3条候选，可能是你想问:")
        for idx, dist, name in candidates:
            print(f"{idx+1}:--{name}(距离{dist:.2f})")
    else:
        print(f"已找到【{topic}】主题")
        time.sleep(1)
        Examination_paper["topic"] = topic
        Mistake_Note["topic"] = topic

        mistake_exam = take_mistakes(mistake, topic)  # mistake:[{question:...,answer:...},{question:...,answer:...}]
        if mistake_exam:
            print("-----" * 3, "温故而知新", "-----" * 3)
            Examination_paper["Examination"].extend(mistake_exam)
            for item in mistake_exam:
                print(f"【错题再现】:\n{item['question']}")
                result = ask_one(item["question"], item["answer"])
                print(f"【评阅】:\n你的答案是:{result['result']}的,\n{result['comment']}")
                if result["result"] == "对":
                    mistake = drop_mistakes(mistake, topic, item["question"])
                else:
                    mistake = append_topic(mistake, topic, "Examination", Mistake_Note[FIELDS[0]])
            save_ledger(mistake, MISTAKE_FILE)

        Test = start_quiz(topic)  # Exam:[{question:...,answer:...},...]
        if Test:
            print("----------正在拉起【出题专家】Agent----------")
            time.sleep(1)
            for item in Test:
                print(f"【问题】:\n{item['question']}")
                result = ask_one(item["question"], item["answer"])
                if result["result"] == "对":
                    score += 1
                else:
                    Mistake_Note["Examination"].append(item)
                print(f"【评阅】:\n你的答案是:{result['result']}的,\n{result['comment']}")
                print("--" * 20)
            Examination_paper["score"].append(score)
            for key in FIELDS:
                data = append_topic(data, topic, key, Examination_paper[key])
            save_ledger(data, MASTERY_FILE)
            if Mistake_Note["Examination"]:
                mistake = append_topic(mistake, topic, "Examination", Mistake_Note["Examination"])
                save_ledger(mistake, MISTAKE_FILE)
            print(f"最终得分{score}/{len(Test)}")
            Tech = int(input("是否拉起【讲解专家】Agent?\n"))
            if Tech:
                time.sleep(1)
                print("----------正在拉起【讲解专家】Agent----------")
                time.sleep(1)
                for i, (exam, ans, res) in enumerate(zip(
                        Examination_paper["Examination"],
                        Examination_paper["answer"],
                        Examination_paper["results"])):
                    explain = explain_master(exam["question"], exam["answer"], ans, res)
                    print(f"【讲评】:\n第{i+1}题:{exam['question']}")
                    for k, v in explain["explain"][0].items():
                        print(k)
                        print(v)
                    print("--" * 20)
            Map=int(input("是否拉起【复习地图】?\n"))
            if Map:
                time.sleep(1)
                print("----------正在拉起【复习地图】----------")
                time.sleep(1)
                show_map()



