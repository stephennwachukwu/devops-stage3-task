from flask import Flask, request, Response, stream_with_context
from tasks import send_mail, log_message
from datetime import datetime
import logging
import os
import re

app = Flask(__name__)

log_file = '/var/log/messaging_system.log'
if not os.path.exists('/var/log'):
    os.makedirs('/var/log')
if not os.path.exists(log_file):
    open(log_file, 'w').close()
logging.basicConfig(filename=log_file, level=logging.INFO)

def is_valid_email(email):
    # Regular expression for validating an email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        #send_mail.delay(sendmail)
        #return f"Email to {sendmail} queued."
        if is_valid_email(sendmail):
            try:
                send_mail.delay(sendmail)
                return f"Email queued for sending to {sendmail}"
            except Exception as e:
                return f"Failed to send email: {str(e)}", 500
        else:
            return "Invalid email format", 400
    elif talktome:
        log_message.delay()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Current time logged: {now}")
        return "Logged the current time."
    else:
        return "Welcome to the messaging system! Use ?sendmail OR ?talktome parameters to Communicate"

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
    app.run(host='0.0.0.0', port=8000, debug=True)

