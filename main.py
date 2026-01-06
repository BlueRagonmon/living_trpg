from flask import Flask, session, jsonify, request
import random

app = Flask(__name__)
app.secret_key = "trpg-life-secret"

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# -------------------------
# 게임 초기화
# -------------------------
def init_game():
    current = {s: 3 for s in STATS}
    potential = current.copy()

    session.clear()
    session["current"] = current
    session["potential"] = potential
    session["age"] = 1
    session["choice_count"] = 0
    session["last_choices"] = []

# -------------------------
# 선택지 생성
# -------------------------
def generate_choices(current, potential):
    choices = []

    # 조건 없는 선택지 풀
    free_pool = [
        {"text": "운동을 한다", "effect": {"체력": 2}},
        {"text": "공부를 한다", "effect": {"지능": 2}},
        {"text": "산책을 한다", "effect": {"민첩": 1}},
        {"text": "친구와 논다", "effect": {"행운": 1}},
        {"text": "힘든 일을 한다", "effect": {"근력": 2}},
    ]

    choices.extend(random.sample(free_pool, 3))

    # 조건 있는 선택지 2개 (potential 기준)
    for _ in range(2):
        stat = random.choice(STATS)
        max_possible = potential[stat]

        require_value = random.randint(
            max(1, max_possible - 2),
            max_possible
        )

        choices.append({
            "text": f"{stat} 시험에 도전한다 (필요 {stat} ≥ {require_value})",
            "require": {stat: require_value},
            "effect": {stat: 2}
        })

    return choices

# -------------------------
# 선택 처리 + potential 갱신
# -------------------------
def apply_choice(choice_index):
    choices = session["last_choices"]
    chosen = choices[choice_index]

    current = session["current"]
    potential = session["potential"]

    # 실제 선택 효과 반영
    for stat, val in chosen["effect"].items():
        current[stat] += val

    # potential 갱신 (이번 턴 모든 선택지 기준)
    for c in choices:
        for stat, val in c["effect"].items():
            possible = current[stat] + val
            if possible > potential[stat]:
                potential[stat] = possible

    session["current"] = current
    session["potential"] = potential

    # 나이 증가
    session["choice_count"] += 1
    if session["choice_count"] % 5 == 0:
        session["age"] += 1

# -------------------------
# API
# -------------------------
@app.route("/start", methods=["GET"])
def start():
    init_game()
    return jsonify({
        "message": "게임 시작",
        "current": session["current"],
        "potential": session["potential"],
        "age": session["age"]
    })

@app.route("/choices", methods=["GET"])
def choices():
    if "current" not in session:
        return jsonify({"error": "게임이 시작되지 않았습니다"}), 400

    new_choices = generate_choices(
        session["current"],
        session["potential"]
    )
    session["last_choices"] = new_choices

    return jsonify({
        "choices": new_choices,
        "current": session["current"],
        "potential": session["potential"],
        "age": session["age"]
    })

@app.route("/choose", methods=["POST"])
def choose():
    if "last_choices" not in session:
        return jsonify({"error": "선택지가 없습니다"}), 400

    index = request.json.get("index")
    if index is None or not (0 <= index < 5):
        return jsonify({"error": "잘못된 선택"}), 400

    apply_choice(index)

    return jsoni
