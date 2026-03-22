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

HTML_PAGE = """
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>DevSecOps Tasks</title>
  </head>
  <body>
    <h1>Pipeline DevSecOps Flask + Redis</h1>
    <p>Instance déployée automatiquement via GitHub Actions + ArgoCD.</p>

    <h2>Tâches</h2>
    <ul>
      {% for t in tasks %}
        <li>{{ t }}</li>
      {% endfor %}
    </ul>

    <form method="post" action="/add">
      <input type="text" name="task" placeholder="Nouvelle tâche">
      <button type="submit">Ajouter</button>
    </form>
  </body>
</html>
"""

@app.route("/")
def index():
    tasks = r.lrange("tasks", 0, -1)
    return render_template_string(HTML_PAGE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task_form():
    from flask import request, redirect
    task = request.form.get("task", "")
    if task:
        r.rpush("tasks", task)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
