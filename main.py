from flask import Flask, session, jsonify, request, render_template_string
import random

app = Flask(__name__)
app.secret_key = "trpg-life-secret"

STATS = ["체력", "근력", "지능", "민첩", "행운"]

# -------------------------
# 게임 로직
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

def generate_choices(current, potential):
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
        max_possible = potential[stat]
        require_value = random.randint(max(1, max_possible - 2), max_possible)

        choices.append({
            "text": f"{stat} 시험에 도전한다 (필요 {stat} ≥ {require_value})",
            "require": {stat: require_value},
            "effect": {stat: 2}
        })

    return choices

def apply_choice(index):
    choices = session["last_choices"]
    chosen = choices[index]

    current = session["current"]
    potential = session["potential"]

    for stat, val in chosen["effect"].items():
        current[stat] += val

    # potential 갱신 (선택하지 않은 선택지도 반영)
    for c in choices:
        for stat, val in c["effect"].items():
            possible = current[stat] + val
            if possible > potential[stat]:
                potential[stat] = possible

    session["choice_count"] += 1
    if session["choice_count"] % 5 == 0:
        session["age"] += 1

# -------------------------
# UI (HTML + JS 통합)
# -------------------------
HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>TRPG 인생 시뮬레이터</title>
<style>
body { font-family: Arial; padding: 20px; }
#stats { position: fixed; top: 20px; right: 20px; border: 1px solid #aaa; padding: 10px; }
button { margin: 5px 0; width: 100%; }
button:disabled { background: #ccc; }
</style>
</head>
<body>

<h1>TRPG 인생 시뮬레이터</h1>

<button onclick="startGame()">게임 시작</button>
<h2 id="age"></h2>

<div id="choices"></div>

<div id="stats"></div>

<script>
let currentStats = {};

function startGame() {
    fetch("/start")
        .then(res => res.json())
        .then(data => {
            currentStats = data.current;
            updateUI(data.current, data.age);
            loadChoices();
        });
}

function loadChoices() {
    fetch("/choices")
        .then(res => res.json())
        .then(data => {
            currentStats = data.current;
            updateUI(data.current, data.age);

            const div = document.getElementById("choices");
            div.innerHTML = "<h3>선택지</h3>";

            data.choices.forEach((c, i) => {
                let disabled = false;
                let reason = "";

                if (c.require) {
                    const stat = Object.keys(c.require)[0];
                    if (currentStats[stat] < c.require[stat]) {
                        disabled = true;
                        reason = ` (조건 부족: ${stat})`;
                    }
                }

                div.innerHTML += `
                    <button ${disabled ? "disabled" : ""} onclick="choose(${i})">
                        ${c.text}${reason}
                    </button>
                `;
            });
        });
}

function choose(i) {
    fetch("/choose", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({index: i})
    })
    .then(res => res.json())
    .then(data => {
        currentStats = data.current;
        updateUI(data.current, data.age);
        loadChoices();
    });
}

function updateUI(stats, age) {
    document.getElementById("age").innerText = `나이: ${age}살`;

    let html = "<h3>스탯</h3>";
    for (let k in stats) {
        html += `${k}: ${stats[k]}<br>`;
    }
    document.getElementById("stats").innerHTML = html;
}
</script>

</body>
</html>
"""

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/start")
def start():
    init_game()
    return jsonify({
        "current": session["current"],
        "age": session["age"]
    })

@app.route("/choices")
def choices():
    new_choices = generate_choices(session["current"], session["potential"])
    session["last_choices"] = new_choices
    return jsonify({
        "choices": new_choices,
        "current": session["current"],
        "age": session["age"]
    })

@app.route("/choose", methods=["POST"])
def choose():
    idx = request.json["index"]
    apply_choice(idx)
    return jsonify({
        "current": session["current"],
        "potential": session["potential"],
        "age": session["age"]
    })

# -------------------------
# 실행
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
