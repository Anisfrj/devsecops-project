from flask import Flask, jsonify, request
import redis
import os

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis-service"),
    port=6379,
    decode_responses=True
)

@app.route("/health")
def health():
    return jsonify({"status": "c'est carré"}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = r.lrange("tasks", 0, -1)
    return jsonify({"tasks": tasks}), 200

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task", "")
    if not task:
        return jsonify({"error": "Champ 'task' manquant"}), 400
    r.rpush("tasks", task)
    return jsonify({"message": "Tâche ajoutée", "task": task}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
