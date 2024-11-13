from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    # Security headers for best practices
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/tasks')
def tasks():
    response = make_response(render_template('tasks.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/about')
def about():
    return "This app demonstrates a simple CI/CD pipeline."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

