from flask import Flask, jsonify, request, render_template_string, redirect
import redis, os

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis-service"), port=6379, decode_responses=True)

HTML_PAGE = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>DevSecOps - Task Manager</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; }
    h1 { color: #2d6a4f; }
    ul { list-style: none; padding: 0; }
    li { background: #f0f0f0; margin: 5px 0; padding: 10px; border-radius: 5px; }
    input { padding: 8px; width: 70%; }
    button { padding: 8px 16px; background: #2d6a4f; color: white; border: none; border-radius: 5px; cursor: pointer; }
    .badge { background: #2d6a4f; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px; }
  </style>
</head>
<body>
  <h1>🚀 Task Manager</h1>
  <p>Déployé automatiquement via <span class="badge">GitHub Actions</span> + <span class="badge">ArgoCD</span> + <span class="badge">Kubernetes</span></p>
  <h2>Tâches ({{ tasks|length }})</h2>
  <ul>
    {% for t in tasks %}
      <li>✅ {{ t }}</li>
    {% else %}
      <li>Aucune tâche pour le moment.</li>
    {% endfor %}
  </ul>
  <form method="post" action="/add">
    <input type="text" name="task" placeholder="Nouvelle tâche...">
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
    task = request.form.get("task", "")
    if task:
        r.rpush("tasks", task)
    return redirect("/")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "flask-api"}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": r.lrange("tasks", 0, -1)}), 200

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
