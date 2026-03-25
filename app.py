from flask import Flask, jsonify
from kahoot import get_kahoot_leaderboard, get_attendance as load_attendance
import os

app = Flask(__name__)

attendance = load_attendance()
scores = get_kahoot_leaderboard()

@app.route("/attendance")
def get_attendance_endpoint():
    return jsonify({
        "success": True,
        "data": {"attendance": attendance},
    })

@app.route("/leaderboard")
def get_leaderboard():
    return jsonify({
        "success": True,
        "data": {"kahoot_scores": scores},
    })

@app.route("/leaderboard/<int:week_id>")
def get_weekly_leaderboard(week_id):
    return jsonify({
        "success": True,
        "data": {"kahoot_scores": get_kahoot_leaderboard(week_id)},
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
