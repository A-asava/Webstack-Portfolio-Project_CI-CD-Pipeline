from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory storage for tasks
tasks = []

@app.route('/')
def home():
    return "Hello, welcome to said's CI/CD demo app!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.json.get("task")
    if new_task:
        tasks.append(new_task)
        return jsonify({"message": "Task added successfully.", "task": new_task}), 201
    return jsonify({"error": "No task provided."}), 400

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if task_id < len(tasks):
        return jsonify({"task": tasks[task_id]})
    return jsonify({"error": "Task not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

