# Messaging System with RabbitMQ/Celery and Python Application behind Nginx

## Objective
Deploy a Python application behind Nginx that interacts with RabbitMQ/Celery for email sending and logging functionality.

## Requirements

### Local Setup

1. **Install RabbitMQ and Celery**
   - **RabbitMQ:** Follow the [RabbitMQ installation guide](https://www.rabbitmq.com/download.html) for your OS.
   - **Celery:** Install using pip:
     ```sh
     pip install celery
     ```

### Python Application Development

Create a Python application (`app.py`) with the following functionalities:

#### Endpoint Functionalities

1. **`?sendmail`**
   - Sends an email using SMTP to the provided value (e.g., `?sendmail=destiny@destinedcodes.com`).
   - Uses RabbitMQ/Celery to queue the email sending task.
   - The email-sending script retrieves and executes tasks from the queue.

2. **`?talktome`**
   - Logs the current time to `/var/log/messaging_system.log`.

3. **`/logs`**
   - Displays the application logs in real-time.

#### Python Application Code
```python
from flask import Flask, request, Response, stream_with_context
from celery import Celery
from datetime import datetime
import smtplib
import logging
import os

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Set up logging
log_file = '/tmp/messaging_system.log'  # Change to a writable location
logging.basicConfig(filename=log_file, level=logging.INFO)

@celery.task
def send_email(recipient):
    sender = "your_email@example.com"
    message = f"Subject: Hello\n\nThis is a test email to {recipient}."
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender, 'your_password')
        server.sendmail(sender, recipient, message)

@app.route('/')
def home():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    if sendmail:
        send_email.delay(sendmail)
        return f"Email queued to {sendmail}"
    elif talktome:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Current time logged: {now}")
        return "Logged the current time."
    return "Welcome to the messaging system!"

@app.route('/logs')
def logs():
    def generate():
        with open(log_file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                yield line
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### Nginx Configuration

Configure Nginx to serve your Python application.

#### `nginx.conf`
```nginx
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    upstream flask_app {
        server localhost:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Endpoint Access

1. **Expose Local Application**
   - Use ngrok to expose your local application endpoint:
     ```sh
     ./ngrok http 80
     ```
   - This will provide a URL to access your application externally.

### Submission Requirements

1. Provide the ngrok (or equivalent) endpoint for testing.
2. Submit a screen recording walk-through.
3. Ensure all requirements are met and the application functions correctly.

### Evaluation Criteria

1. **Functionality:** All specified features must work correctly.
2. **Clarity:** Code and configurations must be well-documented.
3. **Presentation:** The screen recording should be clear and comprehensive.
4. **Deadline Adherence:** Strict deadline, no late submissions accepted.

---

This README provides a comprehensive guide for setting up a messaging system with a Python application behind Nginx, using RabbitMQ/Celery for email sending and logging functionality. Follow each step to ensure your application meets the requirements and functions correctly.
