from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/')
def home():
    """Render the homepage with updated content for testing."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CI/CD Demo App</title>
    </head>
    <body>
        <h1>Hello, welcome to Saidi's CI/CD demo app!</h1>
        <p>This is a simple demo app with a basic CI/CD pipeline.</p>
        <a href="/tasks">View Tasks</a>
    </body>
    </html>
    """
    response = make_response(html_content)
    # Adding security headers for tests
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/tasks')
def tasks():
    """Render the tasks page."""
    return render_template("tasks.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

