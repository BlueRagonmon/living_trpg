import streamlit as st
import random

st.set_page_config(page_title="TRPG 인생 시뮬레이터", layout="wide")

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# -------------------------
# 게임 초기화
# -------------------------
def init_game():
    st.session_state.current = {s: 3 for s in STATS}
    st.session_state.potential = st.session_state.current.copy()
    st.session_state.age = 1
    st.session_state.choice_count = 0
    st.session_state.choices = []

# -------------------------
# 선택지 생성
# -------------------------
def generate_choices():
    current = st.session_state.current
    potential = st.session_state.potential

    choices = []

    free_pool = [
        {"text": "운동을 한다", "effect": {"체력": 2}},
        {"text": "공부를 한다", "effect": {"지능": 2}},
        {"text": "산책을 한다", "effect": {"민첩": 1}},
        {"text": "친구와 논다", "effect": {"행운": 1}},
        {"text": "힘든 일을 한다", "effect": {"근력": 2}},
    ]

    choices.extend(random.sample(free_pool, 3))

    for _ in range(2):
        stat = random.choice(STATS)
        max_possible = st.session_state.potential[stat]
        req = random.randint(max(1, max_possible - 2), max_possible)

        choices.append({
            "text": f"{stat} 시험에 도전한다 (필요 {stat} ≥ {req})",
            "require": {stat: req},
            "effect": {stat: 2}
        })

    st.session_state.choices = choices

# -------------------------
# 선택 처리
# -------------------------
def apply_choice(index):
    choice = st.session_state.choices[index]

    for stat, val in choice["effect"].items():
        st.session_state.current[stat] += val

    # potential 갱신 (선택하지 않은 선택지도 반영)
    for c in st.session_state.choices:
        for stat, val in c["effect"].items():
            possible = st.session_state.current[stat] + val
            st.session_state.potential[stat] = max(
                st.session_state.potential[stat],
                possible
            )

    st.session_state.choice_count += 1
    if st.session_state.choice_count % 5 == 0:
        st.session_state.age += 1

    generate_choices()

# -------------------------
# UI
# -------------------------
st.title("🎲 TRPG 인생 시뮬레이터")

if "current" not in st.session_state:
    if st.button("게임 시작"):
        init_game()
        generate_choices()
else:
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader(f"🧓 나이: {st.session_state.age}살")
        st.markdown("### 📊 스탯")
        for s, v in st.session_state.current.items():
            st.write(f"{s}: {v}")

    with col1:
        st.markdown("### 선택지")
        for i, c in enumerate(st.session_state.choices):
            disabled = False
            label = c["text"]

            if "require" in c:
                stat = list(c["require"].keys())[0]
                if st.session_state.current[stat] < c["require"][stat]:
                    disabled = True
                    label += " ❌"

            if st.button(label, key=i, disabled=disabled):
                apply_choice(i)
                st.experimental_rerun()
