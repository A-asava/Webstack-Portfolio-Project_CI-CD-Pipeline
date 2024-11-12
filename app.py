from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/')
def home():
    return "Hello, welcome to Saidi's CI/CD demo app!"

@app.route('/tasks')
def tasks():
    return "This is where the tasks will be displayed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

