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

