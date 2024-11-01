# Use a specific version of Python that includes more packages
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and Python's distutils
RUN apt-get update && \
    apt-get install -y python3-distutils gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Django
RUN pip install --upgrade pip
RUN pip install django==3.2

# Copy the current directory contents into the container at /app
COPY . .

# Run database migrations
RUN python manage.py migrate

# Expose port 8000 for the application
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

