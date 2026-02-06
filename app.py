import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os, json, random, re

# ---------------- SETUP ----------------

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Smart Exam", layout="centered")
st.title("🧠 AI Smart Exam System")

# ---------------- SAFE JSON ----------------

def safe_json(text):
    text = text.replace("```json","").replace("```","").strip()
    m = re.search(r"\[.*\]", text, re.S)
    if m:
        return json.loads(m.group())
    raise ValueError("Invalid JSON")

# ---------------- SIMPLE EXPLANATION FALLBACK ----------------

def fallback_explanation(q, ans):
    p = f"Explain simply in 2 lines:\nQuestion:{q}\nAnswer:{ans}"
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":p}],
        temperature=0
    )
    return r.choices[0].message.content.strip()

# ---------------- USER INPUT ----------------

topic = st.text_input("Topic")
exam = st.text_input("Exam Type")
level = st.selectbox("Difficulty",["Easy","Medium","Hard"])
count = st.number_input("Questions",1,10,5)

# ---------------- GENERATE ----------------

if st.button("Generate Test"):

    prompt = f"""
Create {count} MCQ questions on {topic} for {exam} at {level} level.

Return ONLY JSON ARRAY.

[
 {{
  "id":1,
  "question":"text",
  "options":["real option","real option","real option","real option"],
  "answer":"one of options",
  "topic":"{topic}"
 }}
]

RULES:
- NEVER use A,B,C,D
- options must be REAL values
- answer MUST match option
- options must be different
"""

    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    questions = safe_json(r.choices[0].message.content)

    for q in questions:
        random.shuffle(q["options"])

    st.session_state.questions = questions
    st.session_state.answers = {}

# ---------------- TEST UI ----------------

if "questions" in st.session_state:

    st.subheader("📝 Attend Test")

    for q in st.session_state.questions:

        st.markdown(f"### Q{q['id']}. {q['question']}")

        opts = ["--Select--"] + q["options"]

        ans = st.radio("Answer", opts, key=q["id"])

        st.session_state.answers[q["id"]] = None if ans=="--Select--" else ans

# ---------------- SUBMIT ----------------

if st.button("Submit Test") and "questions" in st.session_state:

    if None in st.session_state.answers.values():
        st.error("Answer all questions")
        st.stop()

    score = 0
    weak = []

    # explanation batch
    ep = f"""
ONLY JSON ARRAY:

[
{{"id":1,"explanation":"simple"}}
]

Questions:
{st.session_state.questions}
"""

    er = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":ep}],
        temperature=0
    )

    try:
        explanations = safe_json(er.choices[0].message.content)
    except:
        explanations = []

    st.divider()
    st.subheader("📊 Result")

    for q in st.session_state.questions:

        ua = st.session_state.answers[q["id"]]
        ca = q["answer"]

        correct = ua == ca

        if correct:
            score += 1
        else:
            weak.append(q["topic"])

        exp = ""

        for e in explanations:
            if isinstance(e,dict) and e.get("id")==q["id"]:
                exp = e.get("explanation","")

        if not exp:
            exp = fallback_explanation(q["question"],ca)

        st.markdown(f"### Q{q['id']}")
        st.write("Your Answer:",ua)
        st.write("Correct Answer:",ca)

        if correct:
            st.success("Correct ✅")
        else:
            st.error("Wrong ❌")

        st.info("Explanation")
        st.write(exp)

    st.divider()
    st.success(f"Final Score: {score}/{len(st.session_state.questions)}")

    if weak:
        st.warning("📌 Focus Areas:")
        for i in set(weak):
            st.write("•",i)
    else:
        st.success("Excellent! 🎉")
