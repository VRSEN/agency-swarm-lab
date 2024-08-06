# Use the official Python image from the Docker Hub
FROM python:3.12-slim  

# Set environment variable to allow print statements to be displayed immediately
ENV PYTHONUNBUFFERED=1 

# Set the working directory in the container
WORKDIR /app

# Install build tools and other dependencies
RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./Slack-app .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Slack app
CMD ["sh", "-c", "uvicorn app:api --host 0.0.0.0 --port 8000"]