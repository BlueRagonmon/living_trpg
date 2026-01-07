import streamlit as st
import random
import math

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="🎮 인생 TRPG - 인게임",
    layout="wide"
)

# =========================
# 로그인 확인 (가장 중요)
# =========================
if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

# =========================
# 기본 설정
# =========================
STATS = ["체력", "근력", "지능", "민첩", "행운"]

# =========================
# 게임 초기화
# =========================
def init_game():
    base_stats = {s: 3 for s in STATS}
    buff = random.choice(STATS)
    debuff = random.choice([s for s in STATS if s != buff])

    st.session_state.update({
        "stats": base_stats,
        "buff": buff,
        "debuff": debuff,
        "age": 1,
        "choice_count": 0,
        "choices": []
    })

if "stats" not in st.session_state:
    init_game()

# =========================
# 선택지 생성
# =========================
CHOICE_POOL = [
    ("밖에서 논다", {"체력": 1, "민첩": 1}),
    ("책을 읽는다", {"지능": 2}),
    ("친구와 놀다", {"행운": 1}),
    ("힘든 일을 한다", {"근력": 2}),
    ("휴식을 취한다", {"체력": 2}),
]

def generate_choices():
    st.session_state.choices = random.sample(CHOICE_POOL, 3)

if not st.session_state.choices:
    generate_choices()

# =========================
# 선택지 적용
# =========================
def apply_choice(idx):
    _, effects = st.session_state.choices[idx]

    for stat, value in effects.items():
        multiplier = 1.0
        if stat == st.session_state.buff:
            multiplier = 1.5
        elif stat == st.session_state.debuff:
            multiplier = 0.5

        st.session_state.stats[stat] += math.floor(value * multiplier)

    st.session_state.choice_count += 1

    if st.session_state.choice_count % 5 == 0:
        st.session_state.age += 1

    generate_choices()
    st.rerun()

# =========================
# 사이드바 (유저 정보)
# =========================
with st.sidebar:
    st.header("👤 플레이어 정보")
    st.write(f"**닉네임:** {st.session_state.nickname}")
    st.write(f"**나이:** {st.session_state.age}세")

    st.markdown("---")
    st.subheader("🎁 재능")

    st.write(f"강화: **{st.session_state.buff} (+50%)**")
    st.write(f"약화: **{st.session_state.debuff} (-50%)**")

    st.markdown("---")
    st.subheader("📊 스탯")

    for s, v in st.session_state.stats.items():
        tag = ""
        if s == st.session_state.buff:
            tag = " ▲"
        elif s == st.session_state.debuff:
            tag = " ▼"
        st.write(f"{s}: {v}{tag}")

    st.markdown("---")
    if st.button("로그아웃"):
        st.session_state.clear()
        st.switch_page("app.py")

# =========================
# 메인 화면
# =========================
st.title("🎮 인생 TRPG")

st.subheader("당신의 선택은?")

for i, (text, effects) in enumerate(st.session_state.choices):
    effect_text = ", ".join([f"{k} +{v}" for k, v in effects.items()])
    if st.button(f"{text} ({effect_text})", key=i):
        apply_choice(i)
