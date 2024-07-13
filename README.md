# Messaging System with RabbitMQ/Celery and Python Application behind Nginx

## Here’s how you can set up the Python application with RabbitMQ/Celery for email sending and logging functionality, and configure it behind Nginx.

### Step 1: Install RabbitMQ and Celery
Install RabbitMQ and Celery on your local machine:

#### RabbitMQ Installation
- **Ubuntu/Debian**:
  ```sh
  sudo apt-get update
  sudo apt-get install rabbitmq-server
  sudo systemctl enable rabbitmq-server
  sudo systemctl start rabbitmq-server
  ```
- **MacOS**:
  ```sh
  brew install rabbitmq
  brew services start rabbitmq
  ```

#### Celery Installation
Install Celery using pip:
```sh
pip install celery
```

### Step 2: Set up a Python Application
Create a Python application with the necessary functionalities:

#### Directory Structure
```
myapp/
│
├── app.py
├── tasks.py
├── requirements.txt
└── celeryconfig.py
```

#### app.py
```python
from flask import Flask, request
from tasks import send_mail, log_message
import logging

app = Flask(__name__)

logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_mail.delay(sendmail)
        return f"Email to {sendmail} queued."
    
    if talktome:
        log_message.delay()
        return "Message logged."

    return "Hello, use ?sendmail=<email> or ?talktome"

if __name__ == '__main__':
    app.run(debug=True)
```

#### tasks.py
```python
from celery import Celery
import smtplib
import logging
from datetime import datetime

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_mail(email):
    with smtplib.SMTP('localhost') as server:
        server.sendmail('youremail@example.com', email, 'Subject: Test\n\nThis is a test email.')
        print(f"Email sent to {email}")

@app.task
def log_message():
    logging.info(f"Current time: {datetime.now()}")
    print("Message logged")
```

#### celeryconfig.py
```python
broker_url = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'
```

#### requirements.txt
```txt
Flask
celery
```

Install the requirements:
```sh
pip install -r requirements.txt
```

### Step 3: Configure Nginx

#### nginx.conf
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Start Nginx:
```sh
sudo nginx -s reload
```

### Step 4: Expose Application Using ngrok
Install ngrok and expose the local application:

```sh
ngrok http 80
```

ngrok will provide a stable endpoint to access your application externally.

### Running the Application
1. Start RabbitMQ server:
   ```sh
   sudo systemctl start rabbitmq-server
   ```

2. Start the Celery worker:
   ```sh
   celery -A tasks worker --loglevel=info
   ```

3. Start the Flask application:
   ```sh
   python3 app.py
   ```

Now you can access the endpoints using the URL provided by ngrok, e.g., `http://your_ngrok_url/?sendmail=example@example.com` or `http://your_ngrok_url/?talktome`. This setup will queue email sending tasks and log messages to a file.
