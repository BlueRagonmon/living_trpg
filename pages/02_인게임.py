import streamlit as st
import random
import math

st.set_page_config(page_title="TRPG 인생 플레이", layout="wide")

# =========================
# 로그인 검사 (최중요)
# =========================
if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# =========================
# 게임 초기화
# =========================
def init_game():
    base = {s: 3 for s in STATS}
    buff = random.choice(STATS)
    debuff = random.choice([s for s in STATS if s != buff])

    st.session_state.update({
        "buff": buff,
        "debuff": debuff,
        "current": base.copy(),
        "potential": base.copy(),
        "age": 1,
        "choice_count": 0
    })

if "current" not in st.session_state:
    init_game()

# =========================
# 선택지 로직
# =========================
AGE_POOLS = {
    "child": [
        ("뛰어논다", {"체력": 1, "민첩": 1}),
        ("블록 놀이", {"지능": 2}),
        ("친구와 논다", {"행운": 1}),
    ]
}

def generate_choices():
    pool = AGE_POOLS["child"]
    choices = []

    for text, effect in random.sample(pool, 3):
        choices.append({"text": text, "effect": effect})

    st.session_state.choices = choices

if "choices" not in st.session_state:
    generate_choices()

def apply_choice(idx):
    for stat, val in st.session_state.choices[idx]["effect"].items():
        mult = 1.5 if stat == st.session_state.buff else 0.5 if stat == st.session_state.debuff else 1
        st.session_state.current[stat] += math.floor(val * mult)

    generate_choices()

# =========================
# UI
# =========================
st.title("🎮 인생 플레이 중")

left, right = st.columns([3, 1])

with right:
    st.subheader(f"🧑 {st.session_state.nickname}")
    st.write(f"🎁 재능: {st.session_state.buff} +50% / {st.session_state.debuff} -50%")

    st.markdown("### 📊 스탯")
    for s, v in st.session_state.current.items():
        tag = " (+50%)" if s == st.session_state.buff else " (-50%)" if s == st.session_state.debuff else ""
        st.write(f"{s}: {v}{tag}")

    if st.button("로그아웃"):
        st.session_state.clear()
        st.switch_page("app.py")

with left:
    st.markdown("### 선택지")
    for i, c in enumerate(st.session_state.choices):
        label = c["text"] + " ➜ " + ", ".join([f"{k} +{v}" for k, v in c["effect"].items()])
        if st.button(label, key=i):
            apply_choice(i)
            st.rerun()
