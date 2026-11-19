import os,sys
import streamlit as st
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from notes_loader import match_topic
from quiz_master import quiz_master
from grader import Judge
from File_operations import load_ledger,save_ledger,append_topic,take_mistakes,drop_mistakes
from config import MASTERY_FILE,MISTAKE_FILE
from review_map import show_map
from explainer_expert import explain_master
import pandas as pd

#run "F:\AI agent\01-llm-basics\study-tutor\ui\app.py"

STATE_KEYS = {
    "exam":   ["Test_paper", "Test_answer", "submitted",
               "exam_results", "score", "exam_topic"],
    "review": ["Mistake_paper", "review_results", "review_active",
               "review_submitted", "review_score", "review_topic"],
    "map":    ["map_active"],
}

def clear_groups(*names):
    for name in names:
        for k in STATE_KEYS[name]:
            st.session_state.pop(k, None)

def clear_view(keep):
    clear_groups(*[g for g in STATE_KEYS if g != keep])

def quiz(idx, question, key_prefix="ans_"):
    st.markdown(f"**第{idx + 1}题**:{question}")
    st.text_area(
        "你的答案",
        key=f"{key_prefix}{idx}"
    )

def _normalize_comment(comment):
    if not comment:
        return []
    if isinstance(comment, str):
        return [{"点评": comment}]
    if isinstance(comment, dict):
        if "explain" in comment:
            return _normalize_comment(comment["explain"])
        return [comment]
    if isinstance(comment, list):
        return [c if isinstance(c, dict) else {"点评": str(c)} for c in comment]
    return [{"点评": str(comment)}]


def grade_paper(paper,answers):
    exam_results = []
    score = 0
    for idx, item in enumerate(paper):
        ans = answers[idx] if idx < len(answers) else ""
        result = Judge(item["question"], item["answer"], ans)
        is_correct = result["result"] == "对"
        if is_correct:
            score += 1
            comment = _normalize_comment(result.get("comment"))
        else:
            comment = _normalize_comment(
                explain_master(item["question"], item["answer"], ans, result["result"])
            )
        exam_results.append({
            "question": item["question"],
            "answer": ans,
            "result": result["result"],
            "comment": comment,
            "is_correct": is_correct,
        })
    return exam_results, score

st.title("学习管家🧑‍🏫")

topic=st.text_input("请输入主题")
col1, col2 ,col3= st.columns(3)
with col1:
    exam_button=st.button("开始考试")
with col2:
    review_button=st.button("我要复习")
with col3:
    map_button = st.button("复习地图")

if exam_button:
    if topic=="":
        st.warning("请输入主题")
    else:
        ok, candidates = match_topic(topic)
        if not ok:
            st.warning(f"笔记中没有【{topic}】主题  \n您可能想找:")
            data = [{"题号": idx + 1, "距离": f"{distance:.2f}", "文件": filename, "关键字": tag} for
                    idx, distance, filename, tag in candidates]
            for u in data:
                with st.container(border=True):
                    st.write(f"题号：{u['题号']}")
                    st.write(f"距离：{u['距离']}")
                    st.write(f"关键字：{u['关键字']}")
                    st.write(f"文件：{u['文件']}")
        else:
            clear_groups("exam")
            st.session_state.exam_topic = topic
            with st.spinner(f"已找到【{topic}】主题,正在出题中..."):
                st.session_state.Test_paper = quiz_master(topic)
            st.session_state.Test_answer = []

if "Test_paper" in st.session_state:
    if not st.session_state.get("submitted", False):
        for idx, item in enumerate(st.session_state["Test_paper"]):
            quiz(idx,item["question"])
        if st.button("交卷"):
            paper = st.session_state["Test_paper"]
            answers = [st.session_state.get(f"ans_{i}", "") for i in range(len(paper))]
            st.session_state["Test_answer"] = answers

            with st.spinner("正在评分并生成评语..."):
                exam_results, score = grade_paper(paper, answers)
            data = load_ledger(MASTERY_FILE)
            mistake = load_ledger(MISTAKE_FILE)
            exam_topic = st.session_state.exam_topic
            for idx, item in enumerate(paper):
                data = append_topic(data, exam_topic, "Examination", item)
                data = append_topic(data, exam_topic, "answer", answers[idx])
                data = append_topic(data, exam_topic, "results", exam_results[idx]["result"])
                if not exam_results[idx]["is_correct"]:
                    mistake = append_topic(mistake, exam_topic, "Examination", item)

            data = append_topic(data, exam_topic, "score", score)
            save_ledger(data, MASTERY_FILE)
            save_ledger(mistake, MISTAKE_FILE)

            st.session_state.exam_results=exam_results
            st.session_state.score=score
            st.session_state.submitted = True
            st.rerun()
    else:
        paper=st.session_state["Test_answer"]
        st.success(
            f"本次【{st.session_state.exam_topic}】考试得分:"
            f"{st.session_state.score}/{len(paper)}"
        )
        for idx,item in enumerate(st.session_state.exam_results):
            st.markdown(f"**题目 {idx + 1}：** {item['question']}")
            st.markdown("**学生答案：**")
            with st.container(border=True):
                st.markdown(item["answer"] if item["answer"].strip() else "_未作答_")
            st.markdown(f"**评语：**{'✅' if item['result'] == '对' else '❌'}")
            with st.container(border=True):
                for key in item["comment"][0]:
                    st.markdown(f"{key}:{item['comment'][0][key]}")
        if st.button("重新开始"):
            clear_groups("exam")
            st.rerun()

if review_button:
    if topic == "":
        st.warning("请输入主题")
    else:
        mistake = load_ledger(MISTAKE_FILE)
        papers = take_mistakes(mistake, topic, n=3)
        if not papers:
            st.warning(f"错题本中没有【{topic}】的错题哦，快去考一场试吧")
        else:
            clear_view("review")
            st.session_state.Mistake_paper = papers
            st.session_state.review_topic = topic
            st.session_state.review_active = True
            st.session_state.review_submitted = False
            st.rerun()

if st.session_state.get("review_active", False):
    review_topic = st.session_state.review_topic

    if not st.session_state.review_submitted:
        # --- 作答 ---
        for idx, exam in enumerate(st.session_state.Mistake_paper):
            quiz(idx, exam["question"], key_prefix="review_ans_")

        if st.button("交卷", key="review_submit"):
            paper = st.session_state.Mistake_paper
            answers = [
                st.session_state.get(f"review_ans_{i}", "")
                for i in range(len(paper))
            ]

            with st.spinner("正在评分并生成评语..."):
                review_results, score = grade_paper(paper, answers)

            mistake = load_ledger(MISTAKE_FILE)
            for idx, item in enumerate(paper):
                if review_results[idx]["is_correct"]:
                    mistake = drop_mistakes(mistake, review_topic, item["question"])
            save_ledger(mistake, MISTAKE_FILE)

            st.session_state.review_results = review_results
            st.session_state.review_score = score
            st.session_state.review_submitted = True
            st.rerun()
    else:
        # --- 交卷 ---
        paper = st.session_state.Mistake_paper
        st.success(
            f"本次【{review_topic}】复习得分："
            f"{st.session_state.review_score}/{len(paper)}"
        )
        for idx, item in enumerate(st.session_state.review_results):
            st.markdown(f"**题目 {idx + 1}：** {item['question']}")
            st.markdown("**学生答案：**")
            with st.container(border=True):
                st.markdown(item["answer"] if item["answer"].strip() else "_未作答_")
            st.markdown(f"**评语：** {'✅' if item['result'] == '对' else '❌'}")
            with st.container(border=True):
                if not item["comment"]:
                    st.markdown("_无评语_")
                else:
                    for block in item["comment"]:
                        for key, value in block.items():
                            st.markdown(f"**{key}**：{value}")

        if st.button("继续复习"):
            clear_groups("review")
            st.rerun()

if map_button:
    clear_view("map")  # ← 清掉 exam / review
    st.session_state.map_active = True
    st.rerun()

if st.session_state.get("map_active", False):
    data = show_map()
    if "没有考试记录" in data[0]:
        st.info(data[0])
    else:
        rows = [row.strip().split() for row in data]
        header = rows[1]
        body = rows[2:]
        df = pd.DataFrame(body, columns=header)
        st.dataframe(df, hide_index=True, use_container_width=True)

    if st.button("返回", key="map_back"):
        st.session_state.map_active = False
        st.rerun()









