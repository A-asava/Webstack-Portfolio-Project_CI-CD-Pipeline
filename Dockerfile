# Use a specific version of Python that includes more packages
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies in alphabetical order for readability
RUN apt-get update && \
    apt-get install -y \
        gcc \
        libpq-dev \
        python3-distutils && \
    rm -rf /var/lib/apt/lists/*

# Install Flask and other Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project directory into /app inside the container
COPY . /app

# Expose port 5000 for the application (Flask default)
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]

