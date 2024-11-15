from flask import Flask, render_template

app = Flask(__name__)

# Sample job data (in a real app, this would come from a database)
JOBS = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'location': 'Remote',
        'salary': '$120,000',
        'description': 'Python developer needed for exciting projects.'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'New York',
        'salary': '$140,000',
        'description': 'ML expert needed for AI initiatives.'
    },
    {
        'id': 3,
        'title': 'DevOps Engineer',
        'location': 'San Francisco',
        'salary': '$130,000',
        'description': 'Looking for a CI/CD expert.'
    }
]

@app.route('/')
def home():
    return render_template('home.html', 
                         jobs=JOBS, 
                         company_name='Kratos')

@app.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    job = next((job for job in JOBS if job['id'] == job_id), None)
    return job if job else ('Job not found', 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

