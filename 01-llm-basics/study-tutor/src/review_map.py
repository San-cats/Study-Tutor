from File_operations import load_ledger
from config import MASTERY_FILE,MISTAKE_FILE
    #排列
def display_width(s):
    return sum(2 if ord(ch) > 127 else 1 for ch in s)

def pad(s,width):
    diff=width-display_width(s)
    if diff<=0:
        return s
    left=diff//2
    right=diff-left
    return " "*left+s+" "*right

    #地图
def show_map():
    data=load_ledger(MASTERY_FILE)
    mistake=load_ledger(MISTAKE_FILE)
    learn_map=[]
    if data:
        learn_map.append("【复习地图】")
        learn_map.append(f"{pad('主题', 14)}{pad('场次', 14)}{pad('最近得分', 14)}{pad('掌握度', 14)}{pad('错题欠账', 14)}")
        for theme in data:
            debt=0
            session=len(theme["score"])
            last_score=theme['score'][-1]
            starts="★" * theme["score"][-1] + "☆" * (3 - theme["score"][-1])
            for item in mistake:
                if theme["topic"]==item["topic"]:
                    debt=len(item["Examination"])
                    break
            learn_map.append(f"{pad(theme['topic'], 14)}{pad(str(session), 12)}{pad(f'{str(last_score)}/3', 14)}{pad(starts, 14)}{pad(str(debt), 14)}")
    else:
        learn_map.append("还没有考试记录哦！先去考一场")
    return learn_map

if __name__=="__main__":
    for i in show_map():
        print(i)