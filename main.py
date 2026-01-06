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

    st.session_state.nickname = nickname
    st.session_state.buff = buff
    st.session_state.debuff = debuff

    st.session_state.current = base.copy()
    st.session_state.potential = base.copy()
    st.session_state.age = 1
    st.session_state.choice_count = 0
    st.session_state.choices = []

# -------------------------
# 나이별 선택지 풀
# -------------------------
AGE_POOLS = {
    "child": [
        ("뛰어논다", {"체력": 1, "민첩": 1}),
        ("블록 놀이", {"지능": 2}),
        ("친구와 논다", {"행운": 1}),
    ],
    "kid": [
        ("체육 수업", {"체력": 2}),
        ("독서 습관", {"지능": 2}),
        ("운동 연습", {"근력": 1}),
    ],
    "teen": [
        ("시험 공부", {"지능": 3}),
        ("경쟁에 도전", {"근력": 2}),
        ("동아리 활동", {"민첩": 2}),
    ],
    "adult": [
        ("야근", {"체력": -1, "근력": 2}),
        ("자기계발", {"지능": 2}),
        ("인맥 관리", {"행운": 2}),
    ]
}

def get_age_pool(age):
    if age <= 5:
        return AGE_POOLS["child"]
    elif age <= 12:
        return AGE_POOLS["kid"]
    elif age <= 18:
        return AGE_POOLS["teen"]
    else:
        return AGE_POOLS["adult"]

# -------------------------
# 선택지 생성
# -------------------------
def generate_choices():
    pool = get_age_pool(st.session_state.age)
    current = st.session_state.current
    potential = st.session_state.potential

    choices = []

    # 조건 없는 선택지 3개
    for text, effect in random.sample(pool, min(3, len(pool))):
        choices.append({
            "text": text,
            "effect": effect
        })

    # 조건 있는 선택지 2개
    for _ in range(2):
        stat = random.choice(STATS)
        max_possible = potential[stat]
        req = random.randint(max(1, max_possible - 2), max_possible)

        choices.append({
            "text": f"{stat} 도전",
            "require": {stat: req},
            "effect": {stat: 2}
        })

    st.session_state.choices = choices

# -------------------------
# 선택 적용
# -------------------------
def apply_choice(index):
    choice = st.session_state.choices[index]

    for stat, val in choice["effect"].items():
        multiplier = 1.0
        if stat == st.session_state.buff:
            multiplier = 1.5
        elif stat == st.session_state.debuff:
            multiplier = 0.5

        applied = math.floor(val * multiplier)
        st.session_state.current[stat] += applied

        st.session_state.potential[stat] = max(
            st.session_state.potential[stat],
            st.session_state.current[stat]
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
    nickname = st.text_input("닉네임을 입력하세요")

    if st.button("게임 시작") and nickname:
        init_game(nickname)
        generate_choices()
        st.rerun()

else:
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader(f"🧑 {st.session_state.nickname}")
        st.write(f"🎁 재능: **{st.session_state.buff} +50% / {st.se_**
