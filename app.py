from flask import Flask
from kahoot import get_kahoot_leaderboard, get_attendance
import json
import os

app = Flask(__name__)

attendance = get_attendance()
scores = get_kahoot_leaderboard()

@app.route("/attendance")
def get_attendance():
    return json.dumps({"success": True, "data": {
        "attendance": attendance,
    }})

@app.route("/leaderboard")
def get_leaderboard():
    return json.dumps({"success": True, "data": {
        "kahoot_scores": scores,
    }})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
