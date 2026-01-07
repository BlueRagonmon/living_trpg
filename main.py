import streamlit as st
import random
import math

st.set_page_config(page_title="TRPG 인생 시뮬레이터", layout="wide")

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# -------------------------
# 세션 초기화
# -------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # 회원 계정 저장

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

    st.session_sta_
