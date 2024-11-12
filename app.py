from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, welcome to said's CI/CD demo app!"

@app.route('/tasks')
def tasks():
    return "This is where the tasks will be displayed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

