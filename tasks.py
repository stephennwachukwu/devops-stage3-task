import os
from dotenv import load_dotenv
from celery import Celery
import smtplib
import traceback
import logging
from datetime import datetime

load_dotenv()

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task()
def send_mail(receivers):
    print(f"Attempting to send email to {receivers}")
    logging.info(f"Attempting to send email to {receivers}")
    try:
        smtp_server = 'smtp.gmail.com'
        port = 587
        username = os.getenv("USER_EMAIL")
        password = os.getenv("USER_TOKEN")
        sender = 'hello@stephennwac.io'
        message = """From: Indiestephan from Mailtrap <hello@stephennwac.io>
To: stephen nwachukwu <stephennwac007@gmail.com>
Subject: Check out my awesome email for 


This is my test email sent with Python using Mailtrap's SMTP credentials. WDYT?
"""
    #with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #    server.ehlo()
   #     server.starttls()
  #      server.ehlo()
 #       server.login("stephennwac007@gmail.com", "ykndjrkknqcewhou")
#        server.sendmail(sender, receivers, message)
#        print(f"Email sent to {receivers}")
        logging.info(f"Connecting to SMTP server: {smtp_server}:{port}")
        with smtplib.SMTP(smtp_server, port) as server:
            logging.info("Starting TLS")
            server.ehlo()
            server.starttls()
            server.ehlo()
            logging.info("Logging in")
            server.login(username, password)
            logging.info("Sending email")
            server.sendmail(sender, receivers, message)
        print(f"Email sent to {receivers}")
        logging.info(f"Email sent successfully to {receivers}")
    except (smtplib.SMTPException, IOError) as e:
        error_message = f"Failed to send email to {receivers}. Error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        raise send_mail.retry(exc=e)  # Retry after 120 seconds
    except Exception as e:
        error_message = f"Unexpected error when sending email to {receivers}. Error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        raise

@app.task
def log_message():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Current time logged: {now}")
    print("Message logged")

