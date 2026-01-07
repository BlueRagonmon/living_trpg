import streamlit as st
import random

st.set_page_config(page_title="TRPG 인생 시뮬레이터", layout="centered")

# =========================
# 세션 초기화
# =========================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 이미 로그인된 경우 인게임으로 이동
if st.session_state.logged_in:
    st.switch_page("pages/02_game.py")

st.title("🎲 TRPG 인생 시뮬레이터")
st.subheader("로그인")

tab_login, tab_register, tab_guest = st.tabs(["로그인", "회원가입", "게스트"])

# -------------------------
# 로그인
# -------------------------
with tab_login:
    uid = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if uid in st.session_state.users and st.session_state.users[uid]["pw"] == pw:
            st.session_state.logged_in = True
            st.session_state.login_type = "member"
            st.session_state.nickname = st.session_state.users[uid]["nickname"]
            st.switch_page("pages/2_🎮_인게임.py")
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

# -------------------------
# 회원가입
# -------------------------
with tab_register:
    uid = st.text_input("아이디", key="reg_id")
    pw = st.text_input("비밀번호", type="password", key="reg_pw")
    nick = st.text_input("닉네임", key="reg_nick")

    if st.button("회원가입"):
        if uid in st.session_state.users:
            st.error("이미 존재하는 아이디입니다.")
        elif nick in [u["nickname"] for u in st.session_state.users.values()]:
            st.error("이미 사용 중인 닉네임입니다.")
        elif not uid or not pw or not nick:
            st.error("모든 항목을 입력하세요.")
        else:
            st.session_state.users[uid] = {"pw": pw, "nickname": nick}
            st.success("회원가입 완료! 로그인해주세요.")

# -------------------------
# 게스트
# -------------------------
with tab_guest:
    nick = st.text_input("게스트 닉네임")

    if st.button("바로 시작"):
        if nick in [u["nickname"] for u in st.session_state.users.values()]:
            st.error("이미 사용 중인 닉네임입니다.")
        elif not nick:
            st.error("닉네임을 입력하세요.")
        else:
            st.session_state.logged_in = True
            st.session_state.login_type = "guest"
            st.session_state.nickname = nick
            st.switch_page("pages/2_🎮_인게임.py")
