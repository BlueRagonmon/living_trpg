import streamlit as st
import random
import math

st.set_page_config(page_title="TRPG 인생 시뮬레이터", layout="wide")

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# -------------------------
# 게임 초기화
# -------------------------
def init_game(nickname):
    base = {s: 3 for s in STATS}

    buff = random.choice(STATS)
    debuff = random.choice([s for s in STATS if s != buff])

    base[buff] = math.floor(base[buff] * 1.5)
    base[debuff] = max(1, math.floor(base[debuff] * 0.5))

    st.session_state.nickname = nickname
    st.session_state.buff = buff
    st.session_state.debuff = debuff

    st.session_state.current = base.copy()
    st.session_state.potential = base.copy()
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
        ("운동을 한다", {"체력": 2}),
        ("공부를 한다", {"지능": 2}),
        ("산책을 한다", {"민첩": 1}),
        ("친구와 논다", {"행운": 1}),
        ("힘든 일을 한다", {"근력": 2}),
    ]

    for text, effect in random.sample(free_pool, 3):
        choices.append({
            "text": text,
            "effect": effect
        })

    for _ in range(2):
        stat = random.choice(STATS)
        max_possible = potential[stat]
        req = random.randint(max(1, max_possible - 2), max_possible)

        choices.append({
            "text": f"{stat} 시험에 도전한다",
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

    # potential 갱신
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

# 시작 화면
if "current" not in st.session_state:
    nickname = st.text_input("닉네임을 입력하세요")

    if st.button("게임 시작") and nickname:
        init_game(nickname)
        generate_choices()
        st.rerun()

# 게임 화면
else:
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader(f"🧑 닉네임: {st.session_state.nickname}")
        st.write(f"🎁 재능: **{st.session_state.buff} 강화 / {st.session_state.debuff} 약화**")
        st.subheader(f"🎂 나이: {st.session_state.age}살")
        st.markdown("### 📊 스탯")
        for s, v in st.session_state.current.items():
            st.write(f"{s}: {v}")

    with col1:
        st.markdown("### 선택지")
        for i, c in enumerate(st.session_state.choices):
            label = c["text"]

            # 효과 표시
            effect_text = ", ".join(
                [f"{k} +{v}" for k, v in c["effect"].items()]
            )
            label += f"  ➜  ({effect_text})"

            disabled = False
            if "require" in c:
                stat = list(c["require"].keys())[0]
                need = c["require"][stat]
                label += f" [필요 {stat} ≥ {need}]"

                if st.session_state.current[stat] < need:
                    disabled = True

            if st.button(label, key=i, disabled=disabled):
                apply_choice(i)
                st.rerun()
