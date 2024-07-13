from celery import Celery
import smtplib
import logging
from datetime import datetime

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_mail(receivers):
    sender = 'hello@stephennwac.io'
    #receivers = ['stephennwac007@gmail.com']
    message = """From: Indiestephan from Mailtrap <hello@stephennwac.io>
To: stephen nwachukwu <stephennwac007@gmail.com>
Subject: Check out my awesome email for 


This is my test email sent with Python using Mailtrap's SMTP credentials. WDYT?
"""
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("stephennwac007@gmail.com", "ykndjrkknqcewhou")
        server.sendmail(sender, receivers, message)
        print(f"Email sent to {receivers}")

@app.task
def log_message():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Current time logged: {now}")
    print("Message logged")

